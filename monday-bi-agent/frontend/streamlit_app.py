import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from app.main import EnterpriseBIAgent

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="Revenue Intelligence Dashboard",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------------------------
# Styling
# -------------------------------------------------

st.markdown("""
<style>
.big-font {
    font-size:18px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Series-A Revenue Intelligence Dashboard")

# -------------------------------------------------
# Load Agent
# -------------------------------------------------

agent = EnterpriseBIAgent()
df = agent.df

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------

st.sidebar.header("📌 Filters")

sector_filter = st.sidebar.selectbox(
    "Sector",
    ["All"] + sorted(df["sector"].unique().tolist())
)

owner_filter = st.sidebar.selectbox(
    "Owner",
    ["All"] + sorted(df["owner"].unique().tolist())
)

filtered_df = agent.filter_data(sector_filter, owner_filter)

summary = agent.executive_summary(filtered_df)
conversion = agent.conversion_rate(filtered_df)
forecast_90 = agent.forecast_next_90_days(filtered_df)
velocity = agent.pipeline_velocity(filtered_df)
risk_dist = agent.risk_distribution(filtered_df)
insights = agent.generate_ai_insights(filtered_df)

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------

st.markdown("## 📊 Executive Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Deals", summary["total_deals"])
col2.metric("Pipeline", f"₹{summary['total_value']:,.0f}")
col3.metric("Weighted", f"₹{summary['weighted_value']:,.0f}")
col4.metric("Conversion %", f"{conversion:.2f}%")
col5.metric("90-Day Forecast", f"₹{forecast_90:,.0f}")

st.caption(f"Data Source: **{summary['data_source']}**")

st.divider()

# -------------------------------------------------
# Velocity & Risk
# -------------------------------------------------

st.markdown("## ⚡ Pipeline Health")

colA, colB = st.columns(2)

colA.metric("Pipeline Velocity Score", f"{velocity:,.0f}")

risk_chart = px.bar(
    x=list(risk_dist.keys()),
    y=list(risk_dist.values()),
    title="Risk Distribution"
)

colB.plotly_chart(risk_chart, use_container_width=True)

st.divider()

# -------------------------------------------------
# Revenue Breakdown
# -------------------------------------------------

st.markdown("## 📈 Revenue Breakdown")

col1, col2 = st.columns(2)

owner_chart = px.bar(
    agent.revenue_by_owner(filtered_df),
    x="owner",
    y="deal_value",
    title="Revenue by Owner",
    text_auto=True
)

sector_chart = px.pie(
    agent.revenue_by_sector(filtered_df),
    names="sector",
    values="deal_value",
    title="Sector Contribution"
)

col1.plotly_chart(owner_chart, use_container_width=True)
col2.plotly_chart(sector_chart, use_container_width=True)

st.divider()

# -------------------------------------------------
# Stage Analysis
# -------------------------------------------------

stage_chart = px.bar(
    agent.revenue_by_stage(filtered_df),
    x="stage",
    y="deal_value",
    title="Revenue by Stage",
    text_auto=True
)

st.plotly_chart(stage_chart, use_container_width=True)

st.divider()

# -------------------------------------------------
# AI Insights Panel
# -------------------------------------------------

st.markdown("## 🧠 AI Executive Insights")

for insight in insights:
    st.info(insight)

st.divider()

# -------------------------------------------------
# Data Table
# -------------------------------------------------

st.markdown("## 📋 Deal Intelligence Table")

st.dataframe(
    filtered_df.sort_values("deal_value", ascending=False),
    use_container_width=True
)

st.caption("Built with Enterprise Revenue Intelligence Architecture 🚀")