import asyncio
import unittest

from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
"""Testing a local model"""

response = None
model_client = OpenAIChatCompletionClient(
    model="llama3.2:latest",
    base_url="http://localhost:11434/v1",
    api_key="placeholder",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "family": "unknown",
    },
)

async def get_response():
    response = await model_client.create([UserMessage(content="Will you be the Emperor of my agents?", source="user")])
    print(response.content)
    return response.content

class TestIrvinsAgent(unittest.TestCase):
    def test_get_response(self):
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(get_response())
        expected_content = " capital of France is Paris."
        self.assertEqual(response, expected_content,f"Expected '{expected_content}', but got '{response}'")


if __name__ == "__main__":
    unittest.main()