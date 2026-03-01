# app/api/query_builder.py

from typing import Optional


def build_fetch_items_query(
    board_id: str,
    limit: int = 100,
    cursor: Optional[str] = None
) -> str:
    """
    Builds a GraphQL query to fetch board items with pagination support.
    """

    cursor_part = f', cursor: "{cursor}"' if cursor else ""

    query = f"""
    query {{
      boards(ids: {board_id}) {{
        name
        items_page(limit: {limit}{cursor_part}) {{
          cursor
          items {{
            id
            name
            column_values {{
              id
              text
              value
              type
            }}
          }}
        }}
      }}
    }}
    """

    return query