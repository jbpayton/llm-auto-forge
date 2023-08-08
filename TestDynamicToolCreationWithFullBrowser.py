from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI

from prompts import BROWSER_TOOL_MAKER_PROMPT
from Agents import DialogueAgentWithTools

import util
from langchain.tools import Tool
from langchain.agents.agent_toolkits import FileManagementToolkit
from tools.playwrightMod.toolkit import PlayWrightBrowserToolkit

from tools.playwrightMod.utils import (
    create_sync_playwright_browser
)
from langchain.utilities import GoogleSearchAPIWrapper

from tools.ToolRegistrationTool import tool_registration_tool
from tools.ToolQueryTool import tool_query_tool

util.load_secrets()

# Define system prompts for our agent
system_prompt_scribe = BROWSER_TOOL_MAKER_PROMPT

# initialize file management tools
file_tools = FileManagementToolkit(
    selected_tools=["read_file", "write_file", "list_directory", "copy_file", "move_file", "file_delete"]
).get_tools()

# initialize the browser toolkit
browser = create_sync_playwright_browser()
context = browser.new_context(
  user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
)

browser_toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=browser)
browser_tools = browser_toolkit.get_tools()

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
         tool_registration_tool] + file_tools + browser_tools

# Initialize our agents with their respective roles and system prompts
tool_making_agent = DialogueAgentWithTools(name="ToolMaker",
                                           system_message=system_prompt_scribe,
                                           model=ChatOpenAI(
                                               model_name='gpt-4',
                                               streaming=True,
                                               temperature=0.0,
                                               callbacks=[StreamingStdOutCallbackHandler()]),
                                           tools=tools)

tool_making_agent.receive("HumanUser", "Create a meme image of a cat with funny bottom text and top text.")

tool_making_agent.send()

print("Done")
