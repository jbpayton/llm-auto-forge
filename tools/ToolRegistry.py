class ToolRegistry:
    _instance = None
    _tool_registry = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
        return cls._instance

    def set_tools(self, agent_name, tools):
        self._tool_registry[agent_name] = tools

    def get_tools(self, agent_name):
        return self._tool_registry.get(agent_name, [])

    def add_tool(self, agent_name, tool):
        if agent_name not in self._tool_registry:
            self._tool_registry[agent_name] = []
        self._tool_registry[agent_name].append(tool)