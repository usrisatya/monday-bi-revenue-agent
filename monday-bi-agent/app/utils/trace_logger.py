# app/utils/trace_logger.py

from typing import List, Dict, Any


class TraceLogger:

    def __init__(self):
        self.traces: List[Dict[str, Any]] = []

    def add_trace(
        self,
        tool_name: str,
        arguments: dict,
        graphql_query: str = None,
        rows_returned: int = None
    ):
        self.traces.append({
            "tool_name": tool_name,
            "arguments": arguments,
            "graphql_query": graphql_query,
            "rows_returned": rows_returned
        })

    def get_traces(self) -> List[Dict[str, Any]]:
        return self.traces

    def clear(self):
        self.traces = []