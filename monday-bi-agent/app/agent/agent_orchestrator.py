# app/agent/agent_orchestrator.py

import json
from typing import Dict, Any

from app.agent.llm_client import LLMClient
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tool_registry import ToolRegistry
from app.utils.trace_logger import TraceLogger


class AgentOrchestrator:

    def __init__(self):
        self.llm = LLMClient()
        self.trace_logger = TraceLogger()
        self.tool_registry = ToolRegistry(self.trace_logger)

    def handle_query(self, user_query: str) -> Dict[str, Any]:

        self.trace_logger.clear()

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]

        response = self.llm.chat_with_tools(messages)

        message = response.choices[0].message

        # If tool call required
        if message.tool_calls:

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                tool_result = self.tool_registry.execute(
                    tool_name,
                    arguments
                )

                messages.append(message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result, default=str)
                })

            # Second LLM call to generate final answer
            final_response = self.llm.chat_with_tools(messages)
            final_message = final_response.choices[0].message.content

            return {
                "answer": final_message,
                "traces": self.trace_logger.get_traces()
            }

        # If no tool needed
        return {
            "answer": message.content,
            "traces": []
        }