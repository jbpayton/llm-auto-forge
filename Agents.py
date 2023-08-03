from typing import List

from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage, HumanMessage, AIMessage

from tools.ToolRegistry import ToolRegistry

class DialogueAgent:
    def __init__(
        self,
        name: str,
        system_message: SystemMessage = None,
        model: ChatOpenAI = None,
    ) -> None:
        self.name = name
        self.system_message = system_message
        self.model = model
        self.prefix = f"{self.name}: "
        self.reset()

    def reset(self):
        self.message_history = ["Here is the conversation so far."]

    def send(self) -> str:
        if self.model and self.system_message:
            print(f"{self.name}: ")
            message = self.model(
                [
                    self.system_message,
                    HumanMessage(content="\n".join(self.message_history + [self.prefix])),
                ]
            )
            return message.content
        else:
            raise NotImplementedError

    def receive(self, name: str, message: str) -> None:
        self.message_history.append(f"{name}: {message}")


class DialogueAgentWithTools(DialogueAgent):
    def __init__(
        self,
            name: str,
            system_message: SystemMessage,
            model: ChatOpenAI,
            tools: List,
    ) -> None:
        super().__init__(name, system_message, model)
        ToolRegistry().set_tools(name, tools)
        self.tools = tools

    def send(self) -> str:
        """
        Applies the chatmodel to the message history
        and returns the message string
        """
        agent_chain = initialize_agent(
            self.tools,
            self.model,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=99,
            memory=ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            ),
        )
        message = AIMessage(
            content=agent_chain.run(
                input="\n".join(
                    [self.system_message.content] + self.message_history + [self.prefix]
                )
            )
        )

        return message.content


class UserAgent(DialogueAgent):
    def send(self) -> str:
        message = input(f"\n{self.prefix}")
        return message