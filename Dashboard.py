import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==============================
# PAGE CONFIG + STYLE
# ==============================
st.set_page_config(
    page_title="SDG 13 Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }

    h1 {
        color: #4CAF50;
        text-align: center;
    }

    .stMetric {
        background-color: #1f2937;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():

    co2 = pd.read_csv("co2.csv", skiprows=4)
    gdp = pd.read_csv("gdp.csv", skiprows=4)
    urban = pd.read_csv("urban.csv", skiprows=4)
    pop = pd.read_csv("population.csv", skiprows=4)
    elec = pd.read_csv("electricity.csv", skiprows=4)

    def reshape(df, name):
        id_vars = ["Country Name", "Country Code"]
        years = [c for c in df.columns if str(c).isdigit()]

        df = df[id_vars + years]

        df = df.melt(
            id_vars=id_vars,
            value_vars=years,
            var_name="Year",
            value_name=name
        )

        df["Year"] = df["Year"].astype(int)
        return df

    co2 = reshape(co2, "CO2")
    gdp = reshape(gdp, "GDP")
    urban = reshape(urban, "Urban")
    pop = reshape(pop, "Pop")
    elec = reshape(elec, "Electricity")

    df = co2.merge(gdp, on=["Country Name","Country Code","Year"])
    df = df.merge(urban, on=["Country Name","Country Code","Year"])
    df = df.merge(pop, on=["Country Name","Country Code","Year"])
    df = df.merge(elec, on=["Country Name","Country Code","Year"])

    df = df.dropna()

    df = df[(df["Year"] >= 2000) & (df["Year"] <= 2020)]

    df["GDP_per_capita"] = df["GDP"] / df["Pop"]
    df["Log_CO2"] = np.log(df["CO2"] + 1)

    return df


df = load_data()

# ==============================
# TITLE
# ==============================
st.markdown("""
# 🌍 SDG 13: Climate Action Dashboard
### Key Drivers of CO₂ Emissions (2000–2020)
""")

# ==============================
# YEAR SLIDER
# ==============================
year = st.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    2019
)

data = df[df["Year"] == year]

# ==============================
# KPI SECTION
# ==============================
avg_co2 = data["CO2"].mean()
max_country = data.loc[data["CO2"].idxmax(), "Country Name"]
avg_gdp = data["GDP_per_capita"].mean()
avg_elec = data["Electricity"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌫 CO₂ Emissions", f"{avg_co2:,.0f}")
col2.metric("🏆 Highest Emitter", max_country)
col3.metric("💰 GDP per Capita", f"{avg_gdp:,.0f}")
col4.metric("⚡ Electricity Access", f"{avg_elec:.1f}%")

# ==============================
# CHOROPLETH MAP
# ==============================
st.markdown("## 🌎 Global CO₂ Emissions Map")

fig_map = px.choropleth(
    data,
    locations="Country Code",
    color="CO2",
    hover_name="Country Name",
    color_continuous_scale="Turbo",
    template="plotly_dark",
    title=f"CO₂ Emissions in {year}"
)

st.plotly_chart(fig_map, use_container_width=True)

# ==============================
# DRIVER IMPORTANCE (SIMPLIFIED)
# ==============================
st.markdown("## 📊 Key Drivers of CO₂ Emissions")

drivers = pd.DataFrame({
    "Driver": [
        "GDP per Capita",
        "Urbanization",
        "Population",
        "Electricity Access"
    ],
    "Impact": [0.45, 0.30, 0.15, 0.10]
})

fig_driver = px.bar(
    drivers,
    x="Driver",
    y="Impact",
    color="Impact",
    color_continuous_scale="Viridis",
    template="plotly_dark"
)

st.plotly_chart(fig_driver, use_container_width=True)

# ==============================
# TREND OVER TIME
# ==============================
st.markdown("## 📈 CO₂ Emissions Trend")

trend = df.groupby("Year")["CO2"].mean().reset_index()

fig_trend = px.line(
    trend,
    x="Year",
    y="CO2",
    markers=True,
    template="plotly_dark",
    color_discrete_sequence=["#00FFAA"]
)

st.plotly_chart(fig_trend, use_container_width=True)

# ==============================
# TOP COUNTRIES
# ==============================
st.markdown("## 🏆 Top 10 Emitters")

top10 = data.nlargest(10, "CO2")

fig_top = px.bar(
    top10,
    x="Country Name",
    y="CO2",
    color="CO2",
    template="plotly_dark",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_top, use_container_width=True)

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown("### 🌱 SDG 13 Climate Action | Built with Streamlit + Python")
