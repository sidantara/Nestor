import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# --- Load and Prepare Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("combined_data_final.csv", parse_dates=["Date"])
        # Simulate Healthcare Access (1–10) if missing
    if "HealthcareAccess" not in df.columns:
        np.random.seed(42)  # For reproducibility
        df["HealthcareAccess"] = np.random.uniform(1, 10, size=len(df)).round(1)
    
    # Calculate CrimeRate from component crimes
    df["CrimeRateRaw"] = df[["Murder", "Assault", "Rape"]].sum(axis=1)

    # Normalize CrimeRate and SchoolRating to scale 1–10
    scaler = MinMaxScaler(feature_range=(1, 10))
    df["CrimeRate"] = scaler.fit_transform(df[["CrimeRateRaw"]])
    df["SchoolRating"] = scaler.fit_transform(df[["SchoolRating"]])

    return df

data = load_data()

# --- Sidebar: Filter Mode Selection ---
st.sidebar.header("Your Preferences")
filter_mode = st.sidebar.radio("Filter by:", ["Budget", "Bedrooms", "Crime Rate", "Healthcare Access"])

# --- Sidebar: Dynamic Filters ---
if filter_mode == "Budget":
    min_price = st.sidebar.number_input("Min Budget ($)", value=100000)
    max_price = st.sidebar.number_input("Max Budget ($)", value=800000)
    school_rating = st.sidebar.slider("Minimum School Rating (1–10)", 1.0, 10.0, 7.0)

    filtered = data[
        (data["HomePrice"] >= min_price) &
        (data["HomePrice"] <= max_price) &
        (data["SchoolRating"] >= school_rating)
    ]
    display_cols = ["RegionName", "Date", "HomePrice", "SchoolRating", "CrimeRate", "DesirabilityScore"]

elif filter_mode == "Bedrooms":
    bedrooms = st.sidebar.slider("Preferred # of Bedrooms", 1, 5, 3)
    school_rating = st.sidebar.slider("Minimum School Rating (1–10)", 1.0, 10.0, 7.0)

    if "Bedrooms" in data.columns:
        filtered = data[
            (data["Bedrooms"] == bedrooms) &
            (data["SchoolRating"] >= school_rating)
        ]
        display_cols = ["RegionName", "Date", "Bedrooms", "SchoolRating", "CrimeRate", "DesirabilityScore"]
    else:
        st.warning("⚠️ 'Bedrooms' data not available.")
        filtered = data[0:0]
        display_cols = []

elif filter_mode == "Crime Rate":
    max_crime = st.sidebar.slider("Max Acceptable Crime Rate (1–10)", 1.0, 10.0, 5.0)
    school_rating = st.sidebar.slider("Minimum School Rating (1–10)", 1.0, 10.0, 7.0)

    filtered = data[
        (data["CrimeRate"] <= max_crime) &
        (data["SchoolRating"] >= school_rating)
    ]
    display_cols = ["RegionName", "Date", "CrimeRate", "SchoolRating", "DesirabilityScore"]

elif filter_mode == "Healthcare Access":
    min_healthcare = st.sidebar.slider("Minimum Healthcare Access (1–10)", 1.0, 10.0, 7.0)
    school_rating = st.sidebar.slider("Minimum School Rating (1–10)", 1.0, 10.0, 7.0)

    if "HealthcareAccess" in data.columns:
        filtered = data[
            (data["HealthcareAccess"] >= min_healthcare) &
            (data["SchoolRating"] >= school_rating)
        ]
        display_cols = ["RegionName", "Date", "HealthcareAccess", "SchoolRating", "CrimeRate", "DesirabilityScore"]
    else:
        st.warning("⚠️ 'HealthcareAccess' data not available.")
        filtered = data[0:0]
        display_cols = []

# --- Main Content ---
st.title(" Nestor: Smart Home State Recommendations")
st.markdown("### Best States to Consider Based on Economic & Housing Metrics")

# Top pick
if not filtered.empty:
    top_row = filtered.sort_values("DesirabilityScore", ascending=False).iloc[0]
    st.success(f" **Top Pick: {top_row['RegionName']}** — Score: {top_row['DesirabilityScore']:.3f}")

# Result table
st.markdown(f"### {len(filtered)} Matching Results")
if display_cols:
    st.dataframe(filtered.sort_values("DesirabilityScore", ascending=False)[display_cols])

# Bar chart: Top 5 by Desirability
if not filtered.empty and "RegionName" in filtered.columns:
    top5 = filtered.sort_values("DesirabilityScore", ascending=False).head(5)
    st.markdown("### Top Region(s) by Desirability Score")
    st.bar_chart(top5.set_index("RegionName")["DesirabilityScore"])

# Line chart: Price Trends Over Time for Top Regions
if not filtered.empty and "RegionName" in filtered.columns:
    top5_regions = top5["RegionName"].unique()
    trend_data = data[data["RegionName"].isin(top5_regions)]

    st.markdown("### 📈 Price Trends Over Time for Top Regions")
    st.line_chart(
        trend_data.pivot_table(index="Date", columns="RegionName", values="HomePrice")
    )


# Download results
if not filtered.empty:
    st.download_button(
        label="📥 Download Results as CSV",
        data=filtered.to_csv(index=False),
        file_name="nestor_recommendations.csv",
        mime="text/csv"
    )
with st.expander("About the Desirability Score"):
    st.markdown("""
    The Desirability Score is a composite of:
    - Home affordability
    - Unemployment rate
    - Job growth
    - School quality
    - Crime rate (lower is better)
    - Healthcare access (simulated for demonstration)
    
    Data sources include HUD, FBI, FRED, and public housing statistics.
    """)
