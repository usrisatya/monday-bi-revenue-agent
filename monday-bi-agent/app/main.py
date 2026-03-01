# app/main.py

import pandas as pd
from datetime import datetime, timedelta
from typing import Optional

# --------------------------------------------------
# Try Monday Integration
# --------------------------------------------------

try:
    from app.services.deals_service import DealsService
    from app.services.work_orders_service import WorkOrdersService
    MONDAY_AVAILABLE = True
except Exception:
    MONDAY_AVAILABLE = False


# --------------------------------------------------
# Dummy Fallback
# --------------------------------------------------

def load_dummy_data():

    data = [
        ("Naruto", "OWNER_001", "Mining", "Sales Qualified Leads", "High", 489360, 30),
        ("Sasuke", "OWNER_002", "Powerline", "Proposal Sent", "Medium", 611700, 45),
        ("Sakura", "OWNER_004", "DSP", "Work Order Received", "High", 4281900, 10),
        ("Luffy", "OWNER_003", "Tender", "Negotiations", "High", 122340000, 60),
        ("Tanjiro", "OWNER_001", "Mining", "Lead Generated", "High", 2079780, 15),
        ("Zoro", "OWNER_003", "Railways", "Proposal Sent", "Medium", 3058500, 40),
        ("Goku", "OWNER_003", "Railways", "Negotiations", "Medium", 2018605, 50),
        ("Rukia", "OWNER_001", "Renewables", "Demo Done", "High", 3058500, 25),
        ("Nami", "OWNER_004", "Tender", "Proposal Sent", "Low", 91755000, 70),
        ("Sanji", "OWNER_003", "Security", "Negotiations", "Medium", 7340400, 55),
    ]

    df = pd.DataFrame(data, columns=[
        "deal_name",
        "owner",
        "sector",
        "stage",
        "probability",
        "deal_value",
        "age_days"
    ])

    return df


# --------------------------------------------------
# Enrichment Layer
# --------------------------------------------------

def enrich_dataframe(df: pd.DataFrame):

    probability_map = {
        "High": 0.8,
        "Medium": 0.5,
        "Low": 0.2
    }

    df["probability_weight"] = df["probability"].map(probability_map).fillna(0.5)
    df["weighted_value"] = df["deal_value"] * df["probability_weight"]

    # Aging Risk
    df["risk_score"] = df["age_days"].apply(
        lambda x: "High Risk" if x > 60 else
        "Medium Risk" if x > 40 else
        "Low Risk"
    )

    return df


# --------------------------------------------------
# Enterprise Revenue Intelligence Agent
# --------------------------------------------------

class EnterpriseBIAgent:

    def __init__(self):

        self.data_source = "Dummy"
        df = None

        # Try Monday First
        if MONDAY_AVAILABLE:
            try:
                deals_service = DealsService()
                deals = deals_service.get_all_deals()

                if deals:
                    df = pd.DataFrame(deals)
                    df["age_days"] = 30  # fallback if Monday doesn't send
                    self.data_source = "Monday"
            except:
                pass

        # Fallback
        if df is None or df.empty:
            df = load_dummy_data()

        self.df = enrich_dataframe(df)

    # --------------------------------------------------

    def filter_data(self, sector=None, owner=None):

        df = self.df.copy()

        if sector and sector != "All":
            df = df[df["sector"] == sector]

        if owner and owner != "All":
            df = df[df["owner"] == owner]

        return df

    # --------------------------------------------------

    def executive_summary(self, df):

        total_value = df["deal_value"].sum()
        weighted_value = df["weighted_value"].sum()
        total_deals = len(df)
        avg_deal = total_value / total_deals if total_deals else 0

        return {
            "total_deals": total_deals,
            "total_value": total_value,
            "weighted_value": weighted_value,
            "average_deal": avg_deal,
            "data_source": self.data_source
        }

    # --------------------------------------------------
    # Conversion Analysis
    # --------------------------------------------------

    def conversion_rate(self, df):

        if len(df) == 0:
            return 0

        won = df[df["stage"].str.contains("Work Order", case=False)]
        return (len(won) / len(df)) * 100

    # --------------------------------------------------
    # Forecasting Model (Next 90 Days)
    # --------------------------------------------------

    def forecast_next_90_days(self, df):

        forecast_df = df[df["probability"] == "High"]
        forecast_value = forecast_df["weighted_value"].sum()

        return forecast_value

    # --------------------------------------------------
    # Pipeline Velocity
    # --------------------------------------------------

    def pipeline_velocity(self, df):

        if len(df) == 0:
            return 0

        avg_age = df["age_days"].mean()
        velocity_score = df["weighted_value"].sum() / avg_age if avg_age else 0

        return velocity_score

    # --------------------------------------------------
    # Risk Distribution
    # --------------------------------------------------

    def risk_distribution(self, df):

        return df["risk_score"].value_counts().to_dict()

    # --------------------------------------------------
    # Revenue by Dimension
    # --------------------------------------------------

    def revenue_by_owner(self, df):
        return df.groupby("owner")["deal_value"].sum().reset_index()

    def revenue_by_stage(self, df):
        return df.groupby("stage")["deal_value"].sum().reset_index()

    def revenue_by_sector(self, df):
        return df.groupby("sector")["deal_value"].sum().reset_index()

    # --------------------------------------------------
    # AI Insights Generator
    # --------------------------------------------------

    def generate_ai_insights(self, df):

        insights = []

        conversion = self.conversion_rate(df)
        forecast = self.forecast_next_90_days(df)
        velocity = self.pipeline_velocity(df)

        if conversion < 10:
            insights.append("⚠️ Conversion rate is critically low. Review sales qualification process.")

        if forecast > 50_000_000:
            insights.append("🚀 Strong projected 90-day revenue pipeline.")

        if velocity < 100_000:
            insights.append("⏳ Pipeline velocity is slow. Deals aging too long.")

        high_risk = df[df["risk_score"] == "High Risk"]
        if len(high_risk) > 0:
            insights.append(f"🔴 {len(high_risk)} deals are high-risk due to aging.")

        if not insights:
            insights.append("✅ Pipeline health looks stable.")

        return insights