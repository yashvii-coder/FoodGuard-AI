import streamlit as st

from views.profile import load_profile
from services.health_engine import (
    calculate_bmi,
    get_bmi_category,
    get_bmi_message,
    get_healthy_weight_range,
    get_calorie_estimate,
    get_exercises,
    get_videos,
)


def get_diet_plan(profile, goal):
    diet = profile["diet"]

    if goal == "Lose weight":
        if diet == "Vegetarian":
            return [
                "🌅 Breakfast: Vegetable poha / oats + fruit",
                "🥗 Lunch: 2 chapatis + dal + sabzi + salad",
                "🍎 Snack: Fruit + roasted chana",
                "🌙 Dinner: Paneer/tofu + vegetables + 1–2 chapatis",
                "💧 Stay hydrated and limit sugary drinks.",
            ]
        if diet == "Non-Vegetarian":
            return [
                "🌅 Breakfast: Eggs + whole-grain toast + fruit",
                "🥗 Lunch: Chicken/fish + roti/rice + vegetables",
                "🍎 Snack: Fruit + curd",
                "🌙 Dinner: Lean protein + vegetables + moderate carbs",
                "💧 Stay hydrated and limit sugary drinks.",
            ]
        return [
            "🌅 Breakfast: Eggs/poha/oats + fruit",
            "🥗 Lunch: Dal/chicken + roti/rice + vegetables",
            "🍎 Snack: Fruit + nuts/roasted chana",
            "🌙 Dinner: Protein + vegetables + moderate carbs",
            "💧 Stay hydrated and limit sugary drinks.",
        ]

    if goal == "Gain weight":
        return [
            "🌅 Breakfast: Oats/poha + milk/curd + fruit + nuts",
            "🥜 Snack: Peanut butter toast / nuts / banana",
            "🥗 Lunch: Rice/roti + dal + protein + vegetables",
            "🥛 Evening: Milk/curd smoothie or similar nutrient-dense snack",
            "🌙 Dinner: Protein + carbs + vegetables",
            "💚 Prioritize nutritious, energy-dense foods rather than only junk food.",
        ]

    if goal == "Build strength & fitness":
        return [
            "🌅 Breakfast: Protein-rich breakfast + fruit",
            "🥗 Lunch: Balanced protein + whole grains + vegetables",
            "🍎 Snack: Fruit + curd/nuts",
            "🌙 Dinner: Protein + vegetables + carbohydrates",
            "💪 Include protein across your meals to support training.",
        ]

    return [
        "🌅 Breakfast: Balanced protein + whole grains + fruit",
        "🥗 Lunch: Protein + vegetables + rice/roti",
        "🍎 Snack: Fruit + nuts/curd",
        "🌙 Dinner: Protein + vegetables + moderate carbohydrates",
        "💧 Keep hydration and meal timing consistent.",
    ]


