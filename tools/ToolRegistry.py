from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

import importlib.util
import os
import re

import util


class ToolRegistry:
    _instance = None
    _tool_registry = {}
    _tool_data_store = None

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

    def query_unregistered_tools_by_description(self, description, agent_name, tool_path="./AgentTools"):
        if self._tool_data_store is None:
            self._tool_data_store = ToolDataStore(tool_path)

        registered_tools = self._tool_registry.get(agent_name, [])
        registed_tool_names = [tool.name for tool in registered_tools]

        tools = self._tool_data_store.query_description(description)
        unregistered_tools = str(["'Description':" + tool.page_content + "," + str(tool.metadata) for tool in tools if
                                  tool.metadata["tool_name"] not in registed_tool_names])

        return unregistered_tools


def register_tool(tool_function, tool_filename, agent_name, tool_path="./AgentTools"):
    # Parse the module name from the filename
    module_name = os.path.splitext(os.path.basename(tool_filename))[0]
    # Load the module
    spec = importlib.util.spec_from_file_location(module_name, tool_path + "/" + tool_filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Get a reference to the function
    loaded_tool = getattr(module, tool_function)
    # register tool to agent
    ToolRegistry().add_tool(agent_name, loaded_tool)
    # return the description of the tool
    output = loaded_tool.description
    return output


def query_unregistered_tools(description, agent_name, tool_path="./AgentTools"):
    unregistered_tools = ToolRegistry().query_unregistered_tools_by_description(description, agent_name, tool_path)
    tool_message = "The following tools may be helpful, they have not yet been registered and can be registered with " \
                   "the tool_registration_tool:\n" + unregistered_tools
    return tool_message

class ToolDataStore:
    def __init__(self, tool_path="./AgentTools"):

        # Get all the files in the directory
        files = os.listdir(tool_path)

        # initialize the tool list
        tool_list = []
        # Load the tools
        for file in files:
            if file.endswith(".py") and file != "__init__.py" and file != "ToolTemplate.py":
                tool_details = ToolDataStore.parse_py_file(tool_path, file)
                tool_doc = Document(page_content=tool_details["description"],
                                    metadata={"tool_name": tool_details["tool_name"],
                                              "tool_filename": tool_details["tool_filename"]})
                tool_list.append(tool_doc)

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma.from_documents(tool_list, embeddings)

    @staticmethod
    def parse_py_file(tool_path, filename):
        with open(os.path.join(tool_path, filename), 'r') as f:
            content = f.read()

            # Extracting function decorated with @tool
            tool_match = re.search(r'@tool\("([^"]+)"', content)
            if not tool_match:
                raise ValueError("Function is not decorated with @tool")
            tool_function = tool_match.group(1)

            # Extracting docstring
            docstring_match = re.search(r'"""\s*([\s\S]*?)\s*"""', content)
            if not docstring_match:
                raise ValueError("Function does not have a description")
            function_description = docstring_match.group(1).strip()

            return {
                "tool_filename": filename,
                "description": function_description,
                "tool_name": tool_function
            }

    def query_description(self, query):
        return self.vectorstore.similarity_search(query)


if (__name__ == "__main__"):
    register_tool("image_downloader", "ImageDownloader.py", "agent1", tool_path="../AgentTools")
    print(query_unregistered_tools("Make dank memes", "agent1", tool_path="../AgentTools"))

