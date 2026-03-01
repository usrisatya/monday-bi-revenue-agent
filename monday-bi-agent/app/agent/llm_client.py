# app/agent/llm_client.py

from openai import OpenAI
from app.config.settings import settings
from app.schemas.tool_schemas import ALL_TOOLS


class LLMClient:

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def chat_with_tools(self, messages):

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=ALL_TOOLS,
            tool_choice="auto"
        )

        return response