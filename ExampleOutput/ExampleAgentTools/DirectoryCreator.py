import os

from langchain.tools import tool

@tool("create_directory", return_direct=False)
def create_directory(dir_path: str) -> str:
    """This tool creates a directory."""

    try:
        # Create the directory
        os.makedirs(dir_path, exist_ok=True)

        return 'Finished running tool.'
    except:
        # If there is an error, print the error to the console.
        return 'Error: ' + str(sys.exc_info())