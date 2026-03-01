# app/agent/tool_registry.py

from typing import List, Dict

from app.services.deals_service import DealsService
from app.services.work_orders_service import WorkOrdersService
from app.services.business_logic import BusinessLogicService
from app.utils.trace_logger import TraceLogger
from app.utils.date_utils import is_same_quarter
from app.config.constants import REFERENCE_DATE


class ToolRegistry:

    def __init__(self, trace_logger: TraceLogger):
        self.deals_service = DealsService()
        self.work_orders_service = WorkOrdersService()
        self.business_logic = BusinessLogicService()
        self.trace_logger = trace_logger

    # -------------------------------------------------
    # DEALS TOOL
    # -------------------------------------------------
    def _handle_fetch_deals(self, arguments: dict):

        deals = self.deals_service.get_all_deals()

        # Apply filters
        sector = arguments.get("sector")
        stage = arguments.get("stage")
        quarter = arguments.get("quarter")

        if sector:
            deals = [
                d for d in deals
                if d["sector"].lower() == sector.lower()
            ]

        if stage:
            deals = [
                d for d in deals
                if d["stage"].lower() == stage.lower()
            ]

        if quarter:
            deals = [
                d for d in deals
                if d["close_date"]
                and is_same_quarter(d["close_date"], REFERENCE_DATE)
            ]

        summary = self.business_logic.generate_pipeline_summary(deals)

        self.trace_logger.add_trace(
            tool_name="fetch_deals",
            arguments=arguments,
            rows_returned=len(deals)
        )

        return {
            "summary": summary,
            "filtered_count": len(deals)
        }

    # -------------------------------------------------
    # WORK ORDERS TOOL
    # -------------------------------------------------
    def _handle_fetch_work_orders(self, arguments: dict):

        work_orders = self.work_orders_service.get_all_work_orders()

        sector = arguments.get("sector")
        status = arguments.get("status")

        if sector:
            work_orders = [
                w for w in work_orders
                if w["sector"].lower() == sector.lower()
            ]

        if status:
            work_orders = [
                w for w in work_orders
                if w["status"].lower() == status.lower()
            ]

        summary = self.business_logic.generate_revenue_summary(work_orders)

        self.trace_logger.add_trace(
            tool_name="fetch_work_orders",
            arguments=arguments,
            rows_returned=len(work_orders)
        )

        return {
            "summary": summary,
            "filtered_count": len(work_orders)
        }

    # -------------------------------------------------
    # CONVERSION TOOL (cross-board intelligence)
    # -------------------------------------------------
    def _handle_conversion_analysis(self):

        deals = self.deals_service.get_all_deals()
        work_orders = self.work_orders_service.get_all_work_orders()

        summary = self.business_logic.generate_conversion_summary(
            deals,
            work_orders
        )

        self.trace_logger.add_trace(
            tool_name="conversion_analysis",
            arguments={},
            rows_returned=len(deals)
        )

        return {
            "summary": summary
        }

    # -------------------------------------------------
    # EXECUTE
    # -------------------------------------------------
    def execute(self, tool_name: str, arguments: dict):

        if tool_name == "fetch_deals":
            return self._handle_fetch_deals(arguments)

        elif tool_name == "fetch_work_orders":
            return self._handle_fetch_work_orders(arguments)

        elif tool_name == "conversion_analysis":
            return self._handle_conversion_analysis()

        else:
            raise ValueError(f"Unknown tool: {tool_name}")