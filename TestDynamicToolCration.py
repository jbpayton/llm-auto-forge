from langchain import WikipediaAPIWrapper
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from Agents import DialogueAgentWithTools

import util
from langchain.tools import DuckDuckGoSearchRun, Tool, WikipediaQueryRun, PythonREPLTool
from langchain.tools.file_management import WriteFileTool, ReadFileTool

util.load_secrets()

# Define system prompts for our two agents
system_prompt_scribe = SystemMessage(
    role="ToolMaker",
    content="You are a problem solving AI who will create tools for yourself to use to solve problems. Follow all instructions and take as many steps as necessary to solve your problem completely. Before creating "
            "a tool, read './AgentTools/ToolTemplate.py' as it has the proper format "
            "for a langchain tool. Write your own tool into the ./AgentTools folder in a new python file."
)

tools = [ReadFileTool(),
         WriteFileTool(),
         WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
         DuckDuckGoSearchRun(),
         PythonREPLTool()]

# Initialize our agents with their respective roles and system prompts
tool_making_agent = DialogueAgentWithTools(name="ToolMaker",
                                           system_message=system_prompt_scribe,
                                           model=ChatOpenAI(
                                               model_name='gpt-4',
                                               streaming=True,
                                               callbacks=[StreamingStdOutCallbackHandler()]),
                                           tools=tools)

tool_making_agent.receive("HumanUser", "I would like you to write the gettysburg address to a file")

tool_making_agent.send()


print("Done")




