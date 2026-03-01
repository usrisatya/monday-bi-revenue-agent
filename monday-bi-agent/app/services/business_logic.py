# app/services/business_logic.py

from typing import List, Dict
from collections import defaultdict
from datetime import datetime

from app.config.constants import (
    CLOSED_WON_STAGES,
    CLOSED_LOST_STAGES,
    EARLY_STAGE_STAGES,
    DEFAULT_CURRENCY,
    REFERENCE_DATE,
    HIGH_RISK_EARLY_STAGE_PERCENT,
    LOW_CONVERSION_THRESHOLD
)

from app.utils.date_utils import is_same_quarter


class BusinessLogicService:

    # -----------------------------
    # PIPELINE METRICS
    # -----------------------------
    def calculate_pipeline_value(self, deals: List[Dict]) -> float:
        return sum(
            d["deal_value"]
            for d in deals
            if d["stage"] not in CLOSED_WON_STAGES + CLOSED_LOST_STAGES
        )

    def calculate_stage_distribution(self, deals: List[Dict]) -> Dict[str, int]:
        distribution = defaultdict(int)

        for deal in deals:
            stage = deal["stage"] or "Unknown"
            distribution[stage] += 1

        return dict(distribution)

    def calculate_early_stage_risk(self, deals: List[Dict]) -> float:
        if not deals:
            return 0.0

        early_stage_count = sum(
            1 for d in deals if d["stage"] in EARLY_STAGE_STAGES
        )

        return early_stage_count / len(deals)

    # -----------------------------
    # REVENUE METRICS
    # -----------------------------
    def calculate_total_revenue(self, work_orders: List[Dict]) -> float:
        return sum(w["revenue"] for w in work_orders)

    def revenue_by_sector(self, work_orders: List[Dict]) -> Dict[str, float]:
        sector_map = defaultdict(float)

        for w in work_orders:
            sector_map[w["sector"]] += w["revenue"]

        return dict(sector_map)

    # -----------------------------
    # CONVERSION METRICS
    # -----------------------------
    def calculate_conversion_rate(
        self,
        deals: List[Dict],
        work_orders: List[Dict]
    ) -> float:

        if not deals:
            return 0.0

        won_deals = [
            d for d in deals if d["stage"] in CLOSED_WON_STAGES
        ]

        return len(won_deals) / len(deals)

    # -----------------------------
    # QUARTERLY PIPELINE
    # -----------------------------
    def quarterly_pipeline(self, deals: List[Dict]) -> float:

        current_quarter_deals = [
            d for d in deals
            if d["close_date"]
            and is_same_quarter(d["close_date"], REFERENCE_DATE)
        ]

        return sum(d["deal_value"] for d in current_quarter_deals)

    # -----------------------------
    # EXECUTIVE SUMMARY GENERATOR
    # -----------------------------
    def generate_pipeline_summary(self, deals: List[Dict]) -> str:

        total_pipeline = self.calculate_pipeline_value(deals)
        stage_distribution = self.calculate_stage_distribution(deals)
        early_stage_ratio = self.calculate_early_stage_risk(deals)

        summary = f"Current pipeline value stands at {DEFAULT_CURRENCY}{total_pipeline:,.0f}. "

        if early_stage_ratio > HIGH_RISK_EARLY_STAGE_PERCENT:
            summary += (
                "A significant portion of deals are in early stages, "
                "indicating elevated conversion risk. "
            )

        summary += f"Stage distribution: {stage_distribution}."

        return summary

    def generate_revenue_summary(self, work_orders: List[Dict]) -> str:

        total_revenue = self.calculate_total_revenue(work_orders)
        sector_revenue = self.revenue_by_sector(work_orders)

        summary = f"Total realized revenue is {DEFAULT_CURRENCY}{total_revenue:,.0f}. "

        if sector_revenue:
            top_sector = max(sector_revenue, key=sector_revenue.get)
            summary += (
                f"The highest contributing sector is {top_sector} "
                f"with {DEFAULT_CURRENCY}{sector_revenue[top_sector]:,.0f}."
            )

        return summary

    def generate_conversion_summary(
        self,
        deals: List[Dict],
        work_orders: List[Dict]
    ) -> str:

        conversion_rate = self.calculate_conversion_rate(deals, work_orders)

        summary = f"Overall deal conversion rate is {conversion_rate:.0%}. "

        if conversion_rate < LOW_CONVERSION_THRESHOLD:
            summary += (
                "This indicates potential bottlenecks in closing deals "
                "and may require review of sales processes."
            )

        return summary