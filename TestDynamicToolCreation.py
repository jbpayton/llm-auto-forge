from langchain import WikipediaAPIWrapper
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from Agents import DialogueAgentWithTools

import util
from langchain.tools import DuckDuckGoSearchRun, Tool, WikipediaQueryRun, PythonREPLTool
from langchain.tools.file_management import WriteFileTool, ReadFileTool
from tools.ToolRegistrationTool import tool_registration_tool

util.load_secrets()

# Define system prompts for our agent
system_prompt_scribe = SystemMessage(
    role="ToolMaker",
    content="You are a problem solving AI who will create tools and use them to solve problems. Think step by step and follow all "
            "instructions to solve your problem completely. Make sure to follow all of the following rules: \n"
            "1. Only create tools if you do not have tools to perform the task.\n "
            "2. If you already have a tool to perform the task, use it.\n\n "
            "If you need to create a tool, follow these steps: \n"
            "1. If you need to create a tool, read './AgentTools/ToolTemplate.py' as it is a helpful example of a langchain tool.\n "
            "2. Write your own tool into the ./AgentTools folder in a new python file. Name the tool file something descriptive and "
            "also make the tool and function name match (it makes life easier). Also remember the tool must hav a description.\n "
            "3. Afterwards, register it with the tool registration tool. \n"
            "4. After a tool is made, use your tool to solve the problem."
)

tools = [ReadFileTool(),
         WriteFileTool(),
         WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
         DuckDuckGoSearchRun(),
         tool_registration_tool]

# Initialize our agents with their respective roles and system prompts
tool_making_agent = DialogueAgentWithTools(name="ToolMaker",
                                           system_message=system_prompt_scribe,
                                           model=ChatOpenAI(
                                               model_name='gpt-4',
                                               streaming=True,
                                               callbacks=[StreamingStdOutCallbackHandler()]),
                                           tools=tools)

tool_making_agent.receive("HumanUser", "Write the first sentence of the gettysburg address to a file (create a tool to do this).")

tool_making_agent.send()

print("Done")




