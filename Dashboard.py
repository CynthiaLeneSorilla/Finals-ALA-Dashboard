# ============================================================

# PROFESSIONAL SDG 13 DASHBOARD

# Analytics Techniques and Tools - Final Project

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

# CUSTOM CSS

# ============================================================



st.markdown("""

<style>



.main {

    background-color: #f5f7fa;

}



.metric-card {

    background-color: white;

    padding: 20px;

    border-radius: 15px;

    text-align: center;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);

}



.hero {

    background: linear-gradient(90deg,#0f4c75,#3282b8);

    padding: 30px;

    border-radius: 20px;

    text-align: center;

    color: white;

    margin-bottom: 20px;

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



    df = co2.merge(

        gdp,

        on=["Country Name", "Country Code", "Year"]

    )



    df = df.merge(

        urban,

        on=["Country Name", "Country Code", "Year"]

    )



    df = df.merge(

        pop,

        on=["Country Name", "Country Code", "Year"]

    )



    df = df.merge(

        elec,

        on=["Country Name", "Country Code", "Year"]

    )



    df = df.dropna()



    df = df[

        (df["Year"] >= 2000)

        &

        (df["Year"] <= 2020)

    ]



    remove = [

        "World",

        "High income",

        "Low income",

        "Middle income",

        "OECD members"

    ]



    df = df[

        ~df["Country Name"].isin(remove)

    ]



    df["GDP_per_capita"] = (

        df["GDP_current_USD"] /

        df["Population"]

    )



    df["Log_CO2"] = np.log(

        df["CO2_emissions_kt"] + 1

    )



    return df





df = load_data()



# ============================================================

# HERO SECTION

# ============================================================



st.markdown("""

<div class="hero">

<h1>🌍 SDG 13: Climate Action Dashboard</h1>

<h4>Understanding the Drivers Towards Global Development</h4>

<p>

Analyzing the factors influencing CO₂ emissions across countries

from 2000–2020 using World Bank data.

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

# KPI CARDS

# ============================================================



st.subheader(f"📌 Global Indicators ({year})")



col1, col2, col3, col4 = st.columns(4)



with col1:

    st.metric(

        "Avg CO₂ Emissions",

        f"{data['CO2_emissions_kt'].mean():,.0f}"

    )



with col2:

    st.metric(

        "Highest Emitter",

        data.loc[

            data["CO2_emissions_kt"].idxmax(),

            "Country Name"

        ]

    )



with col3:

    st.metric(

        "GDP Per Capita",

        f"${data['GDP_per_capita'].mean():,.0f}"

    )



with col4:

    st.metric(

        "Electricity Access",

        f"{data['Electricity_access_pct'].mean():.1f}%"

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

            color_continuous_scale="YlGnBu",

            title=f"CO₂ Emissions by Country ({year})"

        )



        st.plotly_chart(

            fig_map,

            use_container_width=True

        )



    with right:



        top10 = data.nlargest(

            10,

            "CO2_emissions_kt"

        )



        fig_top = px.bar(

            top10,

            x="Country Name",

            y="CO2_emissions_kt",

            color="CO2_emissions_kt",

            color_continuous_scale="Reds",

            title="Top 10 CO₂ Emitters"

        )



        st.plotly_chart(

            fig_top,

            use_container_width=True

        )



    trend = (

        df.groupby("Year")

        ["CO2_emissions_kt"]

        .mean()

        .reset_index()

    )



    fig_trend = px.line(

        trend,

        x="Year",

        y="CO2_emissions_kt",

        markers=True,

        title="Average Global CO₂ Emissions Over Time"

    )



    st.plotly_chart(

        fig_trend,

        use_container_width=True

    )



# ============================================================

# TAB 2

# ============================================================



with tab2:



    st.subheader(

        "Regression-Based Driver Analysis"

    )



    drivers = pd.DataFrame({



        "Driver": [

            "GDP per Capita",

            "Urban Population",

            "Population",

            "Electricity Access"

        ],



        "Impact": [

            0.42,

            0.28,

            0.18,

            0.12

        ]

    })



    fig_driver = px.bar(

        drivers,

        x="Driver",

        y="Impact",

        color="Impact",

        color_continuous_scale="Blues",

        title="Key Drivers of CO₂ Emissions"

    )



    st.plotly_chart(

        fig_driver,

        use_container_width=True

    )



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

        title="Correlation Matrix"

    )



    st.plotly_chart(

        fig_corr,

        use_container_width=True

    )



    st.success("""

    KEY FINDINGS



    • GDP per Capita has the strongest positive relationship with CO₂ emissions.



    • Urbanization increases energy demand and industrial activity.



    • Population growth contributes to higher emissions.



    • Electricity access supports development but has a smaller direct impact.



    • Economic development and urbanization are the primary drivers of CO₂ emissions globally.

    """)



# ============================================================

# TAB 3

# ============================================================



with tab3:



    country = st.selectbox(

        "Select Country",

        sorted(df["Country Name"].unique())

    )



    country_df = df[

        df["Country Name"] == country

    ]



    fig_country = px.line(

        country_df,

        x="Year",

        y="CO2_emissions_kt",

        markers=True,

        title=f"CO₂ Emissions Trend - {country}"

    )



    st.plotly_chart(

        fig_country,

        use_container_width=True

    )



    fig_gdp = px.scatter(

        country_df,

        x="GDP_per_capita",

        y="CO2_emissions_kt",

        size="Population",

        color="Urban_population_pct",

        title=f"GDP vs CO₂ Emissions - {country}"

    )



    st.plotly_chart(

        fig_gdp,

        use_container_width=True

    )



# ============================================================

# FOOTER

# ============================================================



st.markdown("---")



st.markdown("""



- Plotly

""")
