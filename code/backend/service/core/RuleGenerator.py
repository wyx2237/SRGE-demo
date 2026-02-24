from service.core.atomic_tool.Category import CategoryDict
# from utils.model_request import chat_method
import json
from utils.regex_function import *
from service.core.Agents import get_agent_response, get_general_agent   
from service.core.CalculateFlow import CalculateFlow

MAX_TRY_TIMES = 3


async def question_analyze_wo_atomic(question:str) -> str:
    """
    消融了原子工具模板
    """
    analyze_prompt = """
### 任务说明
你是一个医学领域的计算问题分析专家，你需要对【待计算问题】进行分析，将其拆解为一组独立子步骤，并严格按照规定的格式输出。
对于每个步骤，请列出我要求的【步骤信息】, 并且你需要保证这些步骤能够组合为一个完整的计算流程，给出【步骤组合的流程示意】。

### 步骤信息
Name: 步骤名称——描述当前步骤的名称
Description：步骤描述——描述当前步骤的目标、过程等信息
Inputs: 步骤输入——描述当前步骤的全部输入信息（参数名、类型、描述）
Outputs: 步骤输出——描述当前步骤的全部输出信息（参数名、类型、描述）
Detail: 步骤详情——描述当前步骤的详细计算方式细节
Reasoning: 拆解原因——解释为什么把这个步骤单独拆解


### 重要说明
禁止生成类似"从文本中获取数据"此类的无效步骤，每个步骤的输入变量与输出都应是明确的

### 输出格式 (JSON格式, 以xml标签对<json></json>封装)
# 输出1 步骤列表
<json>
[ 步骤1, 步骤2, ...] 
</json>

# 输出2 步骤组合的流程示意
<workflow>
(inputs(param1, param2,...) -> step1:Name(param1, param2,...) -> step2:Name(param1, param2,...) ->... -> outputs(result)
</workflow>

### 待计算问题
%s

""" % (question)
    agent = get_general_agent(name="QuestionAnalyzer")
    task_result = await agent.run(task=analyze_prompt)
    analyze_result = get_agent_response(task_result)

    # analyze_result = chat_method(analyze_prompt)
    # print(analyze_result)
    steps_result_dict = regex_json_parse(analyze_result)
    flow_result = regex_workflow(analyze_result)
    # print(steps_result_dict)
    # print(flow_result)
    del agent

    return {
        "steps_result_dict": steps_result_dict,
        "flow_result": flow_result
    }

