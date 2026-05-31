import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ======================================================
# PAGE SETTINGS
# ======================================================

st.set_page_config(
    page_title="SDG Dashboard",
    layout="wide"
)

st.title("🌍 Understanding the Drivers Towards Global Development")

st.markdown("""
### SDG 7: Affordable and Clean Energy

**Research Question**

What factors influence access to electricity across countries over time?
""")

# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():

    co2 = pd.read_csv("co2.csv", skiprows=4)
    gdp = pd.read_csv("gdp.csv", skiprows=4)
    urban = pd.read_csv("urban.csv", skiprows=4)
    population = pd.read_csv("population.csv", skiprows=4)
    electricity = pd.read_csv("electricity.csv", skiprows=4)

    return co2, gdp, urban, population, electricity

co2, gdp, urban, population, electricity = load_data()

# ======================================================
# YEAR SELECTION
# ======================================================

years = [str(y) for y in range(2000, 2024)]

selected_year = st.sidebar.selectbox(
    "Select Year",
    years,
    index=len(years)-1
)

# ======================================================
# CLEAN FUNCTION
# ======================================================

def prepare(df, value_name):

    temp = df[[
        "Country Name",
        "Country Code",
        selected_year
    ]].copy()

    temp.columns = [
        "Country",
        "Code",
        value_name
    ]

    return temp

# ======================================================
# PREPARE DATA
# ======================================================

co2_df = prepare(co2, "CO2")
gdp_df = prepare(gdp, "GDP")
urban_df = prepare(urban, "Urban")
pop_df = prepare(population, "Population")
electric_df = prepare(electricity, "Electricity")

# ======================================================
# MERGE
# ======================================================

df = electric_df.merge(
    gdp_df,
    on=["Country","Code"]
)

df = df.merge(
    co2_df,
    on=["Country","Code"]
)

df = df.merge(
    urban_df,
    on=["Country","Code"]
)

df = df.merge(
    pop_df,
    on=["Country","Code"]
)

df = df.dropna()

# ======================================================
# KPI SECTION
# ======================================================

st.subheader(f"Global Indicators ({selected_year})")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Electricity Access",
    f"{df['Electricity'].mean():.1f}%"
)

col2.metric(
    "Average GDP",
    f"${df['GDP'].mean():,.0f}"
)

col3.metric(
    "Average CO₂",
    f"{df['CO2'].mean():.2f}"
)

col4.metric(
    "Countries",
    df["Country"].nunique()
)

# ======================================================
# ELECTRICITY ACCESS MAP
# ======================================================

st.subheader("Electricity Access by Country")

fig_map = px.choropleth(
    df,
    locations="Code",
    color="Electricity",
    hover_name="Country",
    color_continuous_scale="Viridis"
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)

# ======================================================
# GDP VS ELECTRICITY
# ======================================================

st.subheader("GDP vs Electricity Access")

fig_scatter = px.scatter(
    df,
    x="GDP",
    y="Electricity",
    color="CO2",
    hover_name="Country",
    size="Population"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# ======================================================
# TOP COUNTRIES
# ======================================================

st.subheader("Top 15 Countries by Electricity Access")

top15 = df.nlargest(
    15,
    "Electricity"
)

fig_bar = px.bar(
    top15,
    x="Country",
    y="Electricity",
    color="Electricity"
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

# ======================================================
# COUNTRY COMPARISON
# ======================================================

st.subheader("Country Comparison")

countries = sorted(
    df["Country"].unique()
)

selected_countries = st.multiselect(
    "Select Countries",
    countries,
    default=countries[:5]
)

compare = df[
    df["Country"].isin(selected_countries)
]

fig_compare = px.bar(
    compare,
    x="Country",
    y="Electricity",
    color="Country"
)

st.plotly_chart(
    fig_compare,
    use_container_width=True
)

# ======================================================
# DRIVER ANALYSIS
# ======================================================

st.subheader("Potential Drivers of Electricity Access")

corr_df = df[[
    "Electricity",
    "GDP",
    "CO2",
    "Urban",
    "Population"
]]

corr = corr_df.corr()

fig_heat = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="RdBu"
)

st.plotly_chart(
    fig_heat,
    use_container_width=True
)

# ======================================================
# INSIGHTS
# ======================================================

st.subheader("Key Findings")

st.info(
"""
• Countries with higher GDP generally have better electricity access.

• Urbanization is positively associated with electricity coverage.

• Population size alone does not guarantee access to electricity.

• CO₂ emissions tend to increase with industrialization and energy use.

• These variables can be tested further through multiple regression analysis
to determine which factors significantly influence electricity access.
"""
)

# ======================================================
# DATA TABLE
# ======================================================

st.subheader("Merged Dataset")

st.dataframe(df)
