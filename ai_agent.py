import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START,StateGraph,END
from IPython.display import Image,display

load_dotenv()

llm = OpenAI(model="gpt-3.5-turbo-instruct")

system_message = SystemMessage(content="You are a helpful assistant to answer to general purpose queries.")


def assistant(state: MessagesState):
    return {"messages": state["messages"] + [llm.invoke([system_message] + state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_edge(START,"assistant")
builder.add_edge("assistant",END)

react_graph = builder.compile()

messages = [HumanMessage(content="what is the capital of India?")]
result = react_graph.invoke({"messages": messages})

for m in result["messages"]:
    print(m.content)

