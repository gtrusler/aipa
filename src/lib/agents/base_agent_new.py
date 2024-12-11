from typing import List, Optional, Union, TypedDict, Annotated, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor
from langchain_core.tools import BaseTool
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langgraph.graph import StateGraph, END
from langchain_core.agents import AgentAction, AgentFinish

class AgentState(TypedDict):
    input: str
    chat_history: List[BaseMessage]
    output: Optional[str]

class BaseAgent:
    def __init__(
        self,
        model_name: str = "claude-3-sonnet-20240229",
        provider: str = "anthropic",
        temperature: float = 0.7,
        tools: Optional[List] = None
    ):
        """Initialize the agent with a model and tools"""
        self.model_name = model_name
        self.provider = provider
        self.temperature = temperature
        self.tools = tools or []
        self.memory = []
        
        # Set up the model
        self.model = self._get_model()
        
        # Set up the agent with tools
        self.agent = self._create_agent()
        
    def _get_model(self):
        """Get the appropriate model based on provider"""
        if self.provider == "anthropic":
            return ChatAnthropic(
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=3072
            )
        elif self.provider == "openai":
            return ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
            
    def _create_agent(self):
        """Create an agent with tools and prompts"""
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant. You have access to the following tools:

{tools}

To use a tool, use the following format:
<tool>tool_name</tool>
<input>tool input</input>

The tool will respond with:
<output>tool output</output>

For example:
<tool>search</tool>
<input>What is the capital of France?</input>
<output>Paris is the capital of France...</output>

Always use tools when they would be helpful in answering the question.
After using tools, provide a comprehensive response that synthesizes the information.
Format your response in a clear and organized manner.

If you want to respond directly without using a tool, simply write your response without any XML tags."""),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Create the final prompt with tools
        prompt_with_tools = prompt.partial(
            tools="\n".join(f"- {tool.name}: {tool.description}" for tool in self.tools)
        )

        def _parse_output(message: str) -> Union[AgentAction, AgentFinish]:
            """Parse the output message to extract tool calls"""
            if "<tool>" not in message:
                return AgentFinish(
                    return_values={"output": message},
                    log=message,
                )
            
            # Extract tool name
            tool_start = message.index("<tool>") + len("<tool>")
            tool_end = message.index("</tool>")
            tool_name = message[tool_start:tool_end].strip()
            
            # Extract input
            input_start = message.index("<input>") + len("<input>")
            input_end = message.index("</input>")
            tool_input = message[input_start:input_end].strip()
            
            return AgentAction(
                tool=tool_name,
                tool_input=tool_input,
                log=message
            )

        def _format_scratchpad(intermediate_steps: List[tuple]) -> List[BaseMessage]:
            """Format intermediate steps for the agent"""
            if not intermediate_steps:
                return []
                
            thoughts = []
            for action, observation in intermediate_steps:
                thoughts.append(f"<tool>{action.tool}</tool>")
                thoughts.append(f"<input>{action.tool_input}</input>")
                thoughts.append(f"<output>{observation}</output>")
            
            return [AIMessage(content="\n".join(thoughts))]

        # Create the agent chain
        agent = (
            {
                "messages": lambda x: x["messages"],
                "agent_scratchpad": lambda x: _format_scratchpad(x.get("intermediate_steps", []))
            }
            | prompt_with_tools
            | self.model
            | _parse_output
        )
        
        # Create agent executor
        return AgentExecutor(agent=agent, tools=self.tools)

    def add_tool(self, tool: Union[Tool, BaseTool]):
        """Add a tool to the agent"""
        self.tools.append(tool)
        self.agent = self._create_agent()

    def add_message(self, message: Union[str, BaseMessage]):
        """Add a message to the agent's memory"""
        if isinstance(message, str):
            message = HumanMessage(content=message)
        self.memory.append(message)

    def process(self, state: AgentState) -> AgentState:
        """Process a message using the agent"""
        messages = self.get_messages(state)
        response = self.agent.invoke({"messages": messages})
        state["output"] = response["output"]
        return state

    def create_graph(self) -> StateGraph:
        """Create a LangGraph for more complex workflows"""
        workflow = StateGraph(AgentState)

        # Define nodes
        workflow.add_node("process", self.process)
        
        # Define edges
        workflow.add_edge("process", END)

        # Set entry point
        workflow.set_entry_point("process")

        # Compile the graph
        workflow.compile()

        return workflow

    def get_messages(self, state: AgentState) -> List[BaseMessage]:
        """Get messages for the agent"""
        messages = []
        
        # Add chat history
        messages.extend(state["chat_history"])
        
        # Add the current input
        messages.append(HumanMessage(content=state["input"]))
        
        return messages
