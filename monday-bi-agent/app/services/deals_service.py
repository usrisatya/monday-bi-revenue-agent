# app/services/deals_service.py

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


class DealsService:

    def __init__(self):
        self.client = MondayClient()
        self.board_id = settings.DEALS_BOARD_ID

    def fetch_raw_deals(self) -> List[Dict[str, Any]]:
        """
        Fetches raw deals from Monday board.
        """

        query = build_fetch_items_query(self.board_id)
        response = self.client.execute_query(query)

        boards = response.get("data", {}).get("boards", [])

        if not boards:
            return []

        items = boards[0].get("items_page", {}).get("items", [])
        return items

    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts Monday item into structured, cleaned deal dictionary.
        """

        deal_data = {
            "item_id": item.get("id"),
            "deal_name": clean_text(item.get("name")),
            "sector": "Unknown",
            "deal_value": 0.0,
            "stage": "",
            "close_date": None,
        }

        for column in item.get("column_values", []):
            col_id = column.get("id")
            text = column.get("text")

            # ⚠️ Ensure these match your real Monday column IDs
            if col_id == "sector":
                deal_data["sector"] = normalize_sector(text)

            elif col_id == "deal_value":
                deal_data["deal_value"] = clean_number(text)

            elif col_id == "stage":
                deal_data["stage"] = clean_text(text)

            elif col_id == "close_date":
                deal_data["close_date"] = parse_date(text)

        return deal_data

    def get_all_deals(self) -> List[Dict[str, Any]]:
        """
        Public method:
        Returns fully transformed and cleaned deals list.
        """

        raw_items = self.fetch_raw_deals()

        return [self.transform_item(item) for item in raw_items]