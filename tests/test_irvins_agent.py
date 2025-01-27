import pytest

from src.autogen_agentchat.agents import EmperorAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

@pytest.mark.asyncio
async def test_irvins_agent_execution() -> None:
    """Test Irvin's Agent"""

    agent = EmperorAgent(name="Emperor", description=
    "Emperor Agent that receives its power from the council of agents. It is the leader, the emperor.")

    response = await agent.on_messages(
        [TextMessage(content="What is your objective Emperor?", source="user")],
        cancellation_token=CancellationToken(),
    )
    print(response.inner_messages)
    print(response.chat_message)

    await test_irvins_agent_execution()
    await agent.on_reset(CancellationToken())
    assert agent.name == "Emperor"