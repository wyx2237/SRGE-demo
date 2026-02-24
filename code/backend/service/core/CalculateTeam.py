from service.core.Agents import *
# from agent.Agents_v2 import get_agent_response, get_general_agent
from service.core import RuleGenerator
from service.core.CalculateFlow import CalculateFlow
import json
from utils.regex_function import regex_json_parse

from utils.logger import evaluate_logger

class CalculateTeam:
    def __init__(self, context: dict={}):
        self._context = context
        self.parameter_extractor_agent = get_parameter_extractor()
        self.calculate_agent = get_calculate_agent()

    async def run_params_extract(self, calculator_problem: str, patient_info: str, input_params: str) -> dict:
        """
        输入计算问题和病人信息，输出参数字典
        """
        # print("-"*20 + "\n")
        input_info = f"calculator_problem:\n{calculator_problem}\n\ninput_params:\n{input_params}\n\npatient_info:\n{patient_info}\n\n"
        MAX_RETRY = 3
        for i in range(MAX_RETRY):
            if i > 0:
                print(f"Retry {i+1}/{MAX_RETRY}")
                task_result = await self.parameter_extractor_agent.run(task="format error, please follow the json format with xml tags <json></json>, and try extract params again.")
            else:
                task_result = await self.parameter_extractor_agent.run(task=input_info)
            self._context.update({"parameter_extractor_result": task_result.messages[-1].content})
            extract_result = regex_json_parse(task_result.messages[-1].content)
            if extract_result is not None:
                break
                
        input_params_extracted = extract_result.get("input_dict", {})
        return input_params_extracted

    async def run_params_extract_v2(self, calculator_problem: str, patient_info: str, input_params: str) -> dict:
        """
        输入计算问题和病人信息，输出参数字典(包含原文信息)
        [
            { name: 'age', rawValue: '58-year-old', value: 58 },
            { name: 'gender', rawValue: 'male', value: 'male' },
            { name: 'height_m', rawValue: '178 cm', value: 1.78 },
            { name: 'actual_weight', rawValue: '95 kg', value: 95.0 },
            { name: 'serum_creatinine', rawValue: '1.2 mg/dL', value: 1.2 }
        ]
        """
        # print("-"*20 + "\n")
        input_info = f"calculator_problem:\n{calculator_problem}\n\ninput_params:\n{input_params}\n\npatient_info:\n{patient_info}\n\n"
        MAX_RETRY = 3
        for i in range(MAX_RETRY):
            if i > 0:
                print(f"Retry {i+1}/{MAX_RETRY}")
                task_result = await self.parameter_extractor_agent.run(task="format error, please follow the json format with xml tags <json></json>, and try extract params again.")
            else:
                task_result = await self.parameter_extractor_agent.run(task=input_info)
            self._context.update({"parameter_extractor_result": task_result.messages[-1].content})
            extract_result = regex_json_parse(task_result.messages[-1].content)
            if extract_result is not None:
                break
                
        # input_params_extracted = extract_result.get("input_source_list", [])
        return extract_result

    async def run_rule_generate(self, question: str) -> dict:
        # RuleGenerator.question_analyze(question=question)

        analyze_result = await RuleGenerator.question_analyze(question=question)
        evaluate_logger.info(f"analyze_result:\n{json.dumps(analyze_result, indent=4, ensure_ascii=False)}")
        print(analyze_result)
        steps_result_dict = analyze_result['steps_result_dict']
        flow_result = analyze_result['flow_result']

        flow_compose_result = await RuleGenerator.flow_compose(question=question, steps_result_dict=steps_result_dict, flow_result=flow_result)
        evaluate_logger.info(f"flow_compose_result:\n{json.dumps(flow_compose_result, indent=4, ensure_ascii=False)}")

        calculate_flow_dict = flow_compose_result['calculate_flow_dict']

        step_dataflow_update_result = await RuleGenerator.step_dataflow_update(calculate_flow_dict=calculate_flow_dict)
        evaluate_logger.info(f"step_dataflow_update_result:\n{json.dumps(step_dataflow_update_result, indent=4, ensure_ascii=False)}")
        # print("step_dataflow_update_result\n")
        # print(json.dumps(step_dataflow_update_result, indent=4, ensure_ascii=False))

        calculate_flow_dict_with_dataflow = step_dataflow_update_result['calculate_flow_dict']

        step_function_generate_result = await RuleGenerator.step_function_generate(calculate_flow_dict=calculate_flow_dict_with_dataflow)
        evaluate_logger.info(f"step_function_generate_result:\n{json.dumps(step_function_generate_result, indent=4, ensure_ascii=False)}")
        # print("step_function_generate_result")
        # print(json.dumps(step_function_generate_result, indent=4, ensure_ascii=False))
        calculate_flow_dict_with_function = step_function_generate_result['calculate_flow_dict']

        return calculate_flow_dict_with_function

    async def run_rule_generate_wo_atomic(self, question: str) -> dict:
        analyze_result = await RuleGenerator.question_analyze_wo_atomic(question=question)
        evaluate_logger.info(f"analyze_result:\n{json.dumps(analyze_result, indent=4, ensure_ascii=False)}")
        print(analyze_result)
        steps_result_dict = analyze_result['steps_result_dict']
        flow_result = analyze_result['flow_result']

        flow_compose_result = await RuleGenerator.flow_compose(question=question, steps_result_dict=steps_result_dict, flow_result=flow_result)
        evaluate_logger.info(f"flow_compose_result:\n{json.dumps(flow_compose_result, indent=4, ensure_ascii=False)}")

        calculate_flow_dict = flow_compose_result['calculate_flow_dict']

        step_dataflow_update_result = await RuleGenerator.step_dataflow_update(calculate_flow_dict=calculate_flow_dict)
        evaluate_logger.info(f"step_dataflow_update_result:\n{json.dumps(step_dataflow_update_result, indent=4, ensure_ascii=False)}")
        # print("step_dataflow_update_result\n")
        # print(json.dumps(step_dataflow_update_result, indent=4, ensure_ascii=False))

        calculate_flow_dict_with_dataflow = step_dataflow_update_result['calculate_flow_dict']

        step_function_generate_result = await RuleGenerator.step_function_generate(calculate_flow_dict=calculate_flow_dict_with_dataflow)
        evaluate_logger.info(f"step_function_generate_result:\n{json.dumps(step_function_generate_result, indent=4, ensure_ascii=False)}")
        # print("step_function_generate_result")
        # print(json.dumps(step_function_generate_result, indent=4, ensure_ascii=False))
        calculate_flow_dict_with_function = step_function_generate_result['calculate_flow_dict']
        
        return calculate_flow_dict_with_function


    def run_calculate_flow(self, calculate_flow_dict: dict, input_dict: dict) -> dict:
        calculate_flow = CalculateFlow(calculate_flow_dict)
        result = calculate_flow.calculate(input_dict)
        return result
    
    async def run_calculate_flow_wo_code_exec(self, calculate_flow_dict: dict, input_dict: dict) -> dict:
        """
        让 llm 参照 rule 的定义自己对输入参数进行计算
        """
        input_info = f"Rule:\n{calculate_flow_dict}\n\ninput_dict:\n{input_dict}"
        task_result = await self.calculate_agent.run(task=input_info)
        calculate_result = regex_json_parse(task_result.messages[-1].content)
        evaluate_logger.info(f"calculate_result:\n{json.dumps(calculate_result, indent=4, ensure_ascii=False)}")
        final_result = calculate_result.get("final_result", None)
        return final_result
    
    async def run_main(self, calculator_problem: str, patient_info: str, index: int, wo:int=0) -> dict:
        if wo == 1: ## 消融原子工具模板
            calculate_flow_dict = await self.run_rule_generate_wo_atomic(question=calculator_problem)
            evaluate_logger.info(f"calculate_flow_dict:\n{json.dumps(calculate_flow_dict, indent=4, ensure_ascii=False)}")
        else:
            calculate_flow_dict = await self.run_rule_generate(question=calculator_problem)
            if wo == 0:
                evaluate_logger.info(f"calculate_flow_dict:\n{json.dumps(calculate_flow_dict, indent=4, ensure_ascii=False)}")
            else:
                evaluate_logger.info(f"calculate_flow_dict:\n{json.dumps(calculate_flow_dict, indent=4, ensure_ascii=False)}")

        input_params = calculate_flow_dict.get("inputs")
        input_params_extracted = await self.run_params_extract(calculator_problem=calculator_problem, patient_info=patient_info, input_params=input_params)

        if wo == 2: ## 消融代码执行
            result = await self.run_calculate_flow_wo_code_exec(calculate_flow_dict=calculate_flow_dict, input_dict=input_params_extracted)
        else:
            result = self.run_calculate_flow(calculate_flow_dict=calculate_flow_dict, input_dict=input_params_extracted)
        return {
            "calculate_flow_dict": calculate_flow_dict,
            "input_params": input_params,
            "input_params_extracted": input_params_extracted,
            "result": result
        }
    
    async def run_wo_rule_gen(self, calculator_problem: str, patient_info: str, calculate_flow_dict, wo:int=0) -> dict:
        input_params = calculate_flow_dict.get("inputs")
        input_params_extracted = await self.run_params_extract(calculator_problem=calculator_problem, patient_info=patient_info, input_params=input_params)
        if wo == 2: ## 消融代码执行
            result = await self.run_calculate_flow_wo_code_exec(calculate_flow_dict=calculate_flow_dict, input_dict=input_params_extracted)
        else:
            result = self.run_calculate_flow(calculate_flow_dict=calculate_flow_dict, input_dict=input_params_extracted)
        return {
            "input_params": input_params,
            "input_params_extracted": input_params_extracted,
            "result": result
        }

    async def run_direct_llm(self, calculator_problem: str, patient_info: str):
        prompt = ""
        input_info = f"calculator_problem:\n{calculator_problem}\n\npatient_info:\n{patient_info}\n\n"
        agent = get_general_agent(name="GeneralAgent", system_prompt=prompt)
        task_result = await agent.run(task=input_info)
        calculate_result = regex_json_parse(task_result.messages[-1].content)
        return {
            "input_params": None,
            "input_params_extracted": None,
            "result": calculate_result.get("final_result", None)
        }