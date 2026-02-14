from service.core.CalculateTeam import CalculateTeam

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
        params_dict = await calculate_team.run_params_extract(calculator_problem=question, patient_info=text, input_params=rule.get("inputs"))
        return params_dict

    @staticmethod
    async def execute_calculation(params: Dict, rule: Dict) -> Dict:
        """
        执行计算任务

        Args:
            params: 计算参数
            rule: 计算规则
        
        Returns:
            Dict: 包含计算结果的字典
        """
        result_dict = {}
        # 调用算法模块实现计算逻辑
        calculate_team = CalculateTeam()
        result_dict = await calculate_team.run_calculate_flow(calculate_flow_dict=rule, input_dict=params)
        return result_dict
        
