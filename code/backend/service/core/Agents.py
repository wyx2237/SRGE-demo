import asyncio
from autogen_agentchat.agents import AssistantAgent
# from autogen_agentchat.messages import StructuredMessage
# from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.base import TaskResult
from autogen_agentchat.teams import SelectorGroupChat


from service.core.Models import deepseek_v3_model_client, qwen3_8b_wyx_model_client, qwen3_8b_model_client

# MODEL_CLIENT = deepseek_v3_model_client # global variable to be used by all agents
# MODEL_CLIENT = qwen3_8b_wyx_model_client # global variable to be used by all agents
MODEL_CLIENT = qwen3_8b_model_client # global variable to be used by all agents


from utils.regex_function import regex_json_parse
def get_agent_response(task_result: TaskResult):
    last_message = task_result.messages[-1]
    content = last_message.content
    # print("llm_answer:", content)
    return content

## 参数抽取智能体
def get_parameter_extractor():
    PARAMETER_EXTRACTOR_PROMPT = """
### 任务说明
你是一个输入参数抽取专家，你的任务是根据我提供的【计算问题】定义(calculator_problem)和已经分析出来的【输入参数字典】(input_params), 从【病人信息】(patient_info)中抽取所需的所有参数值。

### 输出格式，严格遵循json格式，必须包含 input_dict ，input_source_list 和 missing 三个字段，外部以xml标签对封装
<json>
{
    "input_dict": {
        "参数名称1": "参数值1"
        "参数名称2": "参数值2"
        ...
    }, # 输入参数字典，包含所有参数的名称和实际的值
    "input_source_list": [
        { name: '参数名称1', rawValue: '原文表述1', value: 参数值1 },
        { name: '参数名称2', rawValue: '原文表述2', value: 参数值2 },
        ...
    ], # 输入参数字典中所有参数的原文表述和实际值
    "missing": [...] # 缺失参数列表，必须保证为空列表；如果非空，则仔细反思抽取过程，补充缺失参数
}
</json>

### 重要说明
0. 所有参数名称严格参照【输入参数字典】定义中给出的名称。
1. 所有数字类型的抽取参数的抽取结果，其计量单位以参数描述input_desc中给出的单位为准，最终结果不要带单位，并且必须输出数字类型而不是string类型字符串。其中数字类型包括：int、integer、decimal、float等。
2. 所有boolean类型的抽取参数的抽取结果，请统一输出true或false，不要输出其他形式的表示。
3. 第一次抽取完成后，查看结果中是否有空值。对于空值，如果该参数可以从其他参数简单换算得出，请进行换算并填充它的值。例如长度单位cm m inches 可以相互换算。
4. 如果还有结果为空值，做如下处理：数字类型的参数，默认值设为0；boolean类型的参数，默认值设为false；string类型的参数，默认值设为参数描述中提到的第一个值（如果有的话）。
5. input_source_list 中每个参数的 rawValue 字段，必须严格按照原文表述，不能有任何修改（包括大小写、字符顺序等）。

### 反思机制
保证misssing列表为空，如果非空，则仔细反思抽取过程，补充缺失参数，确实找不到的参数值，请参照`重要说明.4` 设为默认值。务必保证【输入参数字典】中所有参有对应的值数都已经，且值都不为空。

### 以下为输入信息
"""
    parameter_extractor_agent = AssistantAgent(
        name="ParameterExtractor",
        model_client=MODEL_CLIENT,
        system_message=PARAMETER_EXTRACTOR_PROMPT,
        output_content_type_format="json"
    )
    return parameter_extractor_agent

# user_input = """
# 【计算问题】
# %s
# 【输入参数字典】
# %s
# 【病人信息】
# %s
# """

DEFAULT_SYSTEM_PROMPT = """你是一个医学领域的计算问题分析专家，请你按照我的要求完成任务"""
def get_general_agent(name: str="GeneralAgent", system_prompt: str=DEFAULT_SYSTEM_PROMPT):
    # ## 通用智能体
    general_agent = AssistantAgent(
        name=name,
        model_client=MODEL_CLIENT,
        system_message=system_prompt,
        output_content_type_format="json"
    )
    return general_agent


def get_calculate_agent():
    CALCULATE_PROMPT = """
### 任务说明
你是一个医学领域的计算问题分析专家，你需要根据一个完整的【计算流程定义】 (Rule)，和【输入参数】（input_dict），通过计算得出最终计算结果，并按照规定格式输出结果。

### 计算过程
请根据 rule 中定义的完整计算流程，按照steps的步骤顺序依次进行计算，并得到最终输出结果。请列出你的完整思考过程

### 输出格式，严格遵循json格式，必须包含 result 字段，外部以xml标签对封装
<json>
{
    "final_result": 计算结果 （注意数字类型的结果应保持为数字而不是字符串）
}
</json>

### 输出示例
<json>
{   
    "thinking_process": "1. 首先根据规则，确定计算流程...\n2. 然后根据输入参数，进行计算....\n3. 最后得到最终结果...",
    "final_result": 123.45
}
</json>

### 以下为输入信息
"""

    calculate_agent = AssistantAgent(
        name="CalculateAgent",
        model_client=MODEL_CLIENT,
        system_message=CALCULATE_PROMPT,
        output_content_type_format="json"
    )
    return calculate_agent

