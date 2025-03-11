from langgraph.graph import StateGraph, START,END,MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.prompts import ChatPromptTemplate
import datetime
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatBotNode

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
        
    def setup_graph(self, usecase: str):
        """
        Set up the graph for the selected use case
        """   
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        return self.graph_builder.compile()
