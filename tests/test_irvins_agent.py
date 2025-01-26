import pytest
from autogen_agentchat.agents import EmperorAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor


@pytest.mark.asyncio
async def test_irvins_agent_execution() -> None:
    """Test Irvins Agent"""

    agent = EmperorAgent(name="Emperor", code_executor=LocalCommandLineCodeExecutor())

    messages = [
        TextMessage(
            content="""
```
Hello Emperor, how do you wish to prove yourself as king!
```
""".strip(),
            source="assistant",
        )
    ]
    response = await agent.on_messages(messages, CancellationToken())

    assert isinstance(response, Response)
    assert isinstance(response.chat_message, TextMessage)
    assert response.chat_message.content.strip() == "6.481"
    assert response.chat_message.source == "code_executor"

