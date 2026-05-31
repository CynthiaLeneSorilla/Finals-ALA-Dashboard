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
# SOFT DARK + RED ACCENT THEME
# ============================================================

st.markdown("""
<style>

/* ===== BACKGROUND ===== */
.stApp {
    background: linear-gradient(
        180deg,
        #2b2d31 0%,
        #32353b 50%,
        #2a2c30 100%
    );
    font-family: Arial;
}

/* ===== HERO ===== */
.hero {
    background: linear-gradient(135deg, #1f2a2e, #2b3f44, #3a4f55);
    padding: 55px 35px;
    border-radius: 28px;
    text-align: center;
    color: #ffffff;
    margin-bottom: 45px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.35);
}

/* ===== HEADINGS (FIX GLOBAL TEXT VISIBILITY) ===== */
h1, h2, h3 {
    color: #f5f5f5 !important;
}

.sub-header {
    font-size: 22px;
    font-weight: 600;
    color: #f5f5f5;
    margin-bottom: 15px;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: #23262b;
}

/* ===== KPI BOX ===== */
.kpi-card {
    background: #3b3f46;   /* lighter so NOT black */
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    text-align: center;
    border-left: 6px solid #ff4d4d;   /* RED ACCENT */
    transition: 0.25s ease;
}

.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.45);
}

/* KPI TEXT */
.kpi-title {
    font-size: 13px;
    color: #cfd8dc;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 22px;
    font-weight: bold;
    color: #ffffff;
}

/* ===== CHARTS ===== */
[data-testid="stPlotlyChart"] {
    background: #3a3d44;
    padding: 16px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    margin-bottom: 25px;
}

/* ===== SELECT ===== */
.stSelectbox > div > div {
    background: #3a3d44;
    color: white;
    border-radius: 10px;
}

/* ===== SLIDER ===== */
.stSlider > div > div > div > div {
    background-color: #ff4d4d;
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
data = df[df["Year"] == 2019]


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">
<h1>🌍 SDG 13 Climate Action Dashboard</h1>
<h4>Balanced Analysis of Global CO₂ Emissions (2000–2020)</h4>
</div>
""", unsafe_allow_html=True)


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
# 🔥 GLOBAL INDICATORS (FIXED HEADER)
# ============================================================

st.markdown('<div class="sub-header">📊 Global Indicators</div>', unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_box("Avg CO₂ Emissions",
            f"{data['CO2_emissions_kt'].mean():,.0f}")

with col2:
    kpi_box("Highest Emitter (Red Alert)",
            data.loc[data["CO2_emissions_kt"].idxmax(), "Country Name"])

with col3:
    kpi_box("GDP Per Capita",
            f"${data['GDP_per_capita'].mean():,.0f}")

with col4:
    kpi_box("Electricity Access",
            f"{data['Electricity_access_pct'].mean():.1f}%")


# ============================================================
# TABS (MINIMAL DEMO)
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "Overview",
    "Drivers",
    "Country"
])


with tab1:

    st.write("Global Overview Charts here...")


with tab2:

    st.write("Driver Analysis here...")


with tab3:

    st.write("Country Explorer here...")
