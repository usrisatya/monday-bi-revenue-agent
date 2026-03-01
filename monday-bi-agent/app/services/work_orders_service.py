# app/services/work_orders_service.py

from typing import List, Dict, Any

from app.api.monday_client import MondayClient
from app.api.query_builder import build_fetch_items_query
from app.config.settings import settings

from app.services.data_cleaning import (
    clean_number,
    normalize_sector,
    parse_date,
    clean_text
)


class WorkOrdersService:

    def __init__(self):
        self.client = MondayClient()
        self.board_id = settings.WORK_ORDERS_BOARD_ID

    def fetch_raw_work_orders(self) -> List[Dict[str, Any]]:
        query = build_fetch_items_query(self.board_id)
        response = self.client.execute_query(query)

        boards = response.get("data", {}).get("boards", [])
        if not boards:
            return []

        return boards[0].get("items_page", {}).get("items", [])

    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:

        work_order = {
            "item_id": item.get("id"),
            "client_name": clean_text(item.get("name")),
            "sector": "Unknown",
            "revenue": 0.0,
            "status": "",
            "completion_date": None,
        }

        for column in item.get("column_values", []):
            col_id = column.get("id")
            text = column.get("text")

            # ⚠️ Update IDs if your Monday board auto-generated different ones
            if col_id == "sector":
                work_order["sector"] = normalize_sector(text)

            elif col_id == "revenue":
                work_order["revenue"] = clean_number(text)

            elif col_id == "status":
                work_order["status"] = clean_text(text)

            elif col_id == "completion_date":
                work_order["completion_date"] = parse_date(text)

        return work_order

    def get_all_work_orders(self) -> List[Dict[str, Any]]:
        raw_items = self.fetch_raw_work_orders()
        return [self.transform_item(item) for item in raw_items]