def exercise_card(exercise):
    html = (
        '<div class="fg-card">'
        f'<div style="font-size:1.05rem;font-weight:800;margin-bottom:5px;">'
        f'🏋️ {exercise["name"]}</div>'
        f'<div style="color:#16A085;font-weight:700;font-size:.82rem;margin-bottom:7px;">'
        f'{exercise["duration"]}</div>'
        f'<div style="color:#667085;font-size:.84rem;line-height:1.5;">'
        f'{exercise["description"]}</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def video_card(video):
    video_id = video["video_id"]
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    html = (
        '<div class="fg-card">'
        f'<div style="font-size:1rem;font-weight:800;margin-bottom:5px;">'
        f'▶️ {video["title"]}</div>'
        f'<div style="color:#667085;font-size:.82rem;margin-bottom:10px;">'
        f'{video["description"]}</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
    st.link_button("Watch on YouTube →", youtube_url, use_container_width=True)


def show_coach():
    st.markdown(
        '<div class="section-heading">✨ FoodGuard Personal Coach</div>'
        '<div class="section-description">Your personalized food, fitness and healthy-habit assistant.</div>',
        unsafe_allow_html=True,
    )

    profile = load_profile()

    if not profile:
        st.warning("Please complete your Personal Profile first.")
        st.info("Go to the 👤 Profile tab and save your details.")
        return

    name = profile.get("name", "there")

    greeting = (
        '<div class="fg-card">'
        f'<div style="font-size:1.3rem;font-weight:800;">Hi {name} 👋</div>'
        '<div style="color:#667085;margin-top:6px;line-height:1.5;">'
        "Let's understand your current numbers and build a realistic routine around your goal."
        '</div></div>'
    )
    st.markdown(greeting, unsafe_allow_html=True)

    bmi = calculate_bmi(profile["weight_kg"], profile["height_cm"])
    category = get_bmi_category(bmi)
    min_weight, max_weight = get_healthy_weight_range(profile["height_cm"])

    st.markdown("### 📊 Your Health Snapshot")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("BMI", f"{bmi:.1f}")
    with c2:
        st.metric("BMI Category", category)
    with c3:
        st.metric("Weight Range", f"{min_weight}–{max_weight} kg")

    st.info(get_bmi_message(category))

    st.markdown("### 🎯 What would you like to work on?")

    goals = [
        "Lose weight",
        "Gain weight",
        "Maintain weight",
        "Build strength & fitness",
        "Improve body composition",
        "Specific concern",
    ]

    goal = st.selectbox("Choose your main goal", goals, key="coach_goal_select")

    specific_area = None

    if goal == "Specific concern":
        specific_area = st.selectbox(
            "What would you like to focus on?",
            [
                "Belly area",
                "Double chin",
                "Arms",
                "Thighs",
                "Glutes",
                "Back",
                "Overall fitness",
            ],
            key="coach_specific_area",
        )

        custom_goal = st.text_area(
            "Tell FoodGuard AI more",
            placeholder="Example: I want to become more active and improve my core strength.",
            key="coach_custom_goal",
        )

        if custom_goal.strip():
            st.caption(f"💬 Got it! You said: {custom_goal}")

    if specific_area in {
        "Belly area",
        "Double chin",
        "Arms",
        "Thighs",
        "Glutes",
    }:
        st.caption(
            "💡 FoodGuard AI won't promise spot fat reduction. Exercises can strengthen "
            "a specific area, while changes in body fat generally happen across the body."
        )

    if st.button(
        "✨ Generate My Personal Plan",
        use_container_width=True,
        type="primary",
        key="generate_personal_plan",
    ):
        st.session_state.coach_goal = goal
        st.session_state.coach_area = specific_area
        st.session_state.plan_generated = True

    if not st.session_state.get("plan_generated", False):
        return

    st.markdown("---")
    st.markdown("### 🧠 FoodGuard AI Analysis")

    if goal == "Lose weight":
        analysis = (
            "Your plan will focus on sustainable eating habits, regular movement, "
            "strength training and consistency."
        )
    elif goal == "Gain weight":
        analysis = (
            "Your plan will focus on nutritious calorie-dense foods, adequate protein "
            "and progressive strength training."
        )
    elif goal == "Build strength & fitness":
        analysis = (
            "Your plan will focus on progressive strength work, regular activity, "
            "recovery and balanced nutrition."
        )
    elif goal == "Improve body composition":
        analysis = (
            "We'll combine balanced nutrition with strength training and regular "
            "cardiovascular activity."
        )
    elif goal == "Specific concern":
        analysis = (
            f"We'll include exercises relevant to your {specific_area.lower()} "
            "while keeping the overall plan focused on healthy movement."
        )
    else:
        analysis = (
            "We'll focus on maintaining balanced nutrition, regular activity and "
            "sustainable daily habits."
        )

    st.info(analysis)

    st.markdown("### 🔥 Energy Estimate")

    calories = get_calorie_estimate(profile)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Estimated BMR", f'{calories["bmr"]} kcal/day')
    with c2:
        st.metric("Estimated Maintenance", f'{calories["maintenance"]} kcal/day')

    st.caption(
        "These are estimates for educational planning, not medical prescriptions. "
        "Individual needs can vary considerably."
    )

    st.markdown("### 🥗 Your Suggested Food Routine")

    for meal in get_diet_plan(profile, goal):
        st.markdown(
            f'<div class="fg-card" style="padding:.75rem .9rem;margin-bottom:.55rem;color:#173B32 !important;-webkit-text-fill-color:#173B32 !important;">{meal}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("### 🏃 Your Exercise Recommendations")

    exercises = get_exercises(goal, specific_area)
    cols = st.columns(3)

    for index, exercise in enumerate(exercises):
        with cols[index % 3]:
            exercise_card(exercise)

    st.markdown("### 🎥 Guided Workouts")

    for video in get_videos():
        video_card(video)

    st.markdown("### 📅 Simple Weekly Movement Goal")

    st.markdown(
        """<div style="color:#173B32 !important;-webkit-text-fill-color:#173B32 !important;line-height:1.8;">
        <div style="font-weight:700;margin-bottom:6px;">Start with:</div>
        <div>🚶 Regular moderate-intensity activity throughout the week</div>
        <div>💪 Strength-focused exercise at least 2 days per week</div>
        <div>🧘 Recovery and rest days</div>
        <div>💧 Adequate hydration</div>
        <div>😴 Consistent sleep</div>
        <div style="margin-top:10px;">Don't try to change everything at once. Consistency beats intensity.</div>
        </div>""",
        unsafe_allow_html=True,
    )

    if profile.get("health_conditions"):
        st.warning(
            "Because you entered a health condition or medication, use this plan as "
            "general educational guidance and check with your doctor or qualified "
            "dietitian before making major diet or exercise changes."
        )

    if profile.get("exercise_limitations"):
        st.warning(
            "Because you entered an exercise limitation or injury, avoid exercises "
            "that cause pain and get professional guidance before starting a new program."
        )

    st.success(
        "🌿 Small habits + consistency = meaningful progress. "
        "FoodGuard AI is here to help you stay on track."
    )
