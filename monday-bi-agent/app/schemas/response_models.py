# app/schemas/response_models.py

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class DealModel(BaseModel):
    item_id: str
    deal_name: str
    sector: str
    deal_value: float
    stage: str
    close_date: Optional[datetime]


class WorkOrderModel(BaseModel):
    item_id: str
    client_name: str
    sector: str
    revenue: float
    status: str
    completion_date: Optional[datetime]


class ToolTraceModel(BaseModel):
    tool_name: str
    arguments: dict
    graphql_query: Optional[str]
    rows_returned: Optional[int]


class AgentResponse(BaseModel):
    answer: str
    tool_traces: List[ToolTraceModel]