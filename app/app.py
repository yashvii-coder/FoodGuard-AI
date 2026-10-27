import streamlit as st

from components.ui import inject_css, app_header
from views.scan_food import show_scan_food
from views.packaged_food import show_packaged_food
from views.manual_log import show_manual_log
from views.daily_diary import show_daily_diary
from views.profile import show_profile
from views.coach import show_coach
from auth import show_auth


st.set_page_config(
    page_title="FoodGuard AI",
    page_icon="🍎",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# =========================================================
# GLOBAL UI & STYLES
# =========================================================

inject_css()


# =========================================================
# AUTHENTICATION
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    show_auth()
    st.stop()


app_header()


# =========================================================
# NAVIGATION
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "🍎 Scan Food",
        "📦 Packaged Food",
        "✏️ Manual Log",
        "📖 Daily Diary",
        "👤 Profile",
        "✨ My Coach",
    ]
)


# IMPORTANT:
# Each page owns its own heading/description.
# Do not add duplicate page headings here.

with tab1:
    show_scan_food()

with tab2:
    show_packaged_food()

with tab3:
    show_manual_log()

with tab4:
    show_daily_diary()

with tab5:
    show_profile()

with tab6:
    show_coach()


st.markdown(
    '<div class="footer">FoodGuard AI &nbsp;•&nbsp; Smart Food &amp; Nutrition Assistant</div>',
    unsafe_allow_html=True,
)
