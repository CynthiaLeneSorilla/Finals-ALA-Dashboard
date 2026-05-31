# 🌍 SDG 13: Climate Action — Data Analytics Dashboard

## 📌 Project Overview

This project explores the global factors influencing carbon emissions using an interactive data analytics dashboard. It is designed to help understand how economic development, population growth, urbanization, and energy access contribute to environmental impact across countries and time.

The system transforms raw World Bank datasets into a clean analytical framework and presents insights through an interactive Streamlit dashboard.

👉 The goal is not just visualization, but **explanatory analytics** — identifying what drives CO₂ emissions globally.

---

## 🎯 Research Question

> What socioeconomic and environmental factors influence CO₂ emissions across countries from 2000 to 2020?

---

## 📊 Data Sources

This study integrates multiple global datasets:

- World Bank CO₂ Emissions Data
- GDP (World Bank)
- Urban Population (%)
- Total Population
- Electricity Access (%)

All datasets are merged using country codes and standardized across time (2000–2020).

---

## 🛠️ Data Processing Approach

The data pipeline includes:

- Reshaping wide-format indicators into long-format time series
- Standardizing country-level identifiers
- Handling missing values and removing aggregate regions
- Feature engineering (e.g., GDP per capita calculation)
- Time filtering for consistent analysis period

---

## 📈 Analytical Methods

The dashboard applies exploratory and inferential analytics:

- Correlation analysis between variables
- Time-series trend analysis of CO₂ emissions
- Cross-country comparison using rankings
- Driver importance estimation (proxy regression coefficients)

Key variables analyzed:
- GDP per capita
- Urbanization rate
- Population size
- Electricity access

---

## 🖥️ Dashboard Features

The interactive dashboard includes:

- 📌 KPI summary cards for global indicators
- 🌍 Choropleth map of CO₂ emissions
- 📈 Time-series trend visualization
- 🏆 Top emitting countries ranking
- 📊 Driver importance analysis
- 🔥 Correlation heatmap
- 🎛️ Year-based filter for dynamic exploration

---

## 🚀 How to Run the Project

```bash
pip install streamlit pandas numpy plotly
streamlit run Dashboard.py
