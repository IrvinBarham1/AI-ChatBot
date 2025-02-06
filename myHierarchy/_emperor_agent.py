from typing import List, Callable, Any, Awaitable

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import Tool
from autogen_ext.models.openai import OpenAIChatCompletionClient

from myHierarchy._emperor_tools import consult_emperor_tools


class EmperorAgent(AssistantAgent):

    emperor_communication = OpenAIChatCompletionClient(
        model="llama3.2:latest",
        base_url="http://localhost:11434/v1",
        api_key="placeholder",
        model_info={
                "vision": False,
                "function_calling": True,
                "json_output": False,
                "family": "unknown"}
        )

    def __init__(
            self,
            name,
            model_client: OpenAIChatCompletionClient = emperor_communication,
            tools: List[Tool | Callable[..., Any] | Callable[..., Awaitable[Any]]] | None = None,
            description= "An Emperor agent whose the manager of the programing tasks."
                        "You report back to this agent on assigned work. "
                        "Additionally you will use your tools to assist the emperor to complete tasks "
                        ",and research on subject matter the emperor is interested in. "
                        "This is the only agent that can interact with the UserProxyAgent to gain "
                        "additional knowledge to share back to the team.",
            system_message = "You are the leader agent and designate work to your council, "
                             "Your Consigliere agent is the closest advisor to you. "
                             "Your responsibility is to review the work done by the "
                             "consigliere and footmen agents. "
                             "The Consigliere agent will help research subjects that "
                             "are in interest to you as the emperor. "
                             "The footmen agents are your trusted workers to build code "
                             "and to execute tasks assigned to you. All agents who sit under "
                             "you may reach out to you for your help. Additionally, only you have the "
                             "ability to interact with the UserProxyAgent to get an assigned task and to "
                             "gain additional knowledge from the user e.g. if you need information from "
                             "the user not available in tools to pass to your team. "
                             "Reply with TERMINATE to end the conversation."
    ):
        super().__init__(
                name,
                model_client=model_client,
                tools=tools
                or [consult_emperor_tools],
                handoffs=["UserProxyAgent", "ConsigliereAgent", "FootmenCodeAgent", "FootmenWebAgent"],
                description=description,
                system_message=system_message)