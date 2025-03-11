from langgraph.graph import StateGraph, START,END,MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.prompts import ChatPromptTemplate
import datetime
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatBotNode
from src.langgraphagenticai.tools.search_tools import get_tools,create_tool_node
from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode

class GraphBuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(State)
        
    def basic_chatbot_build_graph(self):
        """
        buils a basic chatbot graph using Langgraph
        This method initalizes a chatbot node using the "BasicChatBotNode" class 
        and integrates it into the graph. The Chatbot node is set as both the entry
        and exit point of the graph
        """
        self.basic_chatbot_node = BasicChatBotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)
        
    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node
        and a node tool . It defines tools, initalizes the chatbot with tool 
        capabuilities, and sets up conditional and direct edges between nodes.
        The chatbot node is set as the entry point
        """
        # define the tool and tool node
        tools = get_tools()
        tool_node = create_tool_node(tools)
        
        # define the chatbot node
        obj_chatbot_with_tool_node = ChatbotWithToolNode(self.llm)
        chatbot_node = obj_chatbot_with_tool_node.create_chatbot(tools=tools)
        
        #add nodes
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        # add edges
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        
        
        
        
    def setup_graph(self, usecase: str):
        """
        Set up the graph for the selected use case
        """   
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
            
        if usecase == "Chatbot with Tool":
            self.chatbot_with_tools_build_graph()
            
        return self.graph_builder.compile()
