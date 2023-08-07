from langchain import WikipediaAPIWrapper
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI

from prompts import BROWSER_TOOL_MAKER_PROMPT
from Agents import DialogueAgentWithTools

import util
from langchain.tools import WikipediaQueryRun, Tool
from langchain.tools.file_management import WriteFileTool, ReadFileTool
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import (
    create_sync_playwright_browser
)
from langchain.utilities import GoogleSearchAPIWrapper

from tools.ToolRegistrationTool import tool_registration_tool
from tools.ToolQueryTool import tool_query_tool

util.load_secrets()

# Define system prompts for our agent
system_prompt_scribe = BROWSER_TOOL_MAKER_PROMPT

#initialize the browser toolkit
browser = create_sync_playwright_browser()
browser_toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=browser)
browser_tools = browser_toolkit.get_tools()

#initialie search API
search = GoogleSearchAPIWrapper()

def top10_results(query):
    return search.results(query, 10)

GoogleSearchTool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=top10_results,
)

tools = [ReadFileTool(),
         WriteFileTool(),
         WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
         GoogleSearchTool,
         tool_query_tool,
         tool_registration_tool] + browser_tools

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