async def question_analyze(question:str) -> dict:
    """
    输入问题，按照工具模板进行检测，输出 步骤清单+流程示意
    """

    analyze_prompt = """
### 任务说明
你是一个医学领域的计算问题分析专家，你需要根据我给出的以下【工具模板清单】，对【待计算问题】进行分析和步骤拆解
对于每一个拆解后的子步骤，你需要从【工具模板清单】中选出最贴合当前步骤的工具模板，作为当前步骤的所属类型Category，并且需要给出选取该工具模板的理由Reasoning。
对于每个符合的特定工具模版的步骤，请列出我要求的【步骤信息】, 并且你需要保证这些步骤能够组合为一个完整的计算流程，给出【步骤组合的流程示意】。
最后，反思当前的步骤先后顺序是否存在问题，并进行相应的调整，确保步骤组合的合理性。

### 工具模板清单
%s

<SplitLine>

类别：Other
如果不符合以上工具模板，请选择 Other 类别。

### 步骤信息
Category: 所属工具模板——列出所属的工具模板的标准名称（只能一个，并且必须从【工具模板清单】中选择）
Name: 步骤名称——描述当前步骤的名称
Description：步骤描述——描述当前步骤的目标、过程等信息
Inputs: 步骤输入——描述当前步骤的全部输入信息（参数名、类型、描述）
Outputs: 步骤输出——描述当前步骤的全部输出信息（参数名、类型、描述）
Detail: 步骤详情——描述当前步骤的详细计算方式细节
Reasoning: 归类原因——解释为什么把这个步骤归类到这一工具模板下

### 重要说明
 - 禁止生成类似"从文本中获取数据"此类的无效步骤，每个步骤的输入变量与输出都应是明确的
 - 拆分的步骤不应超过5个，否则可能导致计算流程过长，不易理解（对于简单的分点累积计分的问题，可以考虑合并为一个步骤）
 - 每个步骤的输出尽量为单一值，只有在特定要求下才需要dict等复合结构。（例如，对于累积计分问题，步骤内部可以直接输出累积值，而不需要输出每一项的分值）


### 输出格式 
# 输出1 步骤列表 (JSON格式, 以xml标签对<json></json>封装)
<json>
[ 步骤1, 步骤2, ...] 
</json>

# 输出2 步骤组合的流程示意 (以xml标签对<workflow></workflow>封装)
<workflow>
(inputs(param1, param2,...) -> step1:Name(param1, param2,...) -> step2:Name(param1, param2,...) ->... -> outputs(result)
</workflow>

### 输出示例
<json>
[
    {
        "Category": "Category1",
        "Name": "Name1",
        "Description": "Description1",
        "Inputs": [
            {
                "input_name": "input_name1",
                "input_desc": "input_desc1",
                "input_type": "input_type1"
            }
        ],
        "Outputs": [
            {
                "output_name": "output_name1",
                "output_desc": "output_desc1",
                "output_type": "output_type1"
            }
        ],
        "Detail": "Detail1...",
        "Reasoning": "Reasoning1"
    },
    ...
]
</json>

<workflow>
(inputs(input_name1, input_name2,...) -> step1:Name1(input_name1, input_name2,...) -> step2:Name2(input_name1, input_name2,...) ->... -> outputs(output_name1, output_name2,...)
</workflow>


### 待计算问题
%s

""" % ("\n<SplitLine>\n".join([c['general'] for c in CategoryDict.values()]), question)
    agent = get_general_agent(name="QuuestionAnalyzer")


    # analyze_result = chat_method(analyze_prompt)
    # print(analyze_result)
    try_times = 0
    while try_times < MAX_TRY_TIMES:
        task_result = await agent.run(task=analyze_prompt)
        analyze_result = get_agent_response(task_result)
        # print(f"analyze_result:\n{analyze_result}")
        steps_result_dict = regex_json(analyze_result)
        # print(f"steps_result_dict:\n{steps_result_dict}")
        # steps_result_dict = regex_json_parse(analyze_result)
        if steps_result_dict is not None:
            break
        try_times += 1

    flow_result = regex_workflow(analyze_result)
    if flow_result is None:
        raise ValueError("question analyze failed")
    # print(steps_result_dict)
    # print(flow_result)
    del agent

    return {
        "steps_result_dict": steps_result_dict,
        "flow_result": flow_result
    }

