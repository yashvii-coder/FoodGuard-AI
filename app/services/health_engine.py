import math


# ============================================================
# BMI
# ============================================================

def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI using:
    BMI = weight(kg) / height(m)^2
    """

    if weight_kg <= 0 or height_cm <= 0:
        return None

    height_m = height_cm / 100

    return weight_kg / (height_m ** 2)


def get_bmi_category(bmi):
    """
    Adult BMI categories.
    """

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Healthy weight"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obesity range"


def get_healthy_weight_range(height_cm):
    """
    Approximate adult BMI 18.5–24.9 weight range.
    """

    height_m = height_cm / 100

    minimum = 18.5 * (height_m ** 2)
    maximum = 24.9 * (height_m ** 2)

    return round(minimum, 1), round(maximum, 1)


def get_bmi_message(category):

    messages = {

        "Underweight":
            "🌱 Your body may need a little more fuel. "
            "Let's focus on nourishing meals, strength and gradual progress "
            "rather than simply chasing the scale.",

        "Healthy weight":
            "🌿 You're in a healthy BMI range! "
            "Your numbers look balanced — let's focus on feeling strong, "
            "energetic and consistent. 💚",

        "Overweight":
            "💚 You're ready for a gentle reset. "
            "Small food and movement habits can add up — "
            "let's build a plan that's realistic for you.",

        "Obesity range":
            "🌿 Let's focus on progress, not pressure. "
            "A gradual, sustainable routine around food, movement and sleep "
            "is a better goal than quick fixes."
    }

    return messages.get(
        category,
        "🌿 Let's build healthy habits around food, movement and recovery."
    )


# ============================================================
# CALORIE ESTIMATION
# ============================================================

def calculate_bmr(weight_kg, height_cm, age, sex):
    """
    Mifflin-St Jeor BMR estimation.
    This is an estimate, not a medical prescription.
    """

    if sex == "Male":

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            + 5
        )

    else:

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            - 161
        )

    return round(bmr)


def calculate_tdee(bmr, activity_level):

    activity_factors = {

        "Sedentary":
            1.20,

        "Lightly active":
            1.375,

        "Moderately active":
            1.55,

        "Very active":
            1.725
    }

    factor = activity_factors.get(
        activity_level,
        1.20
    )

    return round(bmr * factor)


def get_calorie_estimate(profile):

    bmr = calculate_bmr(
        profile["weight_kg"],
        profile["height_cm"],
        profile["age"],
        profile["sex"]
    )

    tdee = calculate_tdee(
        bmr,
        profile["activity_level"]
    )

    return {
        "bmr": bmr,
        "maintenance": tdee
    }


# ============================================================
# EXERCISE RECOMMENDATIONS
# ============================================================

EXERCISES = {

    "Lose weight": [

        {
            "name": "Brisk Walking",
            "duration": "25–40 minutes",
            "description":
                "A simple low-impact cardio option that is easy to maintain consistently."
        },

        {
            "name": "Bodyweight Squats",
            "duration": "3 × 10–15 reps",
            "description":
                "Strengthens the legs and improves lower-body fitness."
        },

        {
            "name": "Step-Ups",
            "duration": "3 × 10 reps each leg",
            "description":
                "A practical cardio and lower-body strengthening exercise."
        }
    ],

    "Gain weight": [

        {
            "name": "Bodyweight Squats",
            "duration": "3 × 10–15 reps",
            "description":
                "Builds lower-body strength and supports muscle development."
        },

        {
            "name": "Glute Bridges",
            "duration": "3 × 12–15 reps",
            "description":
                "Strengthens the glutes and posterior chain."
        },

        {
            "name": "Incline Push-Ups",
            "duration": "3 × 8–12 reps",
            "description":
                "A beginner-friendly upper-body strength exercise."
        }
    ],

    "Maintain weight": [

        {
            "name": "Brisk Walking",
            "duration": "25–30 minutes",
            "description":
                "Keeps daily movement consistent and supports cardiovascular fitness."
        },

        {
            "name": "Bodyweight Squats",
            "duration": "3 × 12 reps",
            "description":
                "Maintains lower-body strength."
        },

        {
            "name": "Plank",
            "duration": "3 × 20–40 seconds",
            "description":
                "Strengthens the core and improves trunk stability."
        }
    ],

    "Build strength & fitness": [

        {
            "name": "Bodyweight Squats",
            "duration": "3 × 10–15 reps",
            "description":
                "Builds lower-body strength."
        },

        {
            "name": "Incline Push-Ups",
            "duration": "3 × 8–12 reps",
            "description":
                "Develops upper-body pushing strength."
        },

        {
            "name": "Plank",
            "duration": "3 × 20–40 seconds",
            "description":
                "Builds core stability."
        }
    ],

    "Improve body composition": [

        {
            "name": "Squats",
            "duration": "3 × 10–15 reps",
            "description":
                "Supports lower-body strength and muscle development."
        },

        {
            "name": "Incline Push-Ups",
            "duration": "3 × 8–12 reps",
            "description":
                "Strengthens the chest, shoulders and arms."
        },

        {
            "name": "Brisk Walking",
            "duration": "25–40 minutes",
            "description":
                "Adds regular cardiovascular activity."
        }
    ]
}


SPECIFIC_EXERCISES = {

    "Belly area": [

        {
            "name": "Dead Bug",
            "duration": "3 × 8–12 each side",
            "description":
                "Strengthens the core and improves trunk control."
        },

        {
            "name": "Plank",
            "duration": "3 × 20–40 seconds",
            "description":
                "Develops core stability."
        },

        {
            "name": "Bird Dog",
            "duration": "3 × 8–12 each side",
            "description":
                "Improves core stability and coordination."
        }
    ],

    "Double chin": [

        {
            "name": "Brisk Walking",
            "duration": "25–40 minutes",
            "description":
                "Supports overall physical activity and energy expenditure."
        },

        {
            "name": "Chin Tucks",
            "duration": "2 × 10–15 reps",
            "description":
                "A posture exercise for the neck and chin area."
        },

        {
            "name": "Posture Practice",
            "duration": "5 minutes daily",
            "description":
                "Improves neck and upper-body posture."
        }
    ],

    "Arms": [

        {
            "name": "Wall Push-Ups",
            "duration": "3 × 10–15 reps",
            "description":
                "Beginner-friendly upper-body strengthening."
        },

        {
            "name": "Incline Push-Ups",
            "duration": "3 × 8–12 reps",
            "description":
                "Progresses upper-body pushing strength."
        },

        {
            "name": "Triceps Extensions",
            "duration": "3 × 10–15 reps",
            "description":
                "Targets the triceps."
        }
    ],

    "Thighs": [

        {
            "name": "Bodyweight Squats",
            "duration": "3 × 10–15 reps",
            "description":
                "Strengthens the thighs and glutes."
        },

        {
            "name": "Reverse Lunges",
            "duration": "3 × 8–10 each leg",
            "description":
                "Develops single-leg strength."
        },

        {
            "name": "Step-Ups",
            "duration": "3 × 10 each leg",
            "description":
                "Builds lower-body strength."
        }
    ],

    "Glutes": [

        {
            "name": "Glute Bridges",
            "duration": "3 × 12–15 reps",
            "description":
                "Strengthens the glutes."
        },

        {
            "name": "Squats",
            "duration": "3 × 10–15 reps",
            "description":
                "Works the glutes and legs."
        },

        {
            "name": "Reverse Lunges",
            "duration": "3 × 8–10 each leg",
            "description":
                "Strengthens the glutes and legs."
        }
    ],

    "Back": [

        {
            "name": "Bird Dog",
            "duration": "3 × 8–12 each side",
            "description":
                "Builds core and posterior-chain stability."
        },

        {
            "name": "Wall Angels",
            "duration": "2 × 10 reps",
            "description":
                "Encourages better upper-body posture."
        },

        {
            "name": "Resistance-Band Rows",
            "duration": "3 × 10–15 reps",
            "description":
                "Strengthens the upper back."
        }
    ],

    "Overall fitness": [

        {
            "name": "Brisk Walking",
            "duration": "25–40 minutes",
            "description":
                "Simple cardiovascular exercise."
        },

        {
            "name": "Squats",
            "duration": "3 × 12 reps",
            "description":
                "Builds lower-body strength."
        },

        {
            "name": "Plank",
            "duration": "3 × 20–40 seconds",
            "description":
                "Improves core stability."
        }
    ]
}


def get_exercises(goal, specific_area=None):

    if specific_area and specific_area in SPECIFIC_EXERCISES:
        return SPECIFIC_EXERCISES[specific_area]

    return EXERCISES.get(
        goal,
        EXERCISES["Maintain weight"]
    )


# ============================================================
# VIDEO RECOMMENDATIONS
# ============================================================

VIDEOS = [

    {
        "title": "NHS – Working your abs",
        "source": "NHS",
        "video_id": "06SW69PYAXI",
        "description":
            "A short guided abdominal workout."
    },

    {
        "title": "NHS – Bum workout",
        "source": "NHS",
        "video_id": "Cbo_4hV6Zs4",
        "description":
            "A short guided lower-body workout."
    }
]


def get_videos():
    return VIDEOS