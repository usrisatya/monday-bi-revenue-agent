# app/schemas/tool_schemas.py

# -------------------------------------------------
# FETCH DEALS TOOL
# -------------------------------------------------

FETCH_DEALS_TOOL = {
    "type": "function",
    "function": {
        "name": "fetch_deals",
        "description": (
            "Fetch deals from the Monday Deals board. "
            "Use optional filters like sector, stage, or quarter."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sector": {
                    "type": "string",
                    "description": "Filter deals by sector (e.g., Energy, Healthcare)"
                },
                "stage": {
                    "type": "string",
                    "description": "Filter deals by stage (e.g., Proposal, Closed Won)"
                },
                "quarter": {
                    "type": "string",
                    "description": "Filter deals by current quarter (e.g., Q1, Q2)"
                }
            }
        }
    }
}


# -------------------------------------------------
# FETCH WORK ORDERS TOOL
# -------------------------------------------------

FETCH_WORK_ORDERS_TOOL = {
    "type": "function",
    "function": {
        "name": "fetch_work_orders",
        "description": (
            "Fetch work orders from the Monday Work Orders board. "
            "Supports filtering by sector or status."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sector": {
                    "type": "string",
                    "description": "Filter work orders by sector"
                },
                "status": {
                    "type": "string",
                    "description": "Filter work orders by status"
                }
            }
        }
    }
}


# -------------------------------------------------
# CONVERSION ANALYSIS TOOL (Cross-board intelligence)
# -------------------------------------------------

CONVERSION_ANALYSIS_TOOL = {
    "type": "function",
    "function": {
        "name": "conversion_analysis",
        "description": (
            "Analyze overall deal-to-work-order conversion performance "
            "across both boards."
        ),
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}


# -------------------------------------------------
# ALL TOOLS REGISTRY
# -------------------------------------------------

ALL_TOOLS = [
    FETCH_DEALS_TOOL,
    FETCH_WORK_ORDERS_TOOL,
    CONVERSION_ANALYSIS_TOOL
]