async def flow_compose(question:str, steps_result_dict:dict, flow_result:str) -> str:
    """
    输入步骤清单，按照流程示意进行流程组合，输出结构化的计算流程表示（初始化）
    """

    ## 对于生成的每个步骤，尝试组合成一个完整的计算流程，实现对输入问题的计算
    compose_prompt = """
### 任务说明
你是一个医学领域的计算问题分析专家，你需要根据我给出的【计算问题】以及根据该【计算问题】生成的一组【规范化步骤表示】，组合成一个能够完成该计算问题的完整输入输出流程表示，并按照【计算流程】格式输出
最后请全部以**英文**输出结果。 （please output in English.）

### 计算流程格式 （以JSON格式输出，此处是等价的表示形式）
name: 计算流程名称
description: 计算流程描述
inputs: 输入参数
    - input_name: 输入参数名称，只允许小写字母、数字、下划线组成，且必须以字母开头，蛇形命名法
    - input_desc: 输入参数描述，对于存在计量单位的输入参数，请明确说明其单位；对于存在枚举值的参数（主要是string类型的参数），请列出所有枚举值，并且枚举值应尽可能以简洁易懂的方式表示，不应过长
    - input_type: 输入参数类型 

steps: 计算步骤
    - step_id: 步骤编号(从1开始，1,2,3,... 递增) str类型
      step_name: 步骤名称
      step_description: 步骤描述
      step_inputs: 步骤输入
        - input_name: 输入参数名称，只允许小写字母、数字、下划线组成，且必须以字母开头，蛇形命名法
          input_desc: 输入参数描述，对于存在计量单位的输入参数，请明确说明其单位；对于存在枚举值的参数（主要是string类型的参数），请列出所有枚举值
          input_type: 输入参数类型 

      step_outputs: 步骤输出
        - output_name: 输出参数名称，只允许小写字母、数字、下划线组成，且必须以字母开头，蛇形命名法
          output_desc: 输出参数描述
          output_type: 输出参数类型
          
      category: 所属类别
      reason: 归类原因——解释为什么把这个步骤归类到这一工具模板下
      detail：步骤详细计算过程

output: 输出结果（只有一个，dict形式）
    output_name: 输出参数名称，只允许小写字母、数字、下划线组成，且必须以字母开头，蛇形命名法
    output_desc: 输出参数描述
    output_type: 输出参数类型

### 重要说明
生成计算流程时，请仔细思考并确认，每一个计算步骤的输入参数、输出参数是否合理，是否能够完成该步骤的计算。在所有步骤的输入参数确认完毕后，最后再确认计算流程的初始输入参数有哪些以及如何定义。
每一个计算步骤的输入参数，可能来自于计算流程的初始输入，也可能来自于前置步骤的输出，或者可能是该步骤自己设置的默认输入。

### 输出格式 （JSON格式，以xml标签对<json></json>封装）
<json>
（你生成的计算流程）
</json>


### 输出示例
<json>
{
    "name": "name1",
    "description": "decs1...",
    "inputs": [
        {
            "input_name": "input_name1",
            "input_desc": "input_desc1",
            "input_type": "input_type1"
        }
    ],
    steps: [
        {
            "step_id": "1",
            "step_name": "step_name1",
            "step_description": "step_desc1",
            "step_inputs": [
                {
                    "input_name": "input_name1",
                    "input_desc": "input_desc1",
                    "input_type": "input_type1"
                }
            ],
            "step_outputs": [
                {
                    "output_name": "output_name1",
                    "output_desc": "output_desc1",
                    "output_type": "output_type1"
                }
            ],
            "category": "category1",
            "detail": "detail1..."
        }
    ],
    "output": {
        "output_name": "output_name1",
        "output_desc": "output_desc1",
        "output_type": "output_type1"
    }
}
<json>
### 计算问题
%s

### 规范化步骤表示
%s

""" % (question, steps_result_dict)
    agent = get_general_agent(name="FlowComposer")
    task_result = await agent.run(task=compose_prompt)
    calculate_flow = get_agent_response(task_result)
    # print("calculate_flow:\n")
    # print(calculate_flow)
    # print(len(calculate_flow))
    # print(type(calculate_flow))

    # calculate_flow = chat_method(compose_prompt)
    # print(calculate_flow)
    calculate_flow_dict = regex_json_parse(calculate_flow)
    # calculate_flow_dict = json.loads(calculate_flow)
    # print(calculate_flow_dict)
    del agent

    return {
        "calculate_flow_dict": calculate_flow_dict,
        # "steps": calculate_flow_dict.get("steps", []),
    }

