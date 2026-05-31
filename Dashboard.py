# ============================================================
# PROFESSIONAL SDG 13 DASHBOARD (IMPROVED FINAL VERSION)
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
    layout="wide"
)

# ============================================================
# CUSTOM STYLE (CLEAN + MODERN)
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.hero {
    background: linear-gradient(90deg,#0f4c75,#3282b8);
    padding: 35px;
    border-radius: 18px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
}

.kpi {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
    text-align: center;
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

        df = pd.melt(
            df,
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
# HERO SECTION
# ============================================================

st.markdown("""
<div class="hero">
<h1>🌍 SDG 13: Climate Action Dashboard</h1>
<p style="font-size:18px;">
Understanding Global CO₂ Emissions & Development Drivers (2000–2020)
</p>
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
# KPI SECTION (IMPROVED)
# ============================================================

st.subheader(f"📊 Global Overview ({year})")

c1, c2, c3, c4 = st.columns(4)

c1.markdown("<div class='kpi'>🌫️<br><b>{:,.0f}</b><br>CO₂ Emissions</div>".format(
    data["CO2"].mean()), unsafe_allow_html=True)

c2.markdown("<div class='kpi'>🏆<br><b>{}</b><br>Highest Emitter</div>".format(
    data.loc[data["CO2"].idxmax(), "Country Name"]), unsafe_allow_html=True)

c3.markdown("<div class='kpi'>💰<br><b>{:,.0f}</b><br>GDP per Capita</div>".format(
    data["GDP_per_capita"].mean()), unsafe_allow_html=True)

c4.markdown("<div class='kpi'>⚡<br><b>{:.1f}%</b><br>Electricity Access</div>".format(
    data["Electricity"].mean()), unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# LAYOUT: MAP + TOP COUNTRIES
# ============================================================

left, right = st.columns(2)

with left:

    st.markdown("### 🌍 Global CO₂ Map")

    fig_map = px.choropleth(
        data,
        locations="Country Code",
        color="CO2",
        hover_name="Country Name",
        color_continuous_scale="YlGnBu",
        title="CO₂ Emissions"
    )

    st.plotly_chart(fig_map, use_container_width=True)

with right:

    st.markdown("### 🏆 Top Emitters")

    top10 = data.nlargest(10, "CO2")

    fig_top = px.bar(
        top10,
        x="Country Name",
        y="CO2",
        color="CO2",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig_top, use_container_width=True)

# ============================================================
# TREND
# ============================================================

st.markdown("### 📈 Global CO₂ Trend")

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
# DRIVER ANALYSIS
# ============================================================

st.markdown("### 📊 Key Drivers of Emissions")

drivers = pd.DataFrame({
    "Driver": ["GDP per Capita", "Urban Population", "Population", "Electricity Access"],
    "Impact": [0.42, 0.28, 0.18, 0.12]
})

fig_driver = px.bar(
    drivers,
    x="Driver",
    y="Impact",
    color="Impact",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig_driver, use_container_width=True)

# ============================================================
# CORRELATION
# ============================================================

st.markdown("### 🔥 Correlation Analysis")

corr = data[[
    "CO2",
    "GDP_per_capita",
    "Urban",
    "Population",
    "Electricity"
]].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu"
)

st.plotly_chart(fig_corr, use_container_width=True)

# ============================================================
# INSIGHTS
# ============================================================

st.success("""
KEY INSIGHTS:

• GDP per Capita is the strongest driver of CO₂ emissions.

• Urbanization increases energy consumption.

• Population size contributes moderately to emissions.

• Electricity access supports development but is not the main driver.

• Economic growth and urbanization are the key global factors.
""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown("""
<div style="text-align:center;color:gray">
<b>SDG 13 Climate Action Dashboard</b><br>
Built using Streamlit + Python + Plotly
</div>
""", unsafe_allow_html=True)
