from app.api.monday_client import MondayClient
from app.config.settings import settings

client = MondayClient()

query = f"""
query {{
  boards(ids: {settings.DEALS_BOARD_ID}) {{
    name
  }}
}}
"""

result = client.execute_query(query)
print(result)