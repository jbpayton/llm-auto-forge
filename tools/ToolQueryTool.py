import sys

from langchain.tools import tool
from tools.ToolRegistry import query_unregistered_tools


@tool("tool_query_tool", return_direct=False)
def tool_query_tool(tool_description: str, agent_name: str) -> str:
    """This tool allows an agent to query for available (unregistered) tools given a desired functional description
    and the agent's name. """

    try:
        output = query_unregistered_tools(tool_description, agent_name)

        # After it is finished the tool should return a string that is the output of the tool.
        return output
    except:
        # print the exception
        return str(sys.exc_info())