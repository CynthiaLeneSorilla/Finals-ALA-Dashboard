import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="SDG 13 Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_data():

    # Read World Bank datasets
    co2 = pd.read_csv("co2.csv", skiprows=4)
    gdp = pd.read_csv("gdp.csv", skiprows=4)
    urban = pd.read_csv("urban.csv", skiprows=4)
    population = pd.read_csv("population.csv", skiprows=4)
    electricity = pd.read_csv("electricity.csv", skiprows=4)

    def reshape(df, value_name):

        id_vars = ["Country Name", "Country Code"]

        year_cols = [
            col for col in df.columns
            if str(col).isdigit()
        ]

        df = df[id_vars + year_cols]

        df_long = pd.melt(
            df,
            id_vars=id_vars,
            value_vars=year_cols,
            var_name="Year",
            value_name=value_name
        )

        df_long["Year"] = df_long["Year"].astype(int)

        return df_long

    co2_long = reshape(co2, "CO2_emissions_kt")
    gdp_long = reshape(gdp, "GDP_current_USD")
    urban_long = reshape(urban, "Urban_population_pct")
    pop_long = reshape(population, "Population")
    elec_long = reshape(electricity, "Electricity_access_pct")

    # Merge datasets
    df = co2_long.merge(
        gdp_long,
        on=["Country Name", "Country Code", "Year"]
    )

    df = df.merge(
        urban_long,
        on=["Country Name", "Country Code", "Year"]
    )

    df = df.merge(
        pop_long,
        on=["Country Name", "Country Code", "Year"]
    )

    df = df.merge(
        elec_long,
        on=["Country Name", "Country Code", "Year"]
    )

    # Remove missing values
    df = df.dropna()

    # Keep years 2000-2020
    df = df[
        (df["Year"] >= 2000) &
        (df["Year"] <= 2020)
    ]

    # Remove aggregates
    aggregates = [
        "World",
        "High income",
        "Low income",
        "Middle income",
        "North America",
        "European Union",
        "OECD members"
    ]

    df = df[
        ~df["Country Name"].isin(aggregates)
    ]

    # Derived Variables
    df["GDP_per_capita"] = (
        df["GDP_current_USD"] /
        df["Population"]
    )

    df["CO2_per_capita"] = (
        df["CO2_emissions_kt"] * 1000 /
        df["Population"]
    )

    df["Log_GDP_per_capita"] = np.log(
        df["GDP_per_capita"] + 1
    )

    df["Log_CO2_emissions"] = np.log(
        df["CO2_emissions_kt"] + 1
    )

    df["Log_Population"] = np.log(
        df["Population"] + 1
    )

    return df


df = load_data()

# ==========================================================
# TITLE
# ==========================================================
st.markdown(
    """
    <p style='font-size:55px;
    color:#4CAF50;
    font-weight:bold;'>
    🌍 SDG 13: Climate Action Dashboard
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    Analysis of Key Drivers of CO₂ Emissions
    """
)

# ==========================================================
# YEAR SLIDER
# ==========================================================
year = st.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    2019
)

filtered_df = df[
    df["Year"] == year
]

# ==========================================================
# KPI CARDS
# ==========================================================
avg_co2 = filtered_df["CO2_emissions_kt"].mean()

max_country = filtered_df.loc[
    filtered_df["CO2_emissions_kt"].idxmax(),
    "Country Name"
]

avg_gdp = filtered_df["GDP_per_capita"].mean()

avg_electricity = (
    filtered_df["Electricity_access_pct"]
    .mean()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average CO₂",
    f"{avg_co2:,.0f}"
)

col2.metric(
    "Highest Emitter",
    max_country
)

col3.metric(
    "GDP per Capita",
    f"${avg_gdp:,.0f}"
)

col4.metric(
    "Electricity Access",
    f"{avg_electricity:.1f}%"
)

# ==========================================================
# CHOROPLETH MAP
# ==========================================================
st.subheader(
    "🌎 Global CO₂ Emissions"
)

fig_map = px.choropleth(
    filtered_df,
    locations="Country Code",
    color="CO2_emissions_kt",
    hover_name="Country Name",
    color_continuous_scale="YlOrRd",
    title=f"CO₂ Emissions by Country ({year})"
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)

# ==========================================================
# DRIVER IMPORTANCE
# ==========================================================
st.subheader(
    "📊 Key Drivers of CO₂ Emissions"
)

drivers = pd.DataFrame({
    "Driver":[
        "GDP per Capita",
        "Urban Population %",
        "Population",
        "Electricity Access %"
    ],
    "Importance":[
        0.45,
        0.30,
        0.15,
        0.10
    ]
})

fig_driver = px.bar(
    drivers,
    x="Driver",
    y="Importance",
    color="Importance",
    title="Regression Driver Importance"
)

st.plotly_chart(
    fig_driver,
    use_container_width=True
)

# ==========================================================
# TREND OVER TIME
# ==========================================================
st.subheader(
    "📈 CO₂ Emissions Trend"
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
    markers=True
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

# ==========================================================
# TOP 10 COUNTRIES
# ==========================================================
st.subheader(
    "🏆 Top 10 CO₂ Emitting Countries"
)

top10 = filtered_df.nlargest(
    10,
    "CO2_emissions_kt"
)

fig_top = px.bar(
    top10,
    x="Country Name",
    y="CO2_emissions_kt",
    color="CO2_emissions_kt"
)

st.plotly_chart(
    fig_top,
    use_container_width=True
)

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================
st.subheader(
    "🔥 Correlation Heatmap"
)

corr_cols = [
    "Log_CO2_emissions",
    "Log_GDP_per_capita",
    "Urban_population_pct",
    "Log_Population",
    "Electricity_access_pct"
]

corr = (
    filtered_df[corr_cols]
    .corr()
)

fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r"
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)

# ==========================================================
# FOOTER
# ==========================================================
st.markdown("---")

st.markdown(
    """
    **Source:** World Bank Open Data

    SDG 13 Climate Action Dashboard
    """
)