# 更新步骤之间的输入输出流设置
async def step_dataflow_update(calculate_flow_dict:dict):
    """
    输入计算流程，更新步骤之间的输入输出流设置，输出更新后的计算流程，并保存到文件
    """

    data_flow_prompt = """
### 任务说明
你是一个计算数据分析专家，你需要在我给出的【上下文字典】context 中，找到【当前步骤】的输入参数的值的来源，并更新【当前步骤】的字段设置。

### 更新字段
step.inputs 中每个输入参数，需要从 context 中找到其来源，并更新其字段设置如下：
    input_name: (保持不变)
    input_desc: (保持不变)
    input_type: (一般情况下保持不变，但是在确定引用来源对应的参数时，如果类型与被引用的参数类型不一致，需要将input_type更新为被引用的那个参数的类型)
    input_source: (新增) $|inputs|.xxx 或者 $|1|.xxx 、$|2|.xxx 或者 null
说明：
    $|| 代表上下文字典的引用，inputs 和 数字（即step_id） 为上下文字典的 key，即你需要从context中找到当前步骤的输入是从初始输入(inputs)中获取还是从其他步骤的输出中获取。xxx 为输入参数的名称。
例如：
    input_source: $|inputs|.gender 表示当前步骤的输入参数gender来源于初始输入参数inputs中的input_name为gender的那个参数。
    input_source: $|1|.gender 表示当前步骤的输入参数gender来源于步骤1的输出结果中的output_name为gender的那个参数。
限制：
    $||引用的key必须存在于上下文字典context中，且key必须与context中定义的参数名完全一致。
    例如 context 中有 inputs:[{input_name: "weight_category", input_desc: "Patient's weight category", input_type: "string"}]，则 $|inputs|.weight_category 引用的key必须为 "weight_category"，而不能为 "weight_type"

反思：
    最终的输入参数设置中 input_type必须与被引用的参数类型一致，否则需要更新input_type为被引用的参数类型；如果input_source为null，则需要设置默认值。

### 输出格式 （JSON格式，以xml标签对<json></json>封装）
<json>
（更新后的step）
</json>

### 输出示例
<json>
{
    "step_id": "7",
    "step_name": "calculate_diabetes_score",
    "step_description": "Determine points based on diabetes history",
    "step_inputs": [
        {
            "input_name": "diabetes_history",
            "input_desc": "Presence of diabetes history",
            "input_type": "boolean"
            "input_source": "$|inputs|.diabetes_history"
        }
    ],
    "step_outputs": [
        {
            "output_name": "diabetes_score",
            "output_desc": "Points from diabetes category (0 or 1)",
            "output_type": "integer"
        }
    ],
    "category": "score_calculation",
    "detail": "Yes = +1 point, No = 0 points"
}
</json>

### 上下文字典示例
{
    "inputs": [
        {
            "input_name":"gender", # 引用这个参数时，使用 $|inputs|.gender
            "input_desc":"Patient's gender",
            "input_type":"string"
        }
        ...
    ],
    "1": [
        {
            "output_name": "gender", # 引用这个参数时，使用 $|1|.gender
            "output_desc": "...",
            "output_type": "string"
        },
        {
            "output_name": "age_list", # 引用这个参数时，使用 $|1|.age_list
            "output_desc": "...",
            "output_type": "list"
        }
        ...
    ]
}

### 引用示例
# 示例1
{
    "input_name": "gender",
    "input_desc": "Patient's gender",
    "input_type": "string",
    "input_source": "$|inputs|.gender"
}

# 示例2
{
    "input_name": "age_list",
    "input_desc": "Patient's age list",
    "input_type": "list", # 注意这里的类型是list , 因为引用的age_list参数类型是list
    "input_source": "$|1|.age_list"
}
### 上下文字典
%s

### 当前步骤
%s
"""
    # context = {"inputs": calculate_flow_dict.get("inputs",[])}
    context = {"inputs": [p["input_name"] for p in calculate_flow_dict["inputs"]]}
    steps = calculate_flow_dict.get("steps", [])
    steps_with_source = []
    calflow = CalculateFlow(flow_definition={})
    ## 更新输入输出流设置
    for step in steps:
        prompt = data_flow_prompt % (context, step)
        # print(f"prompt:\n{prompt}\n")
        try_times = 0
        add_info = "\nadd_info\n:"
        while try_times < MAX_TRY_TIMES: 
            try_times += 1

            agent = get_general_agent(name="DataFlowUpdater")
            task_result = await agent.run(task=prompt+add_info)
            step_result = get_agent_response(task_result)
            # step_result = chat_method(prompt)
            updated_step = regex_json_parse(step_result)
            if updated_step is None:
                continue
            # print(f"updated_step:\n{updated_step}\n")

            # 检测当前步骤所有引用参数是否在上下文中已经存在
            try:
                calflow._validate_inputs_for_step(updated_step, context)
                break
            except Exception as e:
                # raise e
                add_info = f"\nadd_info\n:step_id:{str(e)}， 请避免这个错误，并重新生成"
                print(add_info)
                continue


        print(f"updated_step:\n{updated_step}\n")
        step_id = step.get("step_id") # 小心 步骤编号 和上下文字典表示问题 导致计算时无法取到参数

        # 更新上下文字典，添加当前步骤的输出到上下文字典
        context.update({step_id: [p["output_name"] for p in step["step_outputs"]]})
        # context.update({step_id: [p["output_name"] for p in step["step_outputs"]]})

        steps_with_source.append(updated_step)
        del agent

    # 最后更新最终输出的引用
    final_output = calculate_flow_dict.get("output")
    # print(steps_with_source)
    output_source = f"$|{len(steps_with_source)}|." + steps_with_source[-1].get("step_outputs")[0].get("output_name")
    # print(output_source)
    final_output.update({"output_source":output_source})
    calculate_flow_dict.update({"steps": steps_with_source, "output":final_output})

    return {
        "calculate_flow_dict": calculate_flow_dict,
        # "steps": steps_with_source,
    }

