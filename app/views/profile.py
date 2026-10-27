import json
import os

import streamlit as st

from services.health_engine import (
    calculate_bmi,
    get_bmi_category,
    get_bmi_message,
    get_healthy_weight_range
)


# ============================================================
# PROFILE STORAGE
# ============================================================

PROFILE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "user_profiles.json"
)


def get_user_key():

    user = st.session_state.get("auth_user")

    if isinstance(user, dict):

        return (
            user.get("email")
            or user.get("username")
            or user.get("name")
            or "default_user"
        )

    if user:
        return str(user)

    return "default_user"


def load_profiles():

    os.makedirs(
        os.path.dirname(PROFILE_FILE),
        exist_ok=True
    )

    if not os.path.exists(PROFILE_FILE):
        return {}

    try:

        with open(
            PROFILE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


def save_profile(profile):

    profiles = load_profiles()

    profiles[get_user_key()] = profile

    with open(
        PROFILE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            profiles,
            file,
            indent=4
        )


def load_profile():

    profiles = load_profiles()

    return profiles.get(
        get_user_key()
    )


# ============================================================
# PAGE
# ============================================================

def show_profile():

    st.markdown(
        '<div class="section-heading">🌿 Your Personal Profile</div>'
        '<div class="section-description">Tell FoodGuard AI a little about yourself so it can create a more personalized food and fitness experience.</div>',
        unsafe_allow_html=True,
    )

    existing = load_profile()

    if existing:

        st.success(
            "Your profile is already saved. You can update it anytime."
        )

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    st.markdown("### 👤 Basic Information")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Name",
            value=existing.get("name", "") if existing else "",
            placeholder="Enter your name"
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=int(existing.get("age", 21)) if existing else 21
        )

        sex = st.selectbox(
            "Sex",
            [
                "Female",
                "Male"
            ],
            index=(
                1
                if existing and existing.get("sex") == "Male"
                else 0
            )
        )

    with col2:

        height = st.number_input(
            "Height (cm)",
            min_value=100.0,
            max_value=230.0,
            value=float(
                existing.get("height_cm", 165)
                if existing
                else 165
            ),
            step=0.5
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=25.0,
            max_value=250.0,
            value=float(
                existing.get("weight_kg", 60)
                if existing
                else 60
            ),
            step=0.5
        )

        diet = st.selectbox(
            "Diet Preference",
            [
                "Vegetarian",
                "Non-Vegetarian",
                "Mixed"
            ],
            index=(
                [
                    "Vegetarian",
                    "Non-Vegetarian",
                    "Mixed"
                ].index(existing["diet"])
                if existing and existing.get("diet") in [
                    "Vegetarian",
                    "Non-Vegetarian",
                    "Mixed"
                ]
                else 0
            )
        )

    # --------------------------------------------------------
    # ACTIVITY
    # --------------------------------------------------------

    st.markdown("### 🏃 Activity & Lifestyle")

    activity_options = [
        "Sedentary",
        "Lightly active",
        "Moderately active",
        "Very active"
    ]

    activity = st.selectbox(
        "Typical Activity Level",
        activity_options,
        index=(
            activity_options.index(existing["activity_level"])
            if existing
            and existing.get("activity_level") in activity_options
            else 0
        )
    )

    # --------------------------------------------------------
    # HEALTH INFORMATION
    # --------------------------------------------------------

    st.markdown("### 🩺 Health & Safety")

    allergies = st.text_input(
        "Food allergies",
        value=(
            existing.get("allergies", "")
            if existing else ""
        ),
        placeholder="Example: peanuts, milk, shellfish"
    )

    intolerances = st.text_input(
        "Food intolerances",
        value=(
            existing.get("intolerances", "")
            if existing else ""
        ),
        placeholder="Example: lactose"
    )

    disliked_foods = st.text_input(
        "Foods you dislike",
        value=(
            existing.get("disliked_foods", "")
            if existing else ""
        ),
        placeholder="Example: broccoli, tofu"
    )

    health_conditions = st.text_area(
        "Health conditions / medications",
        value=(
            existing.get("health_conditions", "")
            if existing else ""
        ),
        placeholder=(
            "Optional. Example: diabetes, hypertension, "
            "PCOS, thyroid condition, etc."
        )
    )

    exercise_limitations = st.text_area(
        "Exercise limitations or injuries",
        value=(
            existing.get("exercise_limitations", "")
            if existing else ""
        ),
        placeholder=(
            "Example: knee pain, back injury, none"
        )
    )

    # --------------------------------------------------------
    # BMI PREVIEW
    # --------------------------------------------------------

    bmi = calculate_bmi(
        weight,
        height
    )

    category = get_bmi_category(bmi)

    min_weight, max_weight = get_healthy_weight_range(
        height
    )

    st.markdown("### 📊 Your BMI Snapshot")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "BMI",
            f"{bmi:.1f}"
        )

    with c2:

        st.metric(
            "Category",
            category
        )

    with c3:

        st.metric(
            "Approx. healthy range",
            f"{min_weight}–{max_weight} kg"
        )

    st.info(
        get_bmi_message(category)
    )

    st.caption(
        "BMI is a screening measure, not a diagnosis. "
        "It does not capture every aspect of health or body composition."
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    if st.button(
        "💚 Save My Profile",
        use_container_width=True
    ):

        profile = {

            "name": name,

            "age": age,

            "sex": sex,

            "height_cm": height,

            "weight_kg": weight,

            "diet": diet,

            "activity_level": activity,

            "allergies": allergies,

            "intolerances": intolerances,

            "disliked_foods": disliked_foods,

            "health_conditions": health_conditions,

            "exercise_limitations": exercise_limitations
        }

        save_profile(profile)

        st.session_state.profile_saved = True

        st.success(
            "Profile saved successfully! 🌿"
        )

        st.rerun()