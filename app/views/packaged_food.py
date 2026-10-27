
from pathlib import Path
from datetime import datetime
import re
import time

import cv2
import numpy as np
import pandas as pd
import pytesseract
import streamlit as st
from PIL import Image


LOG_PATH = Path("data/food_log.csv")
TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")

if TESSERACT.exists():
    pytesseract.pytesseract.tesseract_cmd = str(TESSERACT)


# ============================================================
# TEXT HELPERS
# ============================================================

def clean_text(text):
    if not text:
        return ""

    text = text.replace("\x0c", " ")
    lines = []

    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)

    return "\n".join(lines)


def normal(text):
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


# ============================================================
# IMAGE / OCR
# ============================================================

def preprocess_for_ocr(image):
    rgb = np.array(image.convert("RGB"))
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    h, w = bgr.shape[:2]
    scale = 4 if max(h, w) < 1800 else 2

    enlarged = cv2.resize(
        bgr,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )

    return enlarged


def ocr_image(image, psm=11):
    config = (
        f"--oem 3 --psm {psm} "
        "-c preserve_interword_spaces=1"
    )

    try:
        return clean_text(
            pytesseract.image_to_string(
                image,
                config=config
            )
        )
    except Exception:
        return ""


def scan_package_ocr(image):
    """
    Fast multi-stage OCR. The progress UI is deliberately
    updated between stages so the user can see that scanning
    is actually happening.
    """

    progress = st.progress(0)
    status = st.empty()

    stages = [
        ("🖼️ Preparing package image...", 12),
        ("🔍 Enlarging the label for OCR...", 28),
        ("📝 Reading product information...", 48),
        ("🥗 Reading the nutrition table...", 68),
        ("🧪 Reading ingredients and allergens...", 84),
        ("🧠 Organising the detected information...", 96),
    ]

    for message, value in stages[:2]:
        status.markdown(
            f"<div class='scan-status'>{message}</div>",
            unsafe_allow_html=True
        )
        progress.progress(value)
        time.sleep(0.35)

    processed = preprocess_for_ocr(image)

    h, w = processed.shape[:2]

    # Full package
    full = processed

    # Nutrition table on the supplied KitKat image is around
    # the lower-middle area. We also use broad regions so
    # other products can work.
    regions = [
        ("full", full),
        (
            "upper",
            processed[
                0:int(h * 0.60),
                0:w
            ]
        ),
        (
            "lower",
            processed[
                int(h * 0.38):h,
                0:w
            ]
        ),
        (
            "center",
            processed[
                int(h * 0.25):int(h * 0.88),
                int(w * 0.10):int(w * 0.90)
            ]
        ),
        (
            "nutrition",
            processed[
                int(h * 0.43):int(h * 0.82),
                int(w * 0.28):int(w * 0.78)
            ]
        ),
    ]

    all_results = []

    for stage_index, (name, region) in enumerate(regions):

        if name == "full":
            status.markdown(
                "<div class='scan-status'>📝 Reading product information...</div>",
                unsafe_allow_html=True
            )
            progress.progress(48)

        elif name == "nutrition":
            status.markdown(
                "<div class='scan-status'>🥗 Reading the nutrition table...</div>",
                unsafe_allow_html=True
            )
            progress.progress(68)

        else:
            status.markdown(
                "<div class='scan-status'>🧪 Reading package details...</div>",
                unsafe_allow_html=True
            )

        # PSM 6 works well for blocks/tables, PSM 11 for
        # scattered package text.
        for psm in ([6, 11] if name in ("full", "nutrition") else [11]):
            text = ocr_image(region, psm)

            if text:
                all_results.append(
                    f"--- {name} / psm{psm} ---\n{text}"
                )

    status.markdown(
        "<div class='scan-status'>🧠 Organising the detected information...</div>",
        unsafe_allow_html=True
    )
    progress.progress(96)
    time.sleep(0.35)

    combined = "\n\n".join(all_results)

    progress.progress(100)
    status.markdown(
        "<div class='scan-status scan-complete'>✅ Package scan complete</div>",
        unsafe_allow_html=True
    )
    time.sleep(0.45)

    progress.empty()
    status.empty()

    return combined


# ============================================================
# PRODUCT NAME / CATEGORY
# ============================================================

