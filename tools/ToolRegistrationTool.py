import sys

from langchain.tools import tool
from tools.ToolRegistry import register_tool


@tool("tool_registration_tool", return_direct=False)
def tool_registration_tool(tool_function: str, tool_filename: str, agent_name: str) -> str:
    """This tool allows an agent to load a tool for its own use given the tool name, tool filename (just the file
    name, no directory), and the agent's name. """

    try:
        output = register_tool(tool_function, tool_filename, agent_name)

        # After it is finished the tool should return a string that is the output of the tool.
        return "Tool Registered successfully: " + output
    except:
        # print the exception
        return str(sys.exc_info())
