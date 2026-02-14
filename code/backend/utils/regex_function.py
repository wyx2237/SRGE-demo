import re

def regex_python(text) -> str:
    matches = re.findall(r"<python>(.*?)</python>", text, re.DOTALL)
    if matches:
        return matches[0].strip()
    else:
        return ""

def regex_workflow(text):
    matches = re.findall(r"<workflow>(.*?)</workflow>", text, re.DOTALL)
    if matches:
        return matches[0].strip()
    else:
        return None

# def regex_json(text):
#     matches = re.findall(r"<json>(.*?)</json>", text, re.DOTALL)
#     if matches:
#         return matches[0].strip()
#     else:
#         return None

def regex_json(text):
    matches = re.findall(r"<json>(.*?)</json>", text, re.DOTALL)
    if matches:
        return matches[0].strip()
    else:
        return None

def regex_json_parse(llm_answer) -> dict | None:
    """
    从大模型回答内容中获取json格式内容
    """
    import re
    import json

    pattern_1 = r"<json>(.*?)</json>"
    pattern_2 = r"```json(.*?)```"
    match = re.findall(pattern_1, llm_answer, re.DOTALL)
    if match:
        # print("Macth:" + str(match))
        data = match[0]
        # print(data)
        try:
            json_data = json.loads(data)
            print("JSON Parse Success")
            return json_data
        except:
            print("JSON Parse Failed")
            return None
    match = re.findall(pattern_2, llm_answer, re.DOTALL)
    if match:
        # print("Macth:" + str(match))
        data = match[0]
        # print(data)
        try:
            json_data = json.loads(data)
            print("JSON Parse Success")
            return json_data
        except:
            print("JSON Parse Failed")
            return None
    
    return None

def regex_input_params(llm_answer):
    matches = re.findall(r"<input_params>(.*?)</input_params>", llm_answer, re.DOTALL)
    if matches:
        return matches[0].strip()
    else:
        return None

def regex_process(llm_answer):
    matches = re.findall(r"<process>(.*?)</process>", llm_answer, re.DOTALL)
    if matches:
        return matches[0].strip()
    else:
        return None

def regex_result(llm_answer):
    matches = re.findall(r"<result>(.*?)</result>", llm_answer, re.DOTALL)
    if matches:
        return matches[0].strip()
    else:
        return None