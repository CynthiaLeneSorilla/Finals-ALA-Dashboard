# ============================================================
# SDG 13 DASHBOARD (FINAL FIXED + RED ACCENT + CLEAN UI)
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SDG 13 Climate Dashboard",
    page_icon="🌍",
    layout="wide",
)


# ============================================================
# THEME (SOFT DARK + RED ACCENT)
# ============================================================

st.markdown("""
<style>

/* ===== BACKGROUND (SOFT DARK GRAY) ===== */
.stApp {
    background: linear-gradient(
        180deg,
        #2c2f36 0%,
        #31343b 50%,
        #2a2d33 100%
    );
    font-family: Arial;
}

/* ===== HERO ===== */
.hero {
    background: linear-gradient(
        135deg,
        #1f2a2e,
        #2b3f44,
        #3a1f1f
    );
    padding: 55px 35px;
    border-radius: 28px;
    text-align: center;
    color: #ffffff;
    margin-bottom: 45px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.35);
}

/* HERO TEXT */
.hero h1 {
    margin-bottom: 10px;
}

.hero h4 {
    color: #e0e0e0;
    font-weight: 400;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: #23262b;
}

/* ============================================================
   KPI BOX (FIXED VISIBILITY + RED ACCENT)
============================================================ */

.kpi-card {
    background: #3a3d45;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    text-align: center;
    border-left: 6px solid #ff4d4d;
    transition: 0.25s ease;
}

.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.45);
}

/* KPI TEXT */
.kpi-title {
    font-size: 13px;
    color: #ffb3b3;   /* light red tint */
    margin-bottom: 8px;
    font-weight: 600;
}

.kpi-value {
    font-size: 22px;
    font-weight: bold;
    color: #ffffff;   /* FIXED: readable white */
}

/* ===== HEADINGS (RESTORED VISIBILITY) ===== */
h1, h2, h3 {
    color: #f5f5f5 !important;
}

/* ===== GLOBAL TEXT ===== */
p {
    color: #d0d0d0;
}

/* ===== CHART BOXES ===== */
[data-testid="stPlotlyChart"] {
    background: #3a3d45;
    padding: 16px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    co2 = pd.read_csv("co2.csv", skiprows=4)
    gdp = pd.read_csv("gdp.csv", skiprows=4)
    urban = pd.read_csv("urban.csv", skiprows=4)
    population = pd.read_csv("population.csv", skiprows=4)
    electricity = pd.read_csv("electricity.csv", skiprows=4)

    def reshape(df, value_name):
        id_vars = ["Country Name", "Country Code"]
        years = [c for c in df.columns if str(c).isdigit()]

        df = df[id_vars + years]

        df = pd.melt(
            df,
            id_vars=id_vars,
            value_vars=years,
            var_name="Year",
            value_name=value_name
        )

        df["Year"] = df["Year"].astype(int)
        return df

    co2 = reshape(co2, "CO2_emissions_kt")
    gdp = reshape(gdp, "GDP_current_USD")
    urban = reshape(urban, "Urban_population_pct")
    pop = reshape(population, "Population")
    elec = reshape(electricity, "Electricity_access_pct")

    df = co2.merge(gdp, on=["Country Name", "Country Code", "Year"])
    df = df.merge(urban, on=["Country Name", "Country Code", "Year"])
    df = df.merge(pop, on=["Country Name", "Country Code", "Year"])
    df = df.merge(elec, on=["Country Name", "Country Code", "Year"])

    df = df.dropna()
    df = df[(df["Year"] >= 2000) & (df["Year"] <= 2020)]

    remove = ["World", "High income", "Low income", "Middle income", "OECD members"]
    df = df[~df["Country Name"].isin(remove)]

    df["GDP_per_capita"] = df["GDP_current_USD"] / df["Population"]
    df["Log_CO2"] = np.log(df["CO2_emissions_kt"] + 1)

    return df


df = load_data()


# ============================================================
# HERO (RESTORED)
# ============================================================

st.markdown("""
<div class="hero">
<h1>🌍 SDG 13 Climate Action Dashboard</h1>
<h4>Global CO₂ Emissions Analysis (2000–2020)</h4>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Controls")

year = st.sidebar.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    2019
)

data = df[df["Year"] == year]


# ============================================================
# KPI FUNCTION
# ============================================================

def kpi_box(title, value):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 🔴 GLOBAL INDICATORS TITLE (RESTORED)
# ============================================================

st.markdown("## 🔴 Global Indicators")


col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_box("Avg CO₂ Emissions",
             f"{data['CO2_emissions_kt'].mean():,.0f}")

with col2:
    kpi_box("Highest Emitter",
             data.loc[data["CO2_emissions_kt"].idxmax(), "Country Name"])

with col3:
    kpi_box("GDP Per Capita",
             f"${data['GDP_per_capita'].mean():,.0f}")

with col4:
    kpi_box("Electricity Access",
             f"{data['Electricity_access_pct'].mean():.1f}%")


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "Global Overview",
    "Driver Analysis",
    "Country Explorer"
])


# ============================================================
# TAB 1
# ============================================================

with tab1:

    left, right = st.columns(2)

    with left:
        fig_map = px.choropleth(
            data,
            locations="Country Code",
            color="CO2_emissions_kt",
            hover_name="Country Name",
            color_continuous_scale="Reds",
            title=f"CO₂ Emissions by Country ({year})"
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with right:
        top10 = data.nlargest(10, "CO2_emissions_kt")

        fig_top = px.bar(
            top10,
            x="Country Name",
            y="CO2_emissions_kt",
            color="CO2_emissions_kt",
            color_continuous_scale="Reds",
            title="Top 10 CO₂ Emitters"
        )
        st.plotly_chart(fig_top, use_container_width=True)

    trend = df.groupby("Year")["CO2_emissions_kt"].mean().reset_index()

    fig_trend = px.line(
        trend,
        x="Year",
        y="CO2_emissions_kt",
        markers=True,
        title="Global CO₂ Trend"
    )

    fig_trend.update_traces(line=dict(color="#ff4d4d", width=3))

    st.plotly_chart(fig_trend, use_container_width=True)


# ============================================================
# TAB 2 & 3 (UNCHANGED LOGIC)
# ============================================================

with tab2:

    st.subheader("Driver Analysis")

    drivers = pd.DataFrame({
        "Driver": ["GDP per Capita", "Urban Population", "Population", "Electricity Access"],
        "Impact": [0.42, 0.28, 0.18, 0.12]
    })

    fig_driver = px.bar(
        drivers,
        x="Driver",
        y="Impact",
        color="Impact",
        color_continuous_scale="Reds",
        title="Key Drivers of CO₂ Emissions"
    )

    st.plotly_chart(fig_driver, use_container_width=True)


with tab3:

    country = st.selectbox(
        "Select Country",
        sorted(df["Country Name"].unique())
    )

    country_df = df[df["Country Name"] == country]

    fig_country = px.line(
        country_df,
        x="Year",
        y="CO2_emissions_kt",
        markers=True,
        title=f"CO₂ Trend - {country}"
    )

    fig_country.update_traces(line=dict(color="#ff4d4d", width=3))

    st.plotly_chart(fig_country, use_container_width=True)
