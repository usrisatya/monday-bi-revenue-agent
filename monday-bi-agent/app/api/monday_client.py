import requests
import json
import logging
from typing import Dict, Any, Optional

from app.config.settings import settings


logger = logging.getLogger(__name__)


class MondayAPIError(Exception):
    """Custom exception for Monday API errors."""
    pass


class MondayClient:
    """
    Responsible ONLY for:
    - Sending live GraphQL queries to Monday.com
    - Handling API/network errors
    - Returning raw JSON response
    """

    BASE_URL = "https://api.monday.com/v2"

    def __init__(self) -> None:
        if not settings.MONDAY_API_KEY:
            raise MondayAPIError("MONDAY_API_KEY is not configured.")

        self.headers = {
            "Authorization": settings.MONDAY_API_KEY,
            "Content-Type": "application/json"
        }

    # --------------------------------------------------
    # Core GraphQL Executor
    # --------------------------------------------------
    def execute_query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        retries: int = 2
    ) -> Dict[str, Any]:
        """
        Executes a GraphQL query against Monday API.
        Supports optional variables and retry logic.
        """

        payload = {
            "query": query,
            "variables": variables or {}
        }

        attempt = 0

        while attempt <= retries:
            try:
                response = requests.post(
                    self.BASE_URL,
                    headers=self.headers,
                    json=payload,
                    timeout=20
                )
                break
            except requests.exceptions.RequestException as e:
                logger.error("Network error calling Monday API", exc_info=True)
                attempt += 1
                if attempt > retries:
                    raise MondayAPIError(
                        f"Network error calling Monday API after {retries} retries: {str(e)}"
                    )

        if response.status_code != 200:
            logger.error("Monday API HTTP Error: %s", response.text)
            raise MondayAPIError(
                f"Monday API returned status {response.status_code}: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise MondayAPIError("Invalid JSON response from Monday API.")

        # GraphQL-level errors
        if "errors" in data:
            error_messages = [
                err.get("message", "Unknown error") for err in data["errors"]
            ]
            raise MondayAPIError(
                f"GraphQL error(s): {', '.join(error_messages)}"
            )

        return data

    # --------------------------------------------------
    # Optional: Helper Methods
    # --------------------------------------------------

    def get_board_items(self, board_id: int) -> Dict[str, Any]:
        """
        Example helper method to fetch items from a board.
        """
        query = """
        query ($board_id: [ID!]) {
            boards(ids: $board_id) {
                id
                name
                items_page(limit: 50) {
                    items {
                        id
                        name
                    }
                }
            }
        }
        """

        variables = {"board_id": board_id}

        return self.execute_query(query=query, variables=variables)