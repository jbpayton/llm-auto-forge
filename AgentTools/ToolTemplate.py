from langchain.tools import tool

@tool("example_tool", return_direct=False)
def example_tool(query: str) -> str:
    """This example tool returns the query string back to the console."""

    # note the above docstring in the triple quotes is the description. Each tool MUST have a description.

    # The code below is run when the tool is called.
    print(query)

    #sometimes you will want to write debug statements to the console
    print("This is a debug statement")

    # After it is finished the tool should return a string that is the output of the tool.
    return "Finished running tool."