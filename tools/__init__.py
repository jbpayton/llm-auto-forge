from langchain.tools import tool
import importlib

@tool("tool_registration_tool", return_direct=True)
def search_api(tool: str, filename: str) -> str:
    """This tool allows an agent to load a tool for its own use given the tool name and tool filename."""

    # The code below is run when the tool is called.
    print(query)

    #sometimes you will want to write debug statements to the console
    print("This is a debug statement")

    # After it is finished the tool should return a string that is the output of the tool.
    return "Finished running tool."