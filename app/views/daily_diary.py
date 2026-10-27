from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st


LOG_PATH = Path("data/food_log.csv")


def show_daily_diary():
    st.markdown(
        '<div class="section-heading">📊 Daily Diary</div>'
        '<div class="section-description">Your food entries and nutrition totals for the selected day.</div>',
        unsafe_allow_html=True,
    )

    if not LOG_PATH.exists():
        st.info("No food entries yet. Add something from Scan Food, Packaged Food, or Manual Log.")
        return

    try:
        df = pd.read_csv(LOG_PATH)
    except Exception as error:
        st.error(f"Could not load diary: {error}")
        return

    if df.empty:
        st.info("Your food diary is empty.")
        return

    if "date" not in df.columns:
        st.error("The food log does not contain a date column.")
        return

    df["date"] = df["date"].astype(str)

    selected = st.date_input("Date", value=date.today(), key="diary_date")
    day = df[df["date"] == selected.strftime("%Y-%m-%d")].copy()

    if day.empty:
        st.info("No food entries for this date.")
        return

    for column in ["calories", "protein", "carbohydrates", "fat", "fiber"]:
        if column not in day.columns:
            day[column] = 0
        day[column] = pd.to_numeric(day[column], errors="coerce").fillna(0)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔥 Calories", f"{day['calories'].sum():.0f} kcal")
    c2.metric("🥩 Protein", f"{day['protein'].sum():.1f} g")
    c3.metric("🍚 Carbs", f"{day['carbohydrates'].sum():.1f} g")
    c4.metric("🥑 Fat", f"{day['fat'].sum():.1f} g")

    st.markdown("### Today's Food")

    columns = [
        c for c in
        ["time", "food", "source", "portion", "calories",
         "protein", "carbohydrates", "fat", "fiber"]
        if c in day.columns
    ]

    show = day[columns].copy()

    if "food" in show.columns:
        show["food"] = (
            show["food"].astype(str).str.replace("_", " ", regex=False).str.title()
        )

    st.dataframe(show, hide_index=True, use_container_width=True)

    st.markdown("### 🌾 Fibre")
    st.metric("Total fibre", f"{day['fiber'].sum():.1f} g")
