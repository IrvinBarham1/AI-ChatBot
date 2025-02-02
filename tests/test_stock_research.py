import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import Swarm
from autogen_agentchat.conditions import HandoffTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import HandoffMessage


async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        model="deepseek-r1:8b",
        base_url="http://localhost:11434/v1",
        api_key="placeholder",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": "unknown"}
    )

    agent = AssistantAgent(
        "Alice",
        model_client=model_client,
        handoffs=["user"],
        system_message="You are Alice and you only answer questions about yourself, ask the user for help if needed.",
    )
    termination = HandoffTermination(target="user") | MaxMessageTermination(3)
    team = Swarm([agent], termination_condition=termination)

    # Start the conversation.
    await Console(team.run_stream(task="What is bob's birthday?"))

    # Resume with user feedback.
    await Console(
        team.run_stream(
            task=HandoffMessage(source="user", target="Alice", content="Bob's birthday is on 1st January.")
        )
    )


asyncio.run(main())