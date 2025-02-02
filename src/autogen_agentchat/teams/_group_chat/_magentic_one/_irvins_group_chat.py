import asyncio

from autogen_core.models import UserMessage, AssistantMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import Swarm
from autogen_agentchat.conditions import HandoffTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import HandoffMessage

# Functions used by organization

async def consult_emperor_tools(args: str):
    print("Emperor has passed these arguments to the tools: ", args)
    emperor_model = OpenAIChatCompletionClient(
        model="deepseek-r1:14b",
        base_url="http://localhost:11434/v1",
        api_key="placeholder",
        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "family": "unknown"}
    )
    response = await emperor_model.create([UserMessage(content=args, source="user")])
    return response.content

def conduct_meeting(args: str):
    pass
def prepare_communication(args: str):
    pass
def work_on_task(args: str):
    pass

async def main() -> None:
    # Defining the organization, agents, and models.
    model_client = OpenAIChatCompletionClient(
        model="llama3.2:latest",
        base_url="http://localhost:11434/v1",
        api_key="placeholder",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": "unknown"}
    )
    model_client2 = OpenAIChatCompletionClient(
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

    emperor_agent = AssistantAgent(
        "Emperor",
        model_client=model_client,
        tools=[consult_emperor_tools],
        handoffs=["user", "consigliere", "footmen"],
        system_message="""You are the emperor agent. 
            Your council of agents have collectively agreed upon your leadership
            and you only receive power from them. If you need information
            from the User, who is not an agent but a helpful human
            advisor who guides you in your purpose to your council,
            you must first send your message, then you can handoff to the user.
            You have your closest advisor agent, the consigliere, to assist you.
            Use TERMINATE when you want to end the conversation.""",
    )

    consigliere = AssistantAgent(
        "consigliere",
        model_client=model_client2,
        handoffs=["emperor_agent", "footmen"],
        tools=[conduct_meeting, prepare_communication],
        system_message="""You are the consigliere to the emperor agent.
        You advise the emperor on matters of importance to the council.
        You have the responsibility to ensure that the emperor's decisions are fair and just.
        However, you must when a decisions are made you must defer to the emperor with respect. 
        If you need information from the user, you must first send your message, then you can handoff to the user.
        When the transaction is complete, handoff to the emperor to finalize.""",
    )

    footman = AssistantAgent(
        "footmen",
        model_client=model_client2,
        handoffs=["consigliere"],
        tools=[work_on_task],
        system_message="""You are the consigliere to the emperor agent.
            You advise the emperor on matters of importance to the council.
            You have the responsibility to ensure that the emperor's decisions are fair and just.
            However, you must when a decisions are made you must defer to the emperor with respect. 
            If you need information from the user, you must first send your message, then you can handoff to the user.
            When the transaction is complete, handoff to the emperor to finalize.""",
    )

    termination = HandoffTermination(target="user") | MaxMessageTermination(15)
    team = Swarm([emperor_agent, consigliere, footman], termination_condition=termination)

    # Start the conversation with Emperor.
    await Console(team.run_stream(task="What is bob's birthday?"))

    # Resume with user feedback.
    await Console(
        team.run_stream(
            task=HandoffMessage(source="user", target="Emperor", content="Bob's birthday is on 1st January.")
        )
    )

    await Console(
        team.run_stream(
            task=HandoffMessage(source="user", target="Emperor", content="Don't you think your footmen should do this job?")
        )
    )

asyncio.run(main())