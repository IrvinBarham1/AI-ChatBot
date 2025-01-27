from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, List, Mapping, Sequence

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.state import BaseState
from autogen_core import CancellationToken, ComponentBase

from ..base import ChatAgent, Response, TaskResult
from ..messages import (
    AgentEvent,
    BaseChatMessage,
    ChatMessage,
    TextMessage,
)

class EmperorAgent(BaseChatAgent):
    """
        Creating subclass for BaseChatAgent which will be my Emperor Agent.
    """

    def __init__(
            self,
            name : str,
            description: str,
    ) -> None:
        super().__init__(name=name, description=description)

    @property
    def produced_message_types(self) -> Sequence[type[ChatMessage]]:
        return (TextMessage,)

    async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
        # Calls the on_messages_stream.
        response: Response | None = None
        async for message in self.on_messages_stream(messages, cancellation_token):
            if isinstance(message, Response):
                response = message
        assert response is not None
        return response

    async def on_messages_stream(
        self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken
    ) -> AsyncGenerator[AgentEvent | ChatMessage | Response, None]:
        response = await self.on_messages(messages, cancellation_token)
        for inner_message in response.inner_messages or []:
            yield inner_message
        yield response

    @abstractmethod
    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        """Resets the agent to its initialization state."""
        pass

    async def save_state(self) -> Mapping[str, Any]:
        """Export state. Default implementation for stateless agents."""
        return BaseState().model_dump()

    async def load_state(self, state: Mapping[str, Any]) -> None:
        """Restore agent from saved state. Default implementation for stateless agents."""
        BaseState.model_validate(state)

    async def close(self) -> None:
        """Called when the runtime is closed"""
        pass