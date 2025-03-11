from src.langgraphagenticai.state.state import State

class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with tool integration
    """
    def __init__(self,model):
        self.llm=model
    
    def process(self,state: State) -> dict:
        """
        process the input state nd generates the response with tool integration
        """
        user_inuput = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role":"user","content": user_inuput}])
        
        # simulate the tool specific  logic 
        tools_response = f"Tool Integration for {user_inuput}"
        return {"messages":[llm_response,tools_response]}
    
    def create_chatbot(self,tools):
        """Returns a chatbot node function"""
        
        llm_with_tools = self.llm.bind_tools(tools)
        
        def chatbot_node(state:State):
            """
            chatbot logic for processing the input state and returning a response
            """
            return {"messages": [llm_with_tools.invoke(state["messages"])]}
        return chatbot_node