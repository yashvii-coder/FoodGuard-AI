
import os
import time
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
from PIL import Image


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

MODEL_PATH = os.path.join(BASE_DIR, "models", "foodguard_food_classifier.keras")
CLASS_NAMES_PATH = os.path.join(BASE_DIR, "models", "class_names.txt")
NUTRITION_PATH = os.path.join(BASE_DIR, "data", "nutrition.csv")
LOG_PATH = os.path.join(BASE_DIR, "data", "food_log.csv")


# =========================================================
# DATA / MODEL
# =========================================================

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model not found: {MODEL_PATH}")
        return None
    return tf.keras.models.load_model(MODEL_PATH)


@st.cache_data
def load_class_names():
    if not os.path.exists(CLASS_NAMES_PATH):
        return []
    with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
        return [x.strip() for x in f if x.strip()]


@st.cache_data
def load_nutrition():
    if not os.path.exists(NUTRITION_PATH):
        return pd.DataFrame()
    return pd.read_csv(NUTRITION_PATH)


def predict_food(image):
    """Keep inference preprocessing identical to the working model pipeline."""
    model = load_model()
    classes = load_class_names()

    if model is None or not classes:
        return None

    image = image.convert("RGB").resize((224, 224))

    # IMPORTANT: do not divide by 255 here.
    image_array = np.asarray(image, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array, verbose=0)[0]

    top_indices = np.argsort(predictions)[::-1][:3]
    top_predictions = [
        (classes[int(i)], float(predictions[int(i)]) * 100)
        for i in top_indices
    ]

    best = int(top_indices[0])
    return classes[best], float(predictions[best]) * 100, top_predictions


def get_nutrition(food_name):
    df = load_nutrition()
    if df.empty:
        return None

    food_col = next(
        (c for c in df.columns if c.lower() in
         ["food", "name", "food_name", "item"]),
        None
    )

    if not food_col:
        return None

    match = df[
        df[food_col].astype(str).str.strip().str.lower()
        == food_name.strip().lower()
    ]

    return None if match.empty else match.iloc[0].to_dict()


def value(row, names, default=0.0):
    if row is None:
        return default

    lower_map = {str(k).lower(): k for k in row.keys()}

    for name in names:
        key = lower_map.get(name.lower())
        if key is not None and pd.notna(row[key]):
            try:
                return float(row[key])
            except (TypeError, ValueError):
                pass

    return default


def nutrition_for_grams(food_name, grams):
    row = get_nutrition(food_name)
    if row is None:
        return None

    reference = value(
        row,
        ["reference_grams", "reference_g", "grams", "serving_grams", "per_grams"],
        100
    )

    factor = grams / reference if reference else grams / 100

    return {
        "calories": round(value(row, ["calories_kcal", "calories", "kcal", "energy_kcal"]) * factor, 1),
        "protein": round(value(row, ["protein_g", "protein"]) * factor, 1),
        "carbohydrates": round(value(row, ["carbohydrates_g", "carbohydrates", "carbs_g", "carbs"]) * factor, 1),
        "fat": round(value(row, ["fat_g", "fat", "total_fat_g"]) * factor, 1),
        "fiber": round(value(row, ["fiber_g", "fibre_g", "fiber", "fibre"]) * factor, 1),
    }


# =========================================================
# PORTION CONTROLS
# =========================================================

