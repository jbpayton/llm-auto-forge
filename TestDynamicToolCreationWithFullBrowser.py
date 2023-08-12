from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI

from prompts import BROWSER_TOOL_MAKER_PROMPT
from Agents import DialogueAgentWithTools

import util
from langchain.tools import Tool
from langchain.agents.agent_toolkits import FileManagementToolkit

from langchain.utilities import GoogleSearchAPIWrapper

from tools.ToolRegistrationTool import tool_registration_tool, query_available_modules
from tools.ToolQueryTool import tool_query_tool
from tools.LLMBrowsingTools import query_website, paged_web_browser

util.load_secrets()

# Define system prompts for our agent
system_prompt_scribe = BROWSER_TOOL_MAKER_PROMPT

# initialize file management tools
file_tools = FileManagementToolkit(
    selected_tools=["read_file", "write_file", "list_directory", "copy_file", "move_file", "file_delete"]
).get_tools()


# initialie search API
search = GoogleSearchAPIWrapper()

def top10_results(query):
    return search.results(query, 10)

GoogleSearchTool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=top10_results,
)

tools = [GoogleSearchTool,
         tool_query_tool,
         tool_registration_tool,
         query_available_modules,
         paged_web_browser,
         ] + file_tools

# Initialize our agents with their respective roles and system prompts
tool_making_agent = DialogueAgentWithTools(name="ToolMaker",
                                           system_message=system_prompt_scribe,
                                           model=ChatOpenAI(
                                               model_name='gpt-4',
                                               streaming=True,
                                               temperature=0.0,
                                               callbacks=[StreamingStdOutCallbackHandler()]),
                                           tools=tools)

tool_making_agent.receive("HumanUser", "Can you tell me what is in this image and add an in-picture caption to this "
                                       "image? ./TestInput/mystery_image.jpg Write the captioned image to "
                                       "./TestOutput/captioned_image.jpg")

tool_making_agent.send()

print("Done")
