from langchain.tools import tool
import importlib.util
import os
from tools.ToolRegistry import ToolRegistry

@tool("tool_registration_tool", return_direct=False)
def tool_registration_tool(tool_function: str, tool_filename: str, agent_name: str) -> str:
    """This tool allows an agent to load a tool for its own use given the tool function name, tool filename (just the file name, no directory), and the agent's name."""

    # Parse the module name from the filename
    module_name = os.path.splitext(os.path.basename(tool_filename))[0]

    # Load the module
    spec = importlib.util.spec_from_file_location(module_name, "./AgentTools/" + tool_filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get a reference to the function
    loaded_tool = getattr(module, tool_function)

    # register tool to agent
    ToolRegistry().add_tool(agent_name, loaded_tool)


    # After it is finished the tool should return a string that is the output of the tool.
    output = "Tool Registered successfully."
    return output