def portion_controls(food_name):
    """Return total estimated grams and a human-readable portion description."""

    key = food_name.lower().strip()

    # Chole Bhature gets its own natural serving controls.
    if key == "chole_bhature":
        st.markdown(
            '<div class="portion-title">⚖️ Tell us about your portion</div>',
            unsafe_allow_html=True
        )
        st.caption("For Chole Bhature, enter the bhatura quantity and size separately.")

        c1, c2 = st.columns(2)

        with c1:
            bhatura_count = st.number_input(
                "Bhatura quantity",
                min_value=1,
                max_value=6,
                value=2,
                step=1,
                key="cb_bhatura_count"
            )

        with c2:
            bhatura_size = st.selectbox(
                "Bhatura size",
                ["Small", "Medium", "Large"],
                index=1,
                key="cb_bhatura_size"
            )

        bhatura_grams = {
            "Small": 70,
            "Medium": 100,
            "Large": 130,
        }[bhatura_size]

        chole_grams = st.number_input(
            "Chole quantity (grams)",
            min_value=50,
            max_value=600,
            value=200,
            step=10,
            key="cb_chole_grams"
        )

        total_grams = bhatura_count * bhatura_grams + chole_grams

        st.markdown(
            f"""
            <div class="portion-summary">
                <span>Estimated total portion</span>
                <strong>{total_grams} g</strong>
                <small>{bhatura_count} × {bhatura_size.lower()} bhatura + {chole_grams} g chole</small>
            </div>
            """,
            unsafe_allow_html=True
        )

        return total_grams, (
            f"{bhatura_count} {bhatura_size.lower()} bhatura + "
            f"{chole_grams} g chole"
        )

    # Pizza: slice count + size.
    if key == "pizza":
        st.markdown(
            '<div class="portion-title">⚖️ Tell us about your portion</div>',
            unsafe_allow_html=True
        )
        c1, c2 = st.columns(2)
        with c1:
            count = st.number_input("Number of slices", 1, 8, 2, 1, key="pizza_count")
        with c2:
            size = st.selectbox("Slice size", ["Small", "Medium", "Large"], index=1, key="pizza_size")

        grams_per_slice = {"Small": 80, "Medium": 110, "Large": 140}[size]
        grams = count * grams_per_slice

        st.markdown(
            f'<div class="portion-summary"><span>Estimated portion</span><strong>{grams} g</strong><small>{count} {size.lower()} slice(s)</small></div>',
            unsafe_allow_html=True
        )
        return grams, f"{count} {size.lower()} pizza slice(s)"

    if key == "dhokla":
       st.markdown(
        '<div class="portion-title">⚖️ Tell us about your portion</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        count = st.number_input(
            "Number of slices",
            1, 8, 2, 1,
            key="dhokla_count"
        )

    with c2:
        size = st.selectbox(
            "Piece size",
            ["Small", "Medium"],
            index=1,
            key="dhokla_size"
        )

    grams_per_piece = {
        "Small": 25,
        "Medium": 35
    }[size]

    grams = count * grams_per_piece

    st.markdown(
        f'<div class="portion-summary">'
        f'<span>Estimated portion</span>'
        f'<strong>{grams} g</strong>'
        f'<small>{count} {size.lower()} piece(s)</small>'
        f'</div>',
        unsafe_allow_html=True
    )

    return grams, f"{count} {size.lower()} dhokla piece(s)"

    # Momos: pieces + size.
    if key == "momos":
        st.markdown(
            '<div class="portion-title">⚖️ Tell us about your portion</div>',
            unsafe_allow_html=True
        )
        c1, c2 = st.columns(2)
        with c1:
            count = st.number_input("Number of momos", 1, 20, 6, 1, key="momo_count")
        with c2:
            size = st.selectbox("Momo size", ["Small", "Medium", "Large"], index=1, key="momo_size")

        grams_per_piece = {"Small": 18, "Medium": 25, "Large": 35}[size]
        grams = count * grams_per_piece

        st.markdown(
            f'<div class="portion-summary"><span>Estimated portion</span><strong>{grams} g</strong><small>{count} {size.lower()} momos</small></div>',
            unsafe_allow_html=True
        )
        return grams, f"{count} {size.lower()} momos"

    # Samosa / idli / jalebi / pakode / paani puri: piece based.
    piece_foods = {
        "samosa": ("Number of samosas", "Samosa size", {"Small": 45, "Medium": 70, "Large": 95}),
        "idli": ("Number of idlis", "Idli size", {"Small": 30, "Medium": 45, "Large": 65}),
        "jalebi": ("Number of pieces", "Jalebi size", {"Small": 15, "Medium": 25, "Large": 40}),
        "pakode": ("Number of pieces", "Pakoda size", {"Small": 15, "Medium": 25, "Large": 40}),
        "paani_puri": ("Number of puris", "Puri size", {"Small": 10, "Medium": 15, "Large": 20}),
    }

    if key in piece_foods:
        label, size_label, weights = piece_foods[key]

        st.markdown(
            '<div class="portion-title">⚖️ Tell us about your portion</div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)
        with c1:
            count = st.number_input(label, 1, 30, 2, 1, key=f"{key}_count")
        with c2:
            size = st.selectbox(size_label, list(weights), index=1, key=f"{key}_size")

        grams = count * weights[size]

        st.markdown(
            f'<div class="portion-summary"><span>Estimated portion</span><strong>{grams} g</strong><small>{count} {size.lower()} portion(s)</small></div>',
            unsafe_allow_html=True
        )

        return grams, f"{count} {size.lower()} portion(s)"

    # Generic foods use grams directly.
    st.markdown(
        '<div class="portion-title">⚖️ Tell us about your portion</div>',
        unsafe_allow_html=True
    )

    grams = st.number_input(
        "Quantity (grams)",
        min_value=10,
        max_value=3000,
        value=100,
        step=10,
        key=f"grams_{key}"
    )

    return grams, f"{grams} g"


# =========================================================
# EXPLANATION
# =========================================================

def food_explanation(food_name, source):
    pretty = food_name.replace("_", " ").title()

    if source == "Home":
        return (
            f"{pretty} can fit into a balanced meal when the portion is appropriate. "
            "Home preparation also gives you more control over oil, salt and ingredients."
        )

    return (
        f"{pretty} can be enjoyed occasionally, but restaurant preparation may use "
        "more oil, salt or richer ingredients. Portion size is especially important."
    )


# =========================================================
# SAVE
# =========================================================

def save_food_log(food_name, source, portion_text, grams, nutrition, confidence):
    now = datetime.now()

    row = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "food": food_name,
        "source": source,
        "portion": portion_text,
        "grams": grams,
        "calories": nutrition["calories"],
        "protein": nutrition["protein"],
        "carbohydrates": nutrition["carbohydrates"],
        "fat": nutrition["fat"],
        "fiber": nutrition["fiber"],
        "confidence": confidence,
        "entry_type": "Food Scan",
    }

    if os.path.exists(LOG_PATH):
        old = pd.read_csv(LOG_PATH)
        result = pd.concat([old, pd.DataFrame([row])], ignore_index=True)
    else:
        result = pd.DataFrame([row])

    result.to_csv(LOG_PATH, index=False)


# =========================================================
# MAIN UI
# =========================================================

def show_scan_food():

    st.markdown(
        """
        <div class="scan-hero">
            <div class="scan-icon">⌕</div>
            <div>
                <div class="scan-hero-title">Scan your food</div>
                <div class="scan-hero-text">
                    Take a photo or upload a meal and FoodGuard AI will identify it.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    input_method = st.radio(
        "Input method",
        ["📷 Camera", "🖼️ Upload"],
        horizontal=True,
        label_visibility="collapsed",
        key="food_input_method"
    )

    image = None

    if input_method.startswith("📷"):
        camera = st.camera_input(
            "Capture your food",
            key="food_camera"
        )
        if camera:
            image = Image.open(camera).convert("RGB")
    else:
        uploaded = st.file_uploader(
            "Choose a food image",
            type=["jpg", "jpeg", "png", "webp"],
            key="food_upload"
        )
        if uploaded:
            image = Image.open(uploaded).convert("RGB")

    if image is not None:

        st.markdown('<div class="preview-label">Image preview</div>', unsafe_allow_html=True)

        st.image(
            image,
            use_container_width=True
        )

        if st.button(
            "🔎  Analyze Food",
            type="primary",
            use_container_width=True,
            key="analyze_food_button"
        ):
            loader = st.empty()

            loader.markdown(
                """
                <div class="scan-loading">
                    <div class="magnifier">⌕</div>
                    <div>
                        <strong>Analyzing your food...</strong>
                        <span>Identifying the dish and checking nutrition</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            time.sleep(0.12)

            result = predict_food(image)

            loader.empty()

            if result:
                st.session_state["scan_result"] = {
                    "food": result[0],
                    "confidence": result[1],
                    "top_predictions": result[2],
                }

                # Reset portion controls when a new food is scanned.
                st.session_state["scan_food_version"] = (
                    st.session_state.get("scan_food_version", 0) + 1
                )

    result = st.session_state.get("scan_result")

    if not result:
        return

    food_name = result["food"]
    pretty = food_name.replace("_", " ").title()
    confidence = result["confidence"]
    top_predictions = result["top_predictions"]

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    confidence_class = "confidence-good" if confidence >= 70 else "confidence-low"

    st.markdown(
        f"""
        <div class="food-result-card">
            <div class="food-result-top">
                <div class="food-result-icon">🍽️</div>
                <div>
                    <div class="eyebrow">FOOD IDENTIFIED</div>
                    <div class="food-result-name">{pretty}</div>
                </div>
                <div class="confidence-pill {confidence_class}">
                    {confidence:.1f}% confident
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("🔎 View alternative predictions"):
        for food, score in top_predictions:
            cols = st.columns([3, 1])
            cols[0].write(food.replace("_", " ").title())
            cols[1].write(f"{score:.1f}%")
            st.progress(min(max(score / 100, 0), 1))

    # -----------------------------------------------------
    # PORTION
    # -----------------------------------------------------

    grams, portion_text = portion_controls(food_name)

    # -----------------------------------------------------
    # NUTRITION
    # -----------------------------------------------------

    nutrition = nutrition_for_grams(food_name, grams)

    if nutrition:
        st.markdown(
            '<div class="section-title">🥗 Nutrition estimate</div>',
            unsafe_allow_html=True
        )

        cards = [
            ("🔥", "Calories", f'{nutrition["calories"]:.1f} kcal'),
            ("🥩", "Protein", f'{nutrition["protein"]:.1f} g'),
            ("🍚", "Carbohydrates", f'{nutrition["carbohydrates"]:.1f} g'),
            ("🌾", "Fibre", f'{nutrition["fiber"]:.1f} g'),
            ("🥑", "Fat", f'{nutrition["fat"]:.1f} g'),
        ]

        for start in range(0, len(cards), 2):
            cols = st.columns(2)

            for col, item in zip(cols, cards[start:start + 2]):
                icon, label, val = item
                with col:
                    st.markdown(
                        f"""
                        <div class="nutrition-card">
                            <div class="nutrition-icon">{icon}</div>
                            <div class="nutrition-label">{label}</div>
                            <div class="nutrition-value">{val}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    else:
        st.warning("Nutrition information is not available for this food yet.")

    # -----------------------------------------------------
    # SOURCE
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🏠 Where was it made?</div>',
        unsafe_allow_html=True
    )

    source = st.radio(
        "Food source",
        ["🏠 Home Made", "🍴 Restaurant"],
        horizontal=True,
        label_visibility="collapsed",
        key="scan_source"
    )

    source_value = "Home" if source.startswith("🏠") else "Restaurant"

    st.markdown(
        f"""
        <div class="food-advice">
            <div class="advice-icon">💡</div>
            <div>{food_explanation(food_name, source_value)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    if st.button(
        "＋  Add to Daily Diary",
        type="primary",
        use_container_width=True,
        key="add_scan_to_diary"
    ):
        save_food_log(
            food_name,
            source_value,
            portion_text,
            grams,
            nutrition,
            confidence
        )
        st.success(f"{pretty} added to your Daily Diary.")


