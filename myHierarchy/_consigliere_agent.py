
from typing import List, Callable, Any, Awaitable

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import Tool
from autogen_ext.models.openai import OpenAIChatCompletionClient



class ConsigliereAgent(AssistantAgent):

    consigliere_thinkTank = OpenAIChatCompletionClient(
        model="deepseek-r1:8b-llama-distill-q4_K_M",
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
            model_client: OpenAIChatCompletionClient = consigliere_thinkTank,
            tools: List[Tool | Callable[..., Any] | Callable[..., Awaitable[Any]]] | None = None,
            description= "A Consigliere Agent whose the close advisor to the Emperor agent. "
                         "This agent helps with research and guidance ",
            system_message = "You are the advisor and research agent to the Emperor and Footmen agents, "
                             "You are more trusted to the Emperor than the Footmen agents. "
                             "Your Emperor agent on your team decides your objective and "
                             "the Footmen agents are the workers who build and execute code. "
                             "You as the Consilgere agent are the close advisor to the Emperor Agent "
                             "and you update the Emperor on the work being done by the Footmen agents. "
                             "You may ask the Emperor agent to request to interact with the user "
                             "to gain additional clarification for your research and advice. "
                             "Reply with TERMINATE to end the conversation."
    ):
        super().__init__(
                name,
                model_client=model_client,
                tools=tools
                or [],
                handoffs=["EmperorAgent", "FootmenCodeAgent", "FootmenWebAgent"],
                description=description,
                system_message=system_message)