KNOWN_PRODUCTS = [
    ("kitkat", "KitKat"),
    ("kit kat", "KitKat"),
    ("dairy milk", "Cadbury Dairy Milk"),
    ("5 star", "Cadbury 5 Star"),
    ("five star", "Cadbury 5 Star"),
    ("perk", "Cadbury Perk"),
    ("munch", "Nestlé Munch"),
    ("milkybar", "Nestlé Milkybar"),
    ("snickers", "Snickers"),
    ("twix", "Twix"),
    ("oreo", "Oreo"),
    ("parle-g", "Parle-G"),
    ("parle g", "Parle-G"),
    ("good day", "Britannia Good Day"),
    ("hide & seek", "Parle Hide & Seek"),
    ("hide and seek", "Parle Hide & Seek"),
    ("maggi", "Maggi"),
    ("kurkure", "Kurkure"),
    ("lays", "Lay's"),
    ("lay's", "Lay's"),
    ("bingo", "Bingo!"),
    ("pringles", "Pringles"),
    ("sunfeast", "Sunfeast"),
    ("britannia", "Britannia"),
    ("unibic", "Unibic"),
]

CATEGORY_RULES = [
    (["chocolate", "cocoa", "cocoa solids", "milk chocolate"], "Chocolate"),
    (["wafer"], "Chocolate Wafer"),
    (["chips", "potato chips", "potato"], "Chips"),
    (["namkeen", "sev", "bhujia"], "Namkeen"),
    (["biscuit", "biscuits", "cookie", "cookies"], "Biscuits / Cookies"),
    (["noodle", "noodles", "masala noodles"], "Instant Noodles"),
    (["instant noodles"], "Instant Noodles"),
    (["juice", "fruit drink"], "Juice / Fruit Drink"),
    (["soft drink", "carbonated", "cola"], "Soft Drink"),
    (["cereal", "flakes", "muesli"], "Cereal"),
    (["cake", "sponge cake"], "Cake"),
    (["bread", "bun"], "Bread"),
    (["ice cream", "icecream"], "Ice Cream"),
    (["namkeen", "snack"], "Packaged Snack"),
]


def detect_product_name(text):
    low = normal(text)

    # Exact/common product or brand detection first.
    for key, label in KNOWN_PRODUCTS:
        if key in low:
            return label

    # Try common phrases around "product/brand".
    patterns = [
        r"(?:brand|product)\s*[:\-]\s*([A-Za-z][A-Za-z0-9 &'!-]{2,50})",
        r"(?:manufactured|marketed)\s+by\s+([A-Za-z][A-Za-z0-9 &'!-]{2,50})",
    ]

    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            candidate = m.group(1).strip()
            cand_low = candidate.lower()
            if (
                len(candidate) >= 3
                and cand_low not in {
                    "full package", "original_psm6", "original_psm6.png",
                    "psm6", "psm11", "full", "original", "package", "original_psm11"
                }
                and not cand_low.endswith(".png")
            ):
                return candidate[:60]

    # Category fallback.
    for keywords, label in CATEGORY_RULES:
        if any(k in low for k in keywords):
            return label

    return "Packaged Food"


# ============================================================
# BASIC PRODUCT INFORMATION
# ============================================================

def first_match(text, patterns):
    for pattern in patterns:
        m = re.search(pattern, text, re.I | re.S)
        if m:
            value = m.group(1).strip()
            value = re.sub(r"\s+", " ", value)
            if value:
                return value
    return None


def extract_basic_info(text):
    data = {}

    data["Product"] = detect_product_name(text)

    data["Net Weight"] = first_match(
        text,
        [
            r"net\s*w(?:eight|eigh[t7])\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?\s*(?:g|kg|ml|l))",
            r"net\s*weight.*?([0-9]+(?:\.[0-9]+)?\s*(?:g|kg|ml|l))",
        ]
    )

    data["MRP"] = first_match(
        text,
        [
            r"mrp.*?(?:rs\.?|₹)?\s*([0-9]+(?:\.[0-9]+)?)",
            r"maximum\s*retail\s*price.*?([0-9]+(?:\.[0-9]+)?)",
        ]
    )

    fssai = first_match(
        text,
        [
            r"(?:fssai|lic\.?|license).*?([0-9]{10,15})",
        ]
    )
    data["FSSAI"] = fssai

    data["Best Before / Expiry"] = first_match(
        text,
        [
            r"best\s*before\s*([^\n]{3,80})",
            r"best\s*before.*?([0-9]+\s*(?:months?|days?|years?)[^\n]{0,50})",
            r"expiry\s*[:\-]?\s*([^\n]{3,80})",
            r"use\s*before\s*[:\-]?\s*([^\n]{3,80})",
        ]
    )

    data["Storage"] = first_match(
        text,
        [
            r"storage\s*(?:condition)?s?\s*[:\-]?\s*([^\n]{3,120})",
            r"store\s+in\s+(?:a\s+)?([^\n]{3,120})",
        ]
    )

    return data


# ============================================================
# NUTRITION
# ============================================================

