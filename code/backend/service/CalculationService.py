from service.core.CalculateTeam import CalculateTeam
from typing import Dict



class CalculationService:
    @staticmethod
    async def extract_parameters(question: str, text: str, rule: Dict) -> Dict:
        """
        从文本中提取计算参数
        
        Args:
            rule: 计算规则
            text: 输入待计算文本（病人信息）
        
        Returns:
            Dict: 包含提取参数的字典
        """
        # 调用算法模块实现参数抽取逻辑
        calculate_team = CalculateTeam()
        extract_result = await calculate_team.run_params_extract_v2(calculator_problem=question, patient_info=text, input_params=rule.get("inputs"))
        return {
            "input_dict": extract_result.get("input_dict", {}),
            "input_source_list": extract_result.get("input_source_list", []),
            # "missing": extract_result.get("missing", [])
        }

    @staticmethod
    async def execute_calculation(params: Dict, rule: Dict) -> Dict:
        """
        执行计算任务

        Args:
            params: 计算参数
            rule: 计算规则
        
        Returns:
            Dict: 包含计算结果的字典
                final_result: 最终计算结果
                execution_steps: 计算执行步骤
        """
        result_dict = {}
        # 调用算法模块实现计算逻辑
        calculate_team = CalculateTeam()
        result_dict = calculate_team.run_calculate_flow(calculate_flow_dict=rule, input_dict=params)
        return result_dict
        
