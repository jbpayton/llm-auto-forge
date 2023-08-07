import sys

from langchain.tools import tool

@tool("example_tool", return_direct=False)
def example_tool(query: str) -> str:
    """This example tool returns the query string back to the console."""
    # note the above docstring in the triple quotes is the description. Each tool MUST have a description.

    try:
        # Put your code here. This is where you will write your tool.
        print(query)

        # Sometimes you will want to write debug statements to the console
        print("This is a debug statement")

        # After it is finished the tool should return a string that is the output of the tool.
        return "Finished running tool."
    except:
        # If there is an error, print the error to the console.
        return "Error: " + str(sys.exc_info())
