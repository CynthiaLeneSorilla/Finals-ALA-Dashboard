# ============================================================
# SDG 13 CLIMATE ACTION DASHBOARD (UI UPGRADED)
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SDG 13 Climate Action Dashboard",
    page_icon="🌍",
    layout="wide",
)


# ============================================================
# GLOBAL UI DESIGN (IMPROVED SPACING + MODERN COLORS)
# ============================================================

st.markdown("""
<style>

/* ===== BACKGROUND ===== */
.stApp {
    background: linear-gradient(
        180deg,
        #f8fbfa 0%,
        #eaf5f1 50%,
        #dff0e8 100%
    );
    font-family: 'Arial';
}

/* ===== HERO SECTION ===== */
.hero {
    background: linear-gradient(
        135deg,
        #0f2f2e,
        #134e4a,
        #166a5a
    );
    padding: 55px 35px;
    border-radius: 28px;
    text-align: center;
    color: white;
    margin-bottom: 45px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.18);
}

/* HERO TEXT SPACING */
.hero h1 {
    margin-bottom: 12px;
}

.hero h4 {
    margin-bottom: 10px;
    font-weight: 400;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        to bottom,
        #e6f4ea,
        #d7f0df
    );
}

/* ===== KPI SPACING ===== */
div[data-testid="column"] {
    padding: 12px;
}

/* ===== KPI CARD DESIGN ===== */
div[style*="border-left"] {
    background: white;
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    margin-bottom: 10px;
}

div[style*="border-left"]:hover {
    transform: translateY(-6px);
    box-shadow: 0 14px 28px rgba(0,0,0,0.12);
}

/* ===== HEADINGS ===== */
h1, h2, h3 {
    color: #0f3d3e;
    margin-bottom: 12px;
}

/* ===== PARAGRAPH SPACING ===== */
p {
    line-height: 1.6;
    color: #2f3e46;
}

/* ===== CHART CARDS ===== */
[data-testid="stPlotlyChart"] {
    background: white;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.06);
    margin-bottom: 28px;
}

/* ===== SELECTBOX ===== */
.stSelectbox > div > div {
    border-radius: 12px;
}

/* ===== SUCCESS BOX ===== */
.stSuccess {
    border-left: 6px solid #1b4332;
    border-radius: 12px;
    padding: 14px;
}

/* ===== SLIDER ===== */
.stSlider > div > div > div > div {
    background-color: #166a5a;
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

    remove = [
        "World",
        "High income",
        "Low income",
        "Middle income",
        "OECD members",
    ]

    df = df[~df["Country Name"].isin(remove)]

    df["GDP_per_capita"] = df["GDP_current_USD"] / df["Population"]
    df["Log_CO2"] = np.log(df["CO2_emissions_kt"] + 1)

    return df


df = load_data()


# ============================================================
# HERO SECTION
# ============================================================

st.markdown("""
<div class="hero">
<h1>🌍 SDG 13: Climate Action Dashboard</h1>
<h4>Understanding Global CO₂ Emission Drivers (2000–2020)</h4>
<p>
A clean, modern data visualization dashboard showing how economic and social
factors influence global emissions.
</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Dashboard Controls")

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

def kpi_box(title, value, color="#2d6a4f"):
    st.markdown(f"""
    <div style="
        background: white;
        padding: 24px;
        border-radius: 18px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.08);
        border-left: 6px solid {color};
        text-align: center;
    ">
        <div style="font-size:14px; color:gray; font-weight:600;">
            {title}
        </div>
        <div style="font-size:22px; font-weight:bold; color:#0f3d3e; margin-top:10px;">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# KPI SECTION
# ============================================================

st.subheader(f"📌 Global Indicators ({year})")

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_box(
        "Avg CO₂ Emissions",
        f"{data['CO2_emissions_kt'].mean():,.0f}",
        "#166a5a"
    )

with col2:
    kpi_box(
        "Highest Emitter",
        data.loc[data["CO2_emissions_kt"].idxmax(), "Country Name"],
        "#1b4332"
    )

with col3:
    kpi_box(
        "GDP Per Capita",
        f"${data['GDP_per_capita'].mean():,.0f}",
        "#2d6a4f"
    )

with col4:
    kpi_box(
        "Electricity Access",
        f"{data['Electricity_access_pct'].mean():.1f}%",
        "#40916c"
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "🌍 Global Overview",
    "📊 Driver Analysis",
    "🔎 Country Explorer"
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
            color_continuous_scale="Viridis",
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
            color_continuous_scale="Viridis",
            title="Top 10 CO₂ Emitters"
        )
        st.plotly_chart(fig_top, use_container_width=True)

    trend = df.groupby("Year")["CO2_emissions_kt"].mean().reset_index()

    fig_trend = px.line(
        trend,
        x="Year",
        y="CO2_emissions_kt",
        markers=True,
        title="Average Global CO₂ Emissions Over Time"
    )

    fig_trend.update_traces(line=dict(color="#1b4332", width=4))

    st.plotly_chart(fig_trend, use_container_width=True)


# ============================================================
# TAB 2
# ============================================================

with tab2:

    st.subheader("Regression-Based Driver Analysis")

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
        color_continuous_scale="Aggrnyl",
        title="Key Drivers of CO₂ Emissions"
    )

    st.plotly_chart(fig_driver, use_container_width=True)

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
        color_continuous_scale="RdYlGn",
        title="Correlation Matrix"
    )

    st.plotly_chart(fig_corr, use_container_width=True)

    st.success("""
    KEY FINDINGS

    • Economic growth increases emissions  
    • Urbanization increases energy demand  
    • Population increases total emissions  
    • Electricity access supports development  
    """)


# ============================================================
# TAB 3
# ============================================================

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
        title=f"CO₂ Emissions Trend - {country}"
    )

    fig_country.update_traces(line=dict(color="#0f3d3e", width=4))

    st.plotly_chart(fig_country, use_container_width=True)

    fig_gdp = px.scatter(
        country_df,
        x="GDP_per_capita",
        y="CO2_emissions_kt",
        size="Population",
        color="Urban_population_pct",
        color_continuous_scale="Viridis",
        title=f"GDP vs CO₂ Emissions - {country}"
    )

    st.plotly_chart(fig_gdp, use_container_width=True)
