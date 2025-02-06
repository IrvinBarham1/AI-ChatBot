from autogen_agentchat.agents import CodeExecutorAgent


class FootmenCodeAgent(CodeExecutorAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "python"