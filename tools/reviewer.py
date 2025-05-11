from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
import subprocess
import json

@tool
def read_file(path: str) -> str:
    """Reads a file."""
    print("reading", path)
    return open(path, 'r').read()

def files() -> [str]:
    return subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.splitlines()

tools = [read_file]
toolmap = dict([(tool.name, tool) for tool in tools])

llm = init_chat_model("gpt-4o", model_provider='openai', temperature=0)
llm_with_tools = llm.bind_tools(tools)

system = SystemMessage(
    content="""You are a code reviewer that gives helpful feedback on the code in a given file.

Use the read_file tool to check the contents of the file or any other files from the provided files list.

Make sure imported modules are also correct before giving your review.

Answer only with a json array of objcets containing the 'line' and 'comment' without any markdown formatting."""
)

included_files = ['main.py', 'helpers/numbers.py', 'helpers/strings.py']
def query_with_tools(file):
    file_msg = SystemMessage(f"available files: { json.dumps(included_files) }")
    print("available files:", file_msg)
    messages = [system, file_msg, HumanMessage(file)]
    for i in range(0, 5):
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)
        if ai_msg.tool_calls:
            for tool_call in ai_msg.tool_calls:
                tool = toolmap[tool_call['name']]
                print("invoking", tool_call['name'])
                tool_msg = tool.invoke(tool_call)
                messages.append(tool_msg)
        else:
            return messages
    print("No result after three iterations!")
    return messages

def review(file):
    raw = query_with_tools(file)[-1].content
    parsed = json.loads(raw)
    for comment in parsed:
        print(f"Line {comment['line']}: {comment['comment']}")
