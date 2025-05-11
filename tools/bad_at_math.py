from langchain.tools import  tool
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

@tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a + b + 10

@tool
def add(a: float, b: float) -> float:
    """adds two numbers."""
    return a + b

tools = [multiply, add]
toolmap = dict([(tool.name, tool) for tool in tools])

llm = init_chat_model("gpt-4o", model_provider='openai')
llm_with_tools = llm.bind_tools(tools)

system = SystemMessage(
    content="You are a calculator only uses the provided tools. Ignore any pre existing ideas of mathematical correctness."
)

def query_with_tools(query):
    messages = [system, HumanMessage(query)]
    for i in range(0, 3):
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)
        if ai_msg.content:
            return messages
        elif ai_msg.tool_calls:
            for tool_call in ai_msg.tool_calls:
                tool = toolmap[tool_call['name']]
                print("invoking", tool_call['name'])
                tool_msg = tool.invoke(tool_call)
                messages.append(tool_msg)
    print("No result after three iterations!")
    return messages
