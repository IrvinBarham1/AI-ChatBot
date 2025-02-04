import asyncio

from autogen_core.models import UserMessage, AssistantMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import Swarm, SelectorGroupChat
from autogen_agentchat.conditions import HandoffTermination, MaxMessageTermination, TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import HandoffMessage
# Functions used by organization

emperor_agent = NotImplemented

async def consult_emperor_tools(args: str):
    print(">>> Emperor has passed these arguments to the tools: " + args)
    emperor_model = OpenAIChatCompletionClient(
        model="deepseek-r1:8b-llama-distill-q4_K_M",
        base_url="http://localhost:11434/v1",
        api_key="placeholder",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": "unknown"}
    )
    emperor_tool_agent = AssistantAgent(
        "emperor_tools",
        model_client=emperor_model,
        handoffs=["emperor_agent"],
        system_message="""You are the tools for the emperor agent. 
                   You are the representation of the working mind of the emperor.
                   If you don't have an answer, handoff to emperor_agent to obtain help from user.
                   When the transaction is complete, handoff to the emperor_agent to finalize.""",
    )
    termination = HandoffTermination(target="Emperor") | MaxMessageTermination(4)
    team = SelectorGroupChat([emperor_tool_agent, emperor_agent],emperor_model,
                    termination_condition=termination)
    print(">>> Emperor is working with his tools.")
    task =  HandoffMessage(source="emperor_agent", target="emperor_tools", content="I need to consult you emperor tools here's my arguments: " + args)
    return await Console(team.run_stream(task=task))
   # return await emperor_model.create([AssistantMessage(content=args, source="emperor_agent")])

async def prepare_research(args: str):
    print(">>> Consigliere has passed these arguments to prepare research: ", args)
    footmen_model = OpenAIChatCompletionClient(
        model="llama3.2:latest",
        base_url="http://localhost:11434/v1",
        api_key="placeholder",
        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "family": "unknown"}
    )
    response = await footmen_model.create([AssistantMessage(
        content="The Consigliere has passed the following args because it need to use its tools to prepare research: " + args, source="consigliere_agent")])
    return response.content

async def work_on_task(args: str):
    print(">>> Footmen has passed these arguments to work on task: ", args)
    footmen_model = OpenAIChatCompletionClient(
        model="deepseek-r1:1.5b",
        base_url="http://localhost:11434/v1",
        api_key="placeholder",
        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "family": "unknown"}
    )
    response = await footmen_model.create([AssistantMessage(content=args, source="emperor_agent")])
    return response.content


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
    global emperor_agent
    emperor_agent = AssistantAgent(
        "emperor_agent",
        model_client=model_client,
        tools=[consult_emperor_tools],
        handoffs=["user", "consigliere", "footmen"],
        system_message="""You are the emperor agent. 
               Your council of agents have collectively agreed upon your leadership
               and you only receive power from them. If you need information
               from the User not available in tools, then you can handoff to the user.
               Additionally, you have your closest advisor agent, the consigliere_agent.
               When the transaction is complete, handoff to the User to finalize.
               Use TERMINATE to end the conversation.""",
    )

    consigliere_agent = AssistantAgent(
        "consigliere_agent",
        model_client=model_client2,
        handoffs=["emperor_agent", "footmen"],
        tools=[prepare_research],
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
        handoffs=["emperor_agent", "consigliere"],
        tools=[work_on_task],
        system_message="""You are the footmen of the emperor agent.
               You complete tasks assigned by the emperor agent.
               If you need information from the emperor or consigliere, you must first send your message, 
               then you can handoff to the emperor or consigliere.
               When the transaction is complete, handoff to the emperor or consigliere to finalize.""",
    )

    termination = HandoffTermination(target="user") | MaxMessageTermination(5) | TextMentionTermination("TERMINATE")
    team = Swarm([emperor_agent, consigliere_agent, footman], termination_condition=termination)

    # Start the conversation with Emperor.
    await Console(team.run_stream(task="What is Bob's birthday?"))

    # Resume with user feedback.
    task = await Console(
        team.run_stream(
            task=HandoffMessage(source="user", target="emperor_agent", content="Bob's birthday is on 1st January.")
        )
    )

    task = HandoffMessage(source="user", target="emperor_agent",
                          content="Prepare a short 2 sentence research on the topic of AI.")
    await Console(team.run_stream(task=task))

asyncio.run(main())