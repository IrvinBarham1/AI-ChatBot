"""
This module initializes the hierarchy of agents.
"""
from autogen_agentchat.agents import UserProxyAgent
from myHierarchy._emperor_agent import EmperorAgent
from myHierarchy._consigliere_agent import ConsigliereAgent
from myHierarchy._footmen_search_agent import FootmenSearchAgent
from myHierarchy._footmen_code_agent import FootmenCodeAgent

__all__ = [
    "UserProxyAgent",
    "EmperorAgent",
    "ConsigliereAgent",
    "FootmenSearchAgent",
    "FootmenCodeAgent",
]