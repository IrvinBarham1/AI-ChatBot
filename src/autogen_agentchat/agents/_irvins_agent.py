from abc import ABC
from typing import AsyncGenerator, List, Sequence, Tuple

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import AgentEvent, ChatMessage, TextMessage
from autogen_core import CancellationToken


class EmperorAgent(BaseChatAgent, ABC):
    """
        Creating subclass for BaseChatAgent which will be my Emperor Agent.
    """
    def __init__(self, name: str, description: str):
        super().__init__(name, "This is the emperor agent that has the final decision by the power given by the council of agents")
        self.description = description

