from langchain.tools import tool

@tool("example_tool", return_direct=True)
def search_api(query: str) -> str:
    """This example tool returns the query string back to the console."""

    # The code below is run when the tool is called.
    print(query)

    #sometimes you will want to write debug statements to the console
    print("This is a debug statement")

    # After it is finished the tool should return a string that is the output of the tool.
    return "Finished running tool."