import os
import sqlite3
import hashlib
import secrets
import streamlit as st


# =========================================================
# DATABASE
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "users.db")


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


# =========================================================
# PASSWORD
# =========================================================

def hash_password(password, salt=None):

    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()

    return password_hash, salt


def verify_password(password, stored_hash, salt):

    password_hash, _ = hash_password(password, salt)

    return secrets.compare_digest(
        password_hash,
        stored_hash
    )


# =========================================================
# REGISTER
# =========================================================

def register_user(name, email, password):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:

        password_hash, salt = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password_hash, salt)
            VALUES (?, ?, ?, ?)
            """,
            (
                name.strip(),
                email.strip().lower(),
                password_hash,
                salt
            )
        )

        conn.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "An account with this email already exists."

    finally:

        conn.close()


# =========================================================
# LOGIN
# =========================================================

def login_user(email, password):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, email, password_hash, salt
        FROM users
        WHERE email = ?
        """,
        (email.strip().lower(),)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return None

    user_id, name, email, stored_hash, salt = user

    if verify_password(password, stored_hash, salt):

        return {
            "id": user_id,
            "name": name,
            "email": email
        }

    return None


# =========================================================
# AUTH PAGE
# =========================================================

def show_auth():

    init_db()

    # -----------------------------------------------------
    # SESSION
    # -----------------------------------------------------

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "auth_user" not in st.session_state:
        st.session_state.auth_user = None

    # -----------------------------------------------------
    # AUTH CSS
    # -----------------------------------------------------

    st.markdown(
        """
        <style>

        /* ================================================
           PAGE
        ================================================ */

        .stApp {
            background:
                radial-gradient(
                    circle at top,
                    #F3FBF7 0%,
                    #EAF7F0 45%,
                    #F7FBF9 100%
                ) !important;
        }

        .main .block-container {
            max-width: 500px !important;
            padding-top: 45px !important;
            padding-bottom: 35px !important;
        }


        /* ================================================
           BRAND
        ================================================ */

        .auth-brand {
            text-align: center;
            margin-bottom: 25px;
        }

        .auth-logo {
            width: 68px;
            height: 68px;

            margin: 0 auto 13px auto;

            border-radius: 20px;

            background: linear-gradient(
                135deg,
                #159A72,
                #0E7657
            );

            display: flex;
            align-items: center;
            justify-content: center;

            color: white;
            font-size: 31px;

            box-shadow:
                0 12px 28px rgba(21,154,114,0.20);
        }

        .auth-brand-title {
            color: #173B32 !important;
            font-size: 28px !important;
            font-weight: 800 !important;
            margin: 0 !important;
        }

        .auth-brand-subtitle {
            color: #657770 !important;
            font-size: 13px !important;
            margin-top: 4px !important;
        }


        /* ================================================
           TABS
        ================================================ */

        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background: #FFFFFF !important;
            border: 1px solid #DCEBE3 !important;
            border-radius: 14px !important;
            padding: 4px !important;
            justify-content: center;
            border-bottom: 1px solid #DCEBE3 !important;
        }

        .stTabs [data-baseweb="tab"] {
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            font-weight: 600 !important;
            padding: 8px 16px !important;
            border-radius: 10px !important;
            border: none !important;
            background: transparent !important;
            transition: all 0.2s ease !important;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: #DDF3E8 !important;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #159A72 0%, #0E7657 100%) !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 12px rgba(21, 154, 114, 0.25) !important;
        }

        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }


        /* ================================================
           CARD
        ================================================ */

        .auth-card {
            background: #FFFFFF;
            border: 1px solid #DCEBE3;
            border-radius: 20px;
            padding: 24px 25px;
            margin-top: 15px;
            margin-bottom: 18px;
            box-shadow: 0 8px 24px rgba(21, 154, 114, 0.08);
        }

        .auth-heading {
            color: #173B32 !important;
            font-size: 21px !important;
            font-weight: 750 !important;
            margin-bottom: 5px !important;
        }

        .auth-description {
            color: #657770 !important;
            font-size: 13px !important;
            line-height: 1.5 !important;
        }


        /* ================================================
           INPUTS
        ================================================ */

        .stTextInput label {
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            font-weight: 600 !important;
        }

        .stTextInput input {
            background: #FFFFFF !important;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            border: 1.5px solid #DCEBE3 !important;
            border-radius: 12px !important;
            min-height: 44px !important;
            padding: 0.65rem 0.95rem !important;
        }

        .stTextInput input:focus {
            border-color: #159A72 !important;
            box-shadow: 0 0 0 3px rgba(21, 154, 114, 0.16) !important;
        }

        .stTextInput input::placeholder {
            color: #8A9B95 !important;
        }


        /* ================================================
           BUTTON
        ================================================ */

        .stButton > button {
            background: linear-gradient(135deg, #159A72 0%, #0E7657 100%) !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            min-height: 44px !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 14px rgba(21, 154, 114, 0.25) !important;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #0E7657 0%, #09533D 100%) !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            transform: translateY(-1.5px);
            box-shadow: 0 6px 18px rgba(21, 154, 114, 0.32) !important;
        }


        /* ================================================
           ALERTS
        ================================================ */

        .stAlert {
            border-radius: 10px !important;
        }


        /* ================================================
           FOOTER
        ================================================ */

        .auth-footer {
            text-align: center;

            color: #7D928A !important;

            font-size: 11px !important;

            margin-top: 25px;
        }


        /* ================================================
           MOBILE
        ================================================ */

        @media (max-width: 600px) {

            .main .block-container {
                padding: 25px 18px 30px 18px !important;
            }

            .auth-brand-title {
                font-size: 25px !important;
            }

            .auth-logo {
                width: 60px;
                height: 60px;
                font-size: 27px;
            }

            .auth-card {
                padding: 20px 18px;
                border-radius: 17px;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 9px 11px !important;
                font-size: 13px !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # BRAND
    # =====================================================

    st.markdown(
        '<div class="auth-brand">'
        '<div class="auth-logo">🌿</div>'
        '<div class="auth-brand-title">FoodGuard AI</div>'
        '<div class="auth-brand-subtitle">'
        'Smart food & nutrition assistant'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # =====================================================
    # TABS
    # =====================================================

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "✨ Create Account"
        ]
    )

    # =====================================================
    # LOGIN
    # =====================================================

    with login_tab:

        st.markdown(
            '<div class="auth-card">'
            '<div class="auth-heading">Welcome back 👋</div>'
            '<div class="auth-description">'
            'Login to continue using FoodGuard AI.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        st.write("")

        if st.button(
            "Login",
            type="primary",
            use_container_width=True,
            key="login_button"
        ):

            if not email or not password:

                st.error(
                    "Please enter your email and password."
                )

            else:

                user = login_user(
                    email,
                    password
                )

                if user:

                    st.session_state.authenticated = True
                    st.session_state.auth_user = user

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password."
                    )

        st.markdown(
            '<div style="text-align:center;margin:14px 0 8px;color:#657770;font-size:0.8rem;font-weight:600;">'
            '— OR INSTANT DEMO ACCESS —'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "🚀 Demo Login (Instant Access)",
            use_container_width=True,
            key="demo_login_button"
        ):
            st.session_state.authenticated = True
            st.session_state.auth_user = {
                "id": 1,
                "name": "Yash",
                "email": "test@foodguard.ai"
            }
            st.rerun()

    # =====================================================
    # REGISTER
    # =====================================================

    with register_tab:

        st.markdown(
            '<div class="auth-card">'
            '<div class="auth-heading">'
            'Create your account 🌱'
            '</div>'
            '<div class="auth-description">'
            'Start tracking your food and nutrition.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        name = st.text_input(
            "Full Name",
            placeholder="Enter your name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="register_confirm_password"
        )

        st.write("")

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True,
            key="register_button"
        ):

            if not name or not email or not password:

                st.error(
                    "Please fill in all required fields."
                )

            elif len(password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                success, message = register_user(
                    name,
                    email,
                    password
                )

                if success:

                    st.success(
                        "Account created successfully! "
                        "You can now login."
                    )

                else:

                    st.error(message)

    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown(
        '<div class="auth-footer">'
        'FoodGuard AI • Smart Food & Nutrition Assistant'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# LOGOUT
# =========================================================

def logout():

    st.session_state.authenticated = False
    st.session_state.auth_user = None

    st.rerun()