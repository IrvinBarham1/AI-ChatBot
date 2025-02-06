from autogen_ext.agents.web_surfer import MultimodalWebSurfer


class FootmenSearchAgent(MultimodalWebSurfer):
    def __init__(self, footmen_search_algorithm):
        self.footmen_search_algorithm = footmen_search_algorithm