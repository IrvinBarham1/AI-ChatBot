import asyncio

from autogen_agentchat.conditions import HandoffTermination, MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console

from myHierarchy._consigliere_agent import ConsigliereAgent
from myHierarchy._emperor_agent import EmperorAgent

async def main() -> None:
    emperor_agent = EmperorAgent("emperor_agent" )
    consigliere_agent = ConsigliereAgent("consigliere_agent")

    termination = HandoffTermination(target="user") | MaxMessageTermination(5) | TextMentionTermination("TERMINATE")
    team = Swarm([emperor_agent, consigliere_agent], termination_condition=termination)
# Start the conversation with team.
    await Console(team.run_stream(task="What is Bob's birthday?"))
# Resume with user feedback.
    await Console(
        team.run_stream(
            task=HandoffMessage(source="user", target="emperor_agent", content="Bob's birthday is on 1st January.")
        )
    )

asyncio.run(main())