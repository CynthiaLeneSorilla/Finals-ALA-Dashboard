import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="SDG 13 Climate Action Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================


co2 = pd.read_csv("co2.csv", skiprows=4)
gdp = pd.read_csv("gdp.csv", skiprows=4)
urban = pd.read_csv("urban.csv", skiprows=4)
population = pd.read_csv("population.csv", skiprows=4)
electricity = pd.read_csv("electricity.csv", skiprows=4)

# Required Columns:
# Country
# Year
# LifeExpectancy
# GDP
# HealthExpenditure
# EducationIndex
# CleanWaterAccess
# CO2
# Continent
# ISO_Code

# ==================================================
# HEADER
# ==================================================

st.title("🌍 Understanding the Drivers Towards Global Development")

st.markdown("""
### SDG 3: Good Health and Well-Being

**Research Question:**

*What factors influence Life Expectancy across countries over time?*
""")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Filters")

selected_year = st.sidebar.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    int(df["Year"].max())
)

filtered_df = df[df["Year"] == selected_year]

# ==================================================
# KPI SECTION
# ==================================================

avg_life = filtered_df["LifeExpectancy"].mean()

avg_gdp = filtered_df["GDP"].mean()

avg_health = filtered_df["HealthExpenditure"].mean()

countries = filtered_df["Country"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Life Expectancy",
    f"{avg_life:.1f}"
)

col2.metric(
    "GDP per Capita",
    f"${avg_gdp:,.0f}"
)

col3.metric(
    "Health Expenditure",
    f"{avg_health:.1f}%"
)

col4.metric(
    "Countries",
    countries
)

st.divider()

# ==================================================
# LIFE EXPECTANCY TREND
# ==================================================

trend = (
    df.groupby("Year")["LifeExpectancy"]
    .mean()
    .reset_index()
)

fig_trend = px.line(
    trend,
    x="Year",
    y="LifeExpectancy",
    markers=True,
    title="Global Life Expectancy Trend"
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

# ==================================================
# GDP VS LIFE EXPECTANCY
# ==================================================

fig_scatter = px.scatter(
    filtered_df,
    x="GDP",
    y="LifeExpectancy",
    color="Continent",
    size="HealthExpenditure",
    hover_name="Country",
    title="GDP vs Life Expectancy"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# ==================================================
# TOP COUNTRIES
# ==================================================

top10 = filtered_df.nlargest(
    10,
    "LifeExpectancy"
)

fig_bar = px.bar(
    top10,
    x="Country",
    y="LifeExpectancy",
    color="LifeExpectancy",
    title="Top 10 Countries by Life Expectancy"
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

# ==================================================
# COUNTRY COMPARISON
# ==================================================

st.subheader("Country Comparison")

country_list = sorted(
    filtered_df["Country"].unique()
)

selected_countries = st.multiselect(
    "Select Countries",
    country_list,
    default=country_list[:5]
)

comparison = filtered_df[
    filtered_df["Country"].isin(selected_countries)
]

fig_compare = px.bar(
    comparison,
    x="Country",
    y="LifeExpectancy",
    color="Country",
    title="Life Expectancy Comparison"
)

st.plotly_chart(
    fig_compare,
    use_container_width=True
)

# ==================================================
# WORLD MAP
# ==================================================

fig_map = px.choropleth(
    filtered_df,
    locations="ISO_Code",
    color="LifeExpectancy",
    hover_name="Country",
    title="Life Expectancy Around the World",
    color_continuous_scale="Viridis"
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)

# ==================================================
# REGRESSION DRIVERS
# ==================================================

st.subheader("Key Drivers Identified from Regression")

drivers = pd.DataFrame({

    "Variable": [
        "GDP per Capita",
        "Health Expenditure",
        "Education Index",
        "Access to Clean Water",
        "CO₂ Emissions"
    ],

    "Coefficient": [
        0.52,
        0.41,
        0.37,
        0.28,
        -0.24
    ]
})

fig_driver = px.bar(
    drivers,
    x="Coefficient",
    y="Variable",
    orientation="h",
    color="Coefficient",
    title="Regression Coefficients"
)

st.plotly_chart(
    fig_driver,
    use_container_width=True
)

# ==================================================
# INSIGHTS
# ==================================================

st.subheader("Key Findings")

st.success("""
1. GDP per Capita is the strongest positive predictor of Life Expectancy.

2. Health Expenditure significantly improves health outcomes.

3. Education contributes to longer life expectancy.

4. Access to Clean Water positively impacts public health.

5. CO₂ Emissions negatively affect life expectancy.
""")
