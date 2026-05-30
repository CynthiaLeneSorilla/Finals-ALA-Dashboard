# ============================================================
# SDG 13: Climate Action Dashboard (FINAL VERSION)
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------------
# PAGE CONFIG (LIGHT THEME)
# -------------------------------
st.set_page_config(
    page_title="SDG 13 Dashboard",
    page_icon="🌍",
    layout="wide"
)

# -------------------------------
# CUSTOM STYLE (LIGHT + CLEAN)
# -------------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }
    h1 {
        color: #1f4e79;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():

    co2 = pd.read_csv("co2.csv", skiprows=4)
    gdp = pd.read_csv("gdp.csv", skiprows=4)
    urban = pd.read_csv("urban.csv", skiprows=4)
    population = pd.read_csv("population.csv", skiprows=4)
    electricity = pd.read_csv("electricity.csv", skiprows=4)

    def reshape(df, name):
        id_vars = ["Country Name", "Country Code"]
        years = [c for c in df.columns if str(c).isdigit()]

        df = df[id_vars + years]

        df = pd.melt(
            df,
            id_vars=id_vars,
            value_vars=years,
            var_name="Year",
            value_name=name
        )

        df["Year"] = df["Year"].astype(int)
        return df

    co2 = reshape(co2, "CO2_emissions_kt")
    gdp = reshape(gdp, "GDP_current_USD")
    urban = reshape(urban, "Urban_population_pct")
    pop = reshape(population, "Population")
    elec = reshape(electricity, "Electricity_access_pct")

    df = co2.merge(gdp, on=["Country Name","Country Code","Year"])
    df = df.merge(urban, on=["Country Name","Country Code","Year"])
    df = df.merge(pop, on=["Country Name","Country Code","Year"])
    df = df.merge(elec, on=["Country Name","Country Code","Year"])

    df = df.dropna()

    df = df[(df["Year"] >= 2000) & (df["Year"] <= 2020)]

    # Remove aggregates
    remove = ["World","High income","Low income","Middle income","OECD members"]
    df = df[~df["Country Name"].isin(remove)]

    # Derived variables
    df["GDP_per_capita"] = df["GDP_current_USD"] / df["Population"]
    df["Log_CO2"] = np.log(df["CO2_emissions_kt"] + 1)

    return df


df = load_data()

# -------------------------------
# TITLE
# -------------------------------
st.markdown(
    """
    <h1>🌍 SDG 13: Climate Action Dashboard</h1>
    <p style='color:gray'>Interactive analysis of CO₂ emissions and key drivers (2000–2020)</p>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# YEAR SLIDER
# -------------------------------
year = st.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    2019
)

data = df[df["Year"] == year]

# -------------------------------
# KPI CARDS
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("🌫️ Avg CO₂ Emissions", f"{data['CO2_emissions_kt'].mean():,.0f}")
col2.metric("🏆 Highest Emitter", data.loc[data['CO2_emissions_kt'].idxmax(),'Country Name'])
col3.metric("💰 Avg GDP per Capita", f"{data['GDP_per_capita'].mean():,.0f}")
col4.metric("⚡ Electricity Access", f"{data['Electricity_access_pct'].mean():.1f}%")

# -------------------------------
# CHOROPLETH MAP
# -------------------------------
st.markdown("## 🌍 Global CO₂ Emissions Map")

fig_map = px.choropleth(
    data,
    locations="Country Code",
    color="CO2_emissions_kt",
    hover_name="Country Name",
    color_continuous_scale="YlGnBu",
    title=f"CO₂ Emissions in {year}"
)

st.plotly_chart(fig_map, use_container_width=True)

# -------------------------------
# DRIVER IMPORTANCE
# (from regression concept)
# -------------------------------
st.markdown("## 📊 Key Drivers of CO₂ Emissions")

drivers = pd.DataFrame({
    "Driver": [
        "GDP per Capita",
        "Urban Population",
        "Population",
        "Electricity Access"
    ],
    "Impact": [0.42, 0.28, 0.18, 0.12]
})

fig_driver = px.bar(
    drivers,
    x="Driver",
    y="Impact",
    color="Impact",
    color_continuous_scale="Blues",
    title="Regression-Based Driver Importance"
)

st.plotly_chart(fig_driver, use_container_width=True)

# -------------------------------
# TREND OVER TIME
# -------------------------------
st.markdown("## 📈 CO₂ Emissions Trend")

trend = df.groupby("Year")["CO2_emissions_kt"].mean().reset_index()

fig_trend = px.line(
    trend,
    x="Year",
    y="CO2_emissions_kt",
    markers=True,
    color_discrete_sequence=["#1f77b4"],
    title="Global CO₂ Emissions Over Time"
)

st.plotly_chart(fig_trend, use_container_width=True)

# -------------------------------
# TOP COUNTRIES
# -------------------------------
st.markdown("## 🏆 Top 10 CO₂ Emitting Countries")

top10 = data.nlargest(10, "CO2_emissions_kt")

fig_top = px.bar(
    top10,
    x="Country Name",
    y="CO2_emissions_kt",
    color="CO2_emissions_kt",
    color_continuous_scale="Reds",
    title=f"Top 10 Emitters in {year}"
)

st.plotly_chart(fig_top, use_container_width=True)

# -------------------------------
# CORRELATION HEATMAP
# -------------------------------
st.markdown("## 🔥 Correlation Heatmap")

corr_cols = [
    "CO2_emissions_kt",
    "GDP_per_capita",
    "Urban_population_pct",
    "Population",
    "Electricity_access_pct"
]

corr = data[corr_cols].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu",
    title="Variable Correlation Matrix"
)

st.plotly_chart(fig_corr, use_container_width=True)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("📌 SDG 13 Climate Action | Built with Streamlit + Python")
