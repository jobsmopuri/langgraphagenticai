import streamlit as st 
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
import json

class DisplayResultsStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        
    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        
        if usecase =="Basic Chatbot":
            for event in graph.stream({"messages":("user",user_message)}):
                #print(event.values())
                for value in event.values():
                    print(value["messages"])
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)
                        #Chatbot with Tool
        elif usecase == "Chatbot with Tool":
            # prepare state and invoke the graph
            initial_state = {"messages":[user_message]}
            res = graph.invoke(initial_state)
            for messages in res["messages"]:
                if type(messages) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(messages.content)
                elif type(messages) == ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool call start")
                        st.write(messages.content)
                        st.write("Tool call end")
                elif type(messages) == AIMessage and messages.content:
                    with st.chat_message("assistant"):
                        st.write(messages.content)
            
                
        