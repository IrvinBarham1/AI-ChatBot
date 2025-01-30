import asyncio

import pytest
from autogen_agentchat import messages
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from src.autogen_agentchat.agents._countdown_agent import run_countdown_agent, CountDownAgent

@pytest.mark.asyncio
async def test_basic_chat_agent() -> None:
    agent = CountDownAgent(name="countdown", count=5)

    messages = [
        TextMessage(
             content="jofgejgeogp".strip(),
            source="assistant",
     )
  ]
    response = await agent.on_messages(messages, CancellationToken())
    assert isinstance(response, Response)
    assert isinstance(response.chat_message, TextMessage)
    await run_countdown_agent(agent)