async def step_function_generate_total(calculate_flow_dict:dict):
    """
    输入计算流程，参照所有步骤的定义信息，生成总体的计算函数，并更新整个计算流程
    """
    function_prompt = """
### 任务说明
你是一个医疗领域的计算问题分析专家，你需要根据我给出的【计算流程】定义，生成一个能够完成该计算流程的完整计算函数，并输出。
### 函数生成规范
[通用部分]
**使用python语言编写函数**
python实现代码:
- 全部使用英文字符，不得出现任何中文字符，包括标点符号
函数名：只允许小写字母、数字、下划线组成，且必须以字母开头，蛇形命名法
输入参数：
- 至少包含一个参数，参数名严格参照【步骤信息】中的step_inputs输入参数定义(必须完全一致，包括字母大小写），并按照python语法规范注明参数类型（例如string->str, number->float / int, boolean->bool等，需要你自行判断并转换）
- list / dict 类型参数，请使用python的list / dict类型，并在函数定义时注明参数类型
- 对于input_source标注为null的输入参数，请在函数定义中为该参数直接设置默认值，并在docstring中说明。

docstring注释：描述函数功能、输入参数、输出参数、返回值等信息，以及函数所属 category
import语句：
- 只允许导入常用的库（math 、datetime等）；
- 只允许 import 包名，
- 不允许 from 包名 import 具体对象，不允许 import XX as 别名
- 在使用时，只用完整包名+方法名的方式调用，例如 datetime.datetime.strptime()， 不允许 import datetime as dt，然后 dt.strptime()
return 输出参数：当输出参数只有一个时，直接返回输出参数值；当有多个参数时，按照步骤信息的step_outputs定义，输出一个dict，key为输出参数名，value为输出参数值。

**重要说明：对于input_source标注为null的输入参数，请在函数中直接设置默认值，不需要作为输入参数传入，并在docstring中说明。

[工具模板专用部分]
%s

### 输出格式 (以<python></python>标签对封装)
<python>
def 函数名(输入参数: 参数类型...) -> 参数类型:
    '''
    decs:函数功能概述
    args:
        - 输入参数1 (参数类型): 输入参数1的描述
        - 输入参数2 (参数类型): 输入参数2的描述
    returns: 返回值名称: 返回值描述
    category: 所属类别
    '''

    (核心代码部分)

    return 输出参数
</python>

### 计算流程定义
%s
"""
    pass

