from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
import autogen_ext
import asyncio

# print("Version of autogen_ext: ", autogen_ext.__version__)
deepseek_v3_model_client = OpenAIChatCompletionClient(
    model="deepseek-chat",
    api_key="sk-0b013592895948a78f28b12280160bb8",
    base_url="https://api.deepseek.com",
    max_retries=3,
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "unknown",
    }
)

qwen3_8b_model_client = OpenAIChatCompletionClient(
    model="qwen3-8b",
    api_key="sk-16fa569a0dec48aeabd453cf72aa0394",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    max_retries=3,
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "qwen",
        "structured_output": True,
    },
    extra_body={"enable_thinking": False} # 试了半天终于试出来要配置这个项才能关闭思考模式
)

qwen3_8b_wyx_model_client = OpenAIChatCompletionClient(
    model="qwen3-8b-vllm",
    api_key="sk-16fa569a0dec48aeabd453cf72aa0394",
    base_url="http://172.20.137.188:8101/v1",
    max_retries=3,
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "qwen",
        "structured_output": True,
    },
    extra_body={"enable_thinking": False} # 试了半天终于试出来要配置这个项才能关闭思考模式
)

## 测试用函数
async def chat_method(question: str) -> str:
    result = await deepseek_v3_model_client.create([UserMessage(content=question, source="user")])
    print(result)   
#     await deepseek_v3_model_client.close()
#     return result.content

# answer = asyncio.run(chat_method("What is the capital of France?请以json格式返回答案"))
# print(answer)