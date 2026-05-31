st.markdown("""
<style>

/* ===== SAFE KPI CARD (NO MOVING / NO OVERLAP) ===== */
.kpi-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 10px;
    transition: 0.25s ease;
}

/* hover effect ONLY on real KPI cards */
.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.12);
}

/* KPI text styles */
.kpi-title {
    font-size: 14px;
    color: #6b7280;
    font-weight: 600;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 22px;
    font-weight: bold;
    color: #0f3d3e;
}

/* FIX STREAMLIT COLUMN SPACING */
div[data-testid="column"] {
    padding: 10px;
}

/* PREVENT OVERLAP ISSUES */
.element-container {
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)
