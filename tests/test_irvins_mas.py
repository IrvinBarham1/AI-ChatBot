import asyncio
import unittest
from typing import Any, Dict, List

import termination
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

 # Agents
model_client1 = OpenAIChatCompletionClient(
    model="deepseek-r1:14b",
    base_url="http://localhost:11434/v1",
    api_key="placeholder",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "family": "unknown",
    },
)

model_client2 = OpenAIChatCompletionClient(
    model="deepseek-r1:8b",
    base_url="http://localhost:11434/v1",
    api_key="placeholder",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "family": "unknown",
    },
)

emperor = AssistantAgent(
    "emperor_agent",
    model_client=model_client1,
    handoffs=["consigliere", "user"],
    system_message="""You are the emperor agent.
    Your council of agents have collectively agreed upon your leadership and you only recieve power from them.
    If you need information from the User, who is not an agent but a helpful human advisor to your council, you must first send your message, then you can handoff to the user.
    Use TERMINATE when you want to end the conversation.""",
)

consigliere = AssistantAgent(
    "consigliere",
    model_client=model_client2,
    handoffs=["emperor_agent", "user"],
    #tools=[refund_flight],
    system_message="""You are the consigliere to the emperor agent.
    You advise the emperor on matters of importance to the council.
    You have the responsibility to ensure that the emperor's decisions are fair and just.
    However, you must when a decisions are made you must defer to the emperor with respect. 
    If you need information from the user, you must first send your message, then you can handoff to the user.
    When the transaction is complete, handoff to the emperor to finalize.""",
)

termination = HandoffTermination(target="user") | TextMentionTermination("TERMINATE")
team = Swarm([emperor, consigliere], termination_condition=termination)
task = "Hello I am the user, just giving a friendly greeting."

async def run_team_stream() -> None:
    task_result = await Console(team.run_stream(task=task))
    print("Task result: " + str(task_result))
    last_message = task_result.messages[-1]
    print(last_message)

    while isinstance(last_message, HandoffMessage) and last_message.target == "user":
        print("here")
        user_message = input("User: ")

        task_result = await Console(
            team.run_stream(task=HandoffMessage(source="user", target=last_message.source, content=user_message))
        )
        last_message = task_result.messages[-1]

class test_irvins_mas(unittest.TestCase):
      def test_irvins_mas(self):
          # response = asyncio.run(run_team_stream())
          print(asyncio.run(Console(team.run_stream(task=task))))


if __name__ == "__main__":
    unittest.main()
