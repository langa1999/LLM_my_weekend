"""Tutorial from https://langchain-ai.github.io/langgraph/how-tos/tool-calling/#react-agent
More inspiration from: https://towardsdatascience.com/from-basics-to-advanced-exploring-langgraph-e8c1cf4db787
"""
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from PIL import Image
import io

from auth import get_openai_api_key
from functions.railway_api import get_departures_board
from functions.daylight_hours import get_sunrise_sunset
from functions.weather_api import get_weather

openai_api_key = get_openai_api_key()


tools = [get_departures_board, get_sunrise_sunset, get_weather]
tool_node = ToolNode(tools)

model_with_tools = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=1,
    max_retries=2,
    api_key=openai_api_key,
).bind_tools(tools)

model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=1,
    max_retries=2,
    api_key=openai_api_key,
)


def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "translation_agent"


def watersports_node(state: MessagesState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}


def kind_node(state: MessagesState):
    messages = state["messages"]
    messages = [SystemMessage(content="You translate everything to French.")] + messages
    response = model.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(MessagesState)

# Define the nodes we will cycle between
workflow.add_node("agent", watersports_node)
workflow.add_node("tools", tool_node)
workflow.add_node("translation_agent", kind_node)

# Define the edges between nodes
workflow.add_edge(start_key=START, end_key="agent")
workflow.add_edge(start_key="tools",end_key= "agent")
workflow.add_conditional_edges(source="agent", path=should_continue, path_map=["tools", "translation_agent"])
workflow.add_edge(start_key="translation_agent",end_key=END)

app = workflow.compile()

for chunk in app.stream(
        input={"messages": [("human", "What is the wind going to be like if I get the next train fastest to Havant? "
                                      "If I wanted to go do watersports, would I run out of daylight hours?")]},
        stream_mode="values",
):
    chunk["messages"][-1].pretty_print()


image_data = app.get_graph().draw_mermaid_png()
image_file = io.BytesIO(image_data)
img = Image.open(image_file)
img.show()
