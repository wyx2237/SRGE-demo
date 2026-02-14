from ast import List
from typing import Dict
from core.CalculateTeam import CalculateTeam

class RuleService:
    @staticmethod
    async def rule_generate(question: str, knowledge: str, text: str) -> Dict:
        """
        生成计算规则
        将计算问题与知识补充合并，作为最终的计算问题的文本形式
        
        Args:
            question: 计算问题描述
            knowledge: 计算知识补充
            text: 患者信息文本

        Returns:
            Dict: 包含计算规则的字典
        """
        # 调用算法模块实现规则生成逻辑
        final_question = f"【计算问题】：{question}\n【相关知识补充】：{knowledge}"
        calculate_team = CalculateTeam()
        calculate_flow_dict = await calculate_team.run_rule_generate(question=final_question)
        return calculate_flow_dict

    @staticmethod
    async def rule_list(keyword: str) -> List[Dict]:
        """
        从文本中提取计算参数
        
        Args:
            keyword: 计算问题关键词
        
        Returns:
            List[Dict]: 列表形式展示持久化存储的所有结构化规则
        """
        # 调用算法模块实现参数抽取逻辑
        rule_list = []
        return rule_list