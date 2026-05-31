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
    layout="wide"
)

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

h1 {
    color: #0b3d91;
    text-align: center;
}

.block-container {
    padding-top: 2rem;
}

.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
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
    pop = reshape(population, "Population")
    elec = reshape(electricity, "Electricity")

    df = co2.merge(gdp, on=["Country Name","Country Code","Year"])
    df = df.merge(urban, on=["Country Name","Country Code","Year"])
    df = df.merge(pop, on=["Country Name","Country Code","Year"])
    df = df.merge(elec, on=["Country Name","Country Code","Year"])

    df = df.dropna()
    df = df[(df["Year"] >= 2000) & (df["Year"] <= 2020)]

    remove = ["World","High income","Low income","Middle income","OECD members"]
    df = df[~df["Country Name"].isin(remove)]

    df["GDP_per_capita"] = df["GDP"] / df["Population"]

    return df

df = load_data()

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div style="
background: linear-gradient(90deg,#0b3d91,#1e88e5);
padding:25px;
border-radius:15px;
text-align:center;
color:white;
">

<h1 style="color:white;">🌍 SDG 13: Climate Action Dashboard</h1>
<p>Global Analysis of CO₂ Emissions & Socioeconomic Drivers (2000–2020)</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ============================================================
# SIDEBAR FILTER
# ============================================================

year = st.sidebar.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    2019
)

data = df[df["Year"] == year]

# ============================================================
# KPI SECTION
# ============================================================

st.markdown("## 📊 Global Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric("CO₂ Emissions", f"{data['CO2'].mean():,.0f}")
c2.metric("Highest Emitter", data.loc[data['CO2'].idxmax(),'Country Name'])
c3.metric("GDP per Capita", f"{data['GDP_per_capita'].mean():,.0f}")
c4.metric("Electricity Access", f"{data['Electricity'].mean():.1f}%")

st.write("")

# ============================================================
# MAP + DRIVERS
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🌍 CO₂ Emissions Map")

    fig_map = px.choropleth(
        data,
        locations="Country Code",
        color="CO2",
        hover_name="Country Name",
        color_continuous_scale="YlGnBu",
        title="CO₂ Emissions"
    )

    st.plotly_chart(fig_map, use_container_width=True)

with col2:

    st.markdown("### 📊 Key Drivers")

    drivers = pd.DataFrame({
        "Driver": ["GDP per Capita","Urbanization","Population","Electricity"],
        "Impact": [0.45,0.30,0.18,0.12]
    })

    fig_driver = px.bar(
        drivers,
        x="Driver",
        y="Impact",
        color="Impact"
    )

    st.plotly_chart(fig_driver, use_container_width=True)

# ============================================================
# TREND
# ============================================================

st.markdown("## 📈 Global CO₂ Trend")

trend = df.groupby("Year")["CO2"].mean().reset_index()

fig_trend = px.line(
    trend,
    x="Year",
    y="CO2",
    markers=True,
    title="CO₂ Emissions Over Time"
)

st.plotly_chart(fig_trend, use_container_width=True)

# ============================================================
# TOP COUNTRIES
# ============================================================

st.markdown("## 🏆 Top Emitters")

top = data.nlargest(10, "CO2")

fig_top = px.bar(
    top,
    x="Country Name",
    y="CO2",
    color="CO2"
)

st.plotly_chart(fig_top, use_container_width=True)

# ============================================================
# CORRELATION
# ============================================================

st.markdown("## 🔥 Correlation Analysis")

corr = data[[
    "CO2","GDP_per_capita","Urban","Population","Electricity"
]].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu"
)

st.plotly_chart(fig_corr, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown("""
### 🌍 SDG 13 Climate Action Dashboard  
Built using Streamlit, Pandas, NumPy, and Plotly  
Final Project – Analytics Techniques & Tools
""")