async def step_function_generate(calculate_flow_dict:dict):
    """
    输入计算流程，生成步骤的计算函数，并更新整个计算流程
    """

    ## 根据每个模板预定义的函数规范生成并调用，实现数据的处理计算 (llm / code)
    function_prompt = """
### 任务说明
你是一个医疗领域的计算问题分析专家，你需要根据我给出的【函数生成规范】和一个具体的【步骤信息】，生成能够实现该步骤的函数代码

### 函数生成规范
[通用部分]
**使用python语言编写函数**
python实现代码:
- 全部使用英文字符，不得出现任何中文字符，包括标点符号
函数名：只允许小写字母、数字、下划线组成，且必须以字母开头，蛇形命名法
输入参数：至少包含一个参数，参数名严格参照【步骤信息】中的step_inputs输入参数定义(必须完全一致，包括字母大小写），并按照python语法规范注明参数类型（例如string->str, number->float / int, boolean->bool等，需要你自行判断并转换）
docstring注释：描述函数功能、输入参数、输出参数、返回值等信息，以及函数所属 category
import语句：
- 只允许导入常用的库（math 、datetime等）；
- 只允许 import 包名，
- 不允许 from 包名 import 具体对象，不允许 import XX as 别名
- 在使用时，只用完整包名+方法名的方式调用，例如 datetime.datetime.strptime()， 不允许 import datetime as dt，然后 dt.strptime()
return 输出参数：当输出参数只有一个时，直接返回输出参数值；当有多个参数时，按照步骤信息的step_outputs定义，输出一个dict，key为输出参数名，value为输出参数值。

**重要说明：对于input_source标注为null的输入参数，请在函数定义中为该参数直接设置默认值，并在docstring中说明。

[工具模板专用部分]
%s

### 输出格式 
# 输出1 思考过程 (以<process></process>标签对封装)
<process>
（列出你在生成函数时的具体思考过程）
</process>

# 输出2 函数代码 (以<python></python>标签对封装)
<python>
def 函数名(输入参数: 参数类型...) -> 参数类型:
    '''
    decs:函数功能概述
    args:
        - 输入参数1 (参数类型): 输入参数1的描述
        - 输入参数2 (参数类型): 输入参数2的描述
    returns: 返回值名称: 返回值描述
    category: 所属类别
    '''

    (核心代码部分)

    return 输出参数
</python>

### 步骤信息
%s
"""

    steps_with_code = []
    steps = calculate_flow_dict.get("steps", [])
    # print(steps)
    # print(json.dumps(steps, indent=4, ensure_ascii=False))
    # raise ValueError("暂时不支持生成函数") 
    for step in steps:
        # print(f"step:\n{step}")
        try:
            prompt = function_prompt % (CategoryDict[step['category']].get('code_logic'), step)
        except:
            prompt = function_prompt % ("", step) # 没有可参照的原子工具模板
        # print(f"Step \n{step}")
        try_times = 0
        while try_times < MAX_TRY_TIMES: 
            agent = get_general_agent(name="FunctionGenerator")
            # print(f"prompt:\n{prompt}\n")
            task_result = await agent.run(task=prompt)
            code_result = get_agent_response(task_result)
            # code_result = chat_method(prompt)
            # print(code_result)
            code = regex_python(code_result)
            print(f"step:\n{step}")
            if code.startswith("def"): # 检查代码正确性
                steps_with_code.append({**step, 'code': code})
                break
            else:
                continue

        del agent

    calculate_flow_dict.update({"steps": steps_with_code})

    return {
        "calculate_flow_dict": calculate_flow_dict,
        # "steps": steps_with_code,
    }

# print(function_prompt)
# code_result = chat_method(function_prompt)

# print(code_result)