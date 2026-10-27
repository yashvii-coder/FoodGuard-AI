from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st


LOG_PATH = Path("data/food_log.csv")
NUTRITION_PATH = Path("data/nutrition.csv")


def get_foods():
    if NUTRITION_PATH.exists():
        df = pd.read_csv(NUTRITION_PATH)

        col = next(
            (
                c for c in df.columns
                if c.lower() in ["food", "name", "food_name", "item"]
            ),
            None
        )

        if col:
            return sorted(
                df[col].dropna().astype(str).unique().tolist()
            )

    return [
        "burger",
        "butter_naan",
        "chai",
        "chapati",
        "chole_bhature",
        "dal_makhani",
        "dhokla",
        "fried_rice",
        "idli",
        "jalebi",
        "kaathi_rolls",
        "kadai_paneer",
        "kulfi",
        "masala_dosa",
        "momos",
        "paani_puri",
        "pakode",
        "pav_bhaji",
        "pizza",
        "samosa"
    ]


def lookup(food, grams):

    df = (
        pd.read_csv(NUTRITION_PATH)
        if NUTRITION_PATH.exists()
        else pd.DataFrame()
    )

    if df.empty:
        return {
            "calories": 0,
            "protein": 0,
            "carbohydrates": 0,
            "fat": 0,
            "fiber": 0
        }

    col = next(
        (
            c for c in df.columns
            if c.lower() in ["food", "name", "food_name", "item"]
        ),
        None
    )

    row = (
        df[df[col].astype(str).str.lower() == food.lower()]
        if col
        else pd.DataFrame()
    )

    if row.empty:
        return {
            "calories": 0,
            "protein": 0,
            "carbohydrates": 0,
            "fat": 0,
            "fiber": 0
        }

    r = row.iloc[0]

    def get(names):

        for c in df.columns:

            if c.lower() in names:

                try:
                    return float(r[c])
                except:
                    return 0

        return 0

    ref = get({
        "reference_grams",
        "reference_g",
        "grams",
        "serving_grams",
        "per_grams"
    }) or 100

    f = grams / ref

    return {
        "calories": round(
            get({
                "calories_kcal",
                "calories",
                "kcal",
                "energy_kcal"
            }) * f,
            1
        ),

        "protein": round(
            get({
                "protein_g",
                "protein"
            }) * f,
            1
        ),

        "carbohydrates": round(
            get({
                "carbohydrates_g",
                "carbohydrates",
                "carbs_g",
                "carbs"
            }) * f,
            1
        ),

        "fat": round(
            get({
                "fat_g",
                "fat",
                "total_fat_g"
            }) * f,
            1
        ),

        "fiber": round(
            get({
                "fiber_g",
                "fibre_g",
                "fiber",
                "fibre"
            }) * f,
            1
        )
    }


def show_manual_log():

    st.markdown(
        '<div class="section-heading">Add Food Manually</div>'
        '<div class="section-description">Enter your food and portion to estimate its nutrition and add it to your Daily Diary.</div>',
        unsafe_allow_html=True,
    )

    foods = get_foods()

    food = st.selectbox(
        "Food",
        foods,
        format_func=lambda x: x.replace("_", " ").title()
    )

    col1, col2 = st.columns(2)

    with col1:

        source = st.selectbox(
            "Where did you eat it?",
            ["Home", "Restaurant"]
        )

    with col2:

        grams = st.number_input(
            "Quantity (grams)",
            min_value=10,
            max_value=3000,
            value=100,
            step=10
        )

    nutrition = lookup(food, grams)

    st.markdown("### Nutrition Estimate")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Calories",
            f"{nutrition['calories']} kcal"
        )

    with c2:
        st.metric(
            "Protein",
            f"{nutrition['protein']} g"
        )

    with c3:
        st.metric(
            "Carbohydrates",
            f"{nutrition['carbohydrates']} g"
        )

    with c4:
        st.metric(
            "Fat",
            f"{nutrition['fat']} g"
        )

    st.caption(
        f"Estimated nutrition for {grams} g of "
        f"{food.replace('_', ' ').title()}."
    )

    if st.button(
        "➕ Add to Daily Diary",
        type="primary",
        use_container_width=True
    ):

        row = pd.DataFrame([
            {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%H:%M"),
                "food": food,
                "source": source,
                "portion": f"{grams} g",
                "grams": grams,
                "calories": nutrition["calories"],
                "protein": nutrition["protein"],
                "carbohydrates": nutrition["carbohydrates"],
                "fat": nutrition["fat"],
                "fiber": nutrition["fiber"],
                "confidence": 100,
                "entry_type": "manual"
            }
        ])

        LOG_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if LOG_PATH.exists():

            row.to_csv(
                LOG_PATH,
                mode="a",
                header=False,
                index=False
            )

        else:

            row.to_csv(
                LOG_PATH,
                index=False
            )

        st.success(
            f"{food.replace('_', ' ').title()} "
            f"was added to your Daily Diary."
        )