NUTRIENTS = {
    "Energy": ["energy", "calories", "kcal"],
    "Protein": ["protein"],
    "Carbohydrates": ["carbohydrate", "carbohydrates", "carbs"],
    "Total Sugars": ["total sugars", "sugars"],
    "Added Sugars": ["added sugars", "added sugar"],
    "Total Fat": ["total fat", "fat"],
    "Saturated Fat": ["saturated fat", "saturates"],
    "Trans Fat": ["trans fat"],
    "Fibre": ["dietary fibre", "dietary fiber", "fibre", "fiber"],
    "Sodium": ["sodium"],
}


def clean_ocr_line(line):
    line = normal(line)

    corrections = {
        "proteln": "protein",
        "protelin": "protein",
        "carbohydrat": "carbohydrate",
        "carbohydratse": "carbohydrates",
        "sodlum": "sodium",
        "sodtum": "sodium",
        "flbre": "fibre",
        "flber": "fiber",
    }

    for bad, good in corrections.items():
        line = line.replace(bad, good)

    return line


def numbers_from_line(line):
    # OCR sometimes turns decimal commas into commas.
    line = line.replace(",", ".")

    return re.findall(
        r"(?<![A-Za-z])\d+(?:\.\d+)?",
        line
    )


def extract_nutrition(text):
    lines = [
        x.strip()
        for x in text.splitlines()
        if x.strip()
    ]

    result = {}

    for nutrient, aliases in NUTRIENTS.items():
        value = None

        for i, raw_line in enumerate(lines):
            line = clean_ocr_line(raw_line)

            if not any(alias in line for alias in aliases):
                continue

            candidates = []

            # Same line + next 3 lines. This handles OCR that
            # separates nutrient names and numeric columns.
            for j in range(i, min(i + 4, len(lines))):
                candidates.extend(
                    numbers_from_line(lines[j])
                )

            for candidate in candidates:
                try:
                    number = float(candidate)

                    # Avoid grabbing years/license numbers.
                    if number >= 0 and number <= 100000:
                        value = number
                        break
                except ValueError:
                    continue

            if value is not None:
                break

        result[nutrient] = value

    return result


# ============================================================
# INGREDIENTS / ALLERGENS
# ============================================================

def extract_ingredients(text):
    m = re.search(
        r"ingredients?\s*[:\-]?\s*(.*?)(?=\n\s*(?:contains|may contain|nutrition|nutritional|storage|best before|mrp|$))",
        text,
        re.I | re.S
    )

    if m:
        value = re.sub(r"\s+", " ", m.group(1)).strip()
        if len(value) > 3:
            return value

    # Fallback: take the rest of the line after Ingredients.
    for line in text.splitlines():
        if "ingredient" in line.lower():
            value = re.sub(
                r"^.*?ingredients?\s*[:\-]?\s*",
                "",
                line,
                flags=re.I
            ).strip()
            if value:
                return value

    return "Not detected"


def extract_allergens(text):
    found = []

    for pattern in [
        r"may\s*contain\s*[:\-]?\s*([^\n]+)",
        r"contains\s*[:\-]?\s*([^\n]+)",
    ]:
        for value in re.findall(pattern, text, re.I):
            value = re.sub(r"\s+", " ", value).strip()

            if value and len(value) > 2:
                if value.lower() not in [x.lower() for x in found]:
                    found.append(value)

    return " | ".join(found) if found else "Not detected"


# ============================================================
# MAIN EXTRACTION
# ============================================================

def extract_product_info(text):
    data = {}

    data.update(extract_basic_info(text))
    data.update(extract_nutrition(text))

    data["Ingredients"] = extract_ingredients(text)
    data["Allergens"] = extract_allergens(text)

    return data


# ============================================================
# DIARY
# ============================================================

def save_to_diary(data):
    LOG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    row = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "food": data.get("Product") or "Packaged Food",
        "quantity": data.get("Net Weight") or "",
        "source": "Outside",
        "calories": data.get("Energy") or "",
        "protein": data.get("Protein") or "",
        "carbs": data.get("Carbohydrates") or "",
        "fat": data.get("Total Fat") or "",
    }

    new_df = pd.DataFrame([row])

    if LOG_PATH.exists():
        try:
            old_df = pd.read_csv(LOG_PATH)
            df = pd.concat(
                [old_df, new_df],
                ignore_index=True
            )
        except Exception:
            df = new_df
    else:
        df = new_df

    df.to_csv(
        LOG_PATH,
        index=False
    )


# ============================================================
# UI
# ============================================================

def show_packaged_food():

    st.markdown(
        '<div class="package-title">📦 Packaged Food Scanner</div>'
        '<div class="package-subtitle">Scan the back of a package to read nutrition, ingredients, allergens and product information.</div>',
        unsafe_allow_html=True,
    )

    input_method = st.radio(
        "Choose how to scan",
        ["🖼️ Upload Photo", "📷 Take Photo"],
        horizontal=True,
        key="package_input_method"
    )

    uploaded = None
    camera = None

    # IMPORTANT: only render the selected input.
    if input_method == "🖼️ Upload Photo":

        uploaded = st.file_uploader(
            "Upload the back of the package",
            type=["jpg", "jpeg", "png", "webp"],
            key="package_upload"
        )

        image_source = uploaded

    else:

        camera = st.camera_input(
            "Take a photo of the back of the package",
            key="package_camera"
        )

        image_source = camera

    if image_source is None:

        st.markdown(
            """
            <div class="package-empty">
                <div class="package-empty-icon">📦</div>
                <b>Upload or capture the back of your package</b>
                <br>
                <span>
                    Make sure the nutrition table and ingredients are visible.
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        return

    image = Image.open(image_source).convert("RGB")

    st.image(
        image,
        caption="Package image",
        use_container_width=True
    )

    st.markdown(
        "<div class='package-ready'>✓ Image ready for scanning</div>",
        unsafe_allow_html=True
    )

    if st.button(
        "🔍 Scan Package",
        type="primary",
        use_container_width=True,
        key="scan_package_button"
    ):

        try:
            raw_text = scan_package_ocr(image)
            data = extract_product_info(raw_text)

            st.session_state["package_raw_text"] = raw_text
            st.session_state["package_data"] = data
            st.session_state["package_scanned"] = True

            st.rerun()

        except Exception as e:

            st.error(
                f"Package scan failed: {e}"
            )

    if not st.session_state.get("package_scanned"):
        return

    data = st.session_state.get(
        "package_data",
        {}
    )

    st.markdown(
        "## 🧾 Product Information"
    )

    # The supplied image contains "KitKat" in the package
    # artwork/slogan, so this will display KitKat rather than
    # an internal OCR-processing label.
    product_name = data.get(
        "Product",
        "Packaged Food"
    )
    if (
        not product_name
        or product_name.lower().strip() in {
            "full package", "original_psm6", "original_psm6.png",
            "psm6", "psm11", "full", "original", "package", "original_psm11"
        }
        or product_name.lower().endswith(".png")
    ):
        product_name = "Packaged Food"

    st.markdown(
        f"""
        <div class="product-name-card">
            <div class="product-name-label">PRODUCT DETECTED</div>
            <div class="product-name">{product_name}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Net Weight",
            data.get("Net Weight") or "Not detected"
        )

    with col2:
        mrp = data.get("MRP")
        st.metric(
            "MRP",
            f"₹{mrp}" if mrp else "Not detected"
        )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "FSSAI",
            data.get("FSSAI") or "Not detected"
        )

    with col2:
        st.metric(
            "Best Before / Expiry",
            data.get("Best Before / Expiry")
            or "Not detected"
        )

    # --------------------------------------------------------
    # NUTRITION
    # --------------------------------------------------------

    st.markdown(
        "## 🥗 Nutrition Information"
    )

    units = {
        "Energy": "kcal",
        "Protein": "g",
        "Carbohydrates": "g",
        "Total Sugars": "g",
        "Added Sugars": "g",
        "Total Fat": "g",
        "Saturated Fat": "g",
        "Trans Fat": "g",
        "Fibre": "g",
        "Sodium": "mg",
    }

    rows = []

    for nutrient, unit in units.items():

        value = data.get(nutrient)

        if value is None:
            display = "Not detected"
        else:
            display = f"{value:g} {unit}"

        rows.append(
            {
                "Nutrient": nutrient,
                "Value": display
            }
        )

    st.dataframe(
        pd.DataFrame(rows),
        hide_index=True,
        use_container_width=True
    )

    # --------------------------------------------------------
    # INGREDIENTS
    # --------------------------------------------------------

    st.markdown("## 🧪 Ingredients")

    st.markdown(
        f"""
        <div class="package-info-card">
            {data.get("Ingredients", "Not detected")}
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # ALLERGENS
    # --------------------------------------------------------

    st.markdown("## ⚠️ Allergens")

    allergens = data.get(
        "Allergens",
        "Not detected"
    )

    if allergens != "Not detected":
        st.warning(allergens)
    else:
        st.info("No allergen statement detected.")

    # --------------------------------------------------------
    # STORAGE
    # --------------------------------------------------------

    st.markdown("## 🧊 Storage")

    st.info(
        data.get("Storage") or "Not detected"
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    if st.button(
        "💾 Save to Daily Diary",
        use_container_width=True,
        key="save_packaged_food"
    ):

        save_to_diary(data)

        st.success(
            "Packaged food saved to Daily Diary as Outside."
        )

    # --------------------------------------------------------
    # RAW OCR
    # --------------------------------------------------------

    with st.expander("🔎 View Raw OCR Text"):

        st.text(
            st.session_state.get(
                "package_raw_text",
                "No OCR text."
            )
        )


# Compatibility with older app versions.
def render_packaged_food(root=None):
    return show_packaged_food()
