import datetime
from typing import Dict, List
from service.core.CalculateTeam import CalculateTeam
from service.core.RuleCache import global_rule_cache
import asyncio
import random

from datetime import datetime

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
        for keyword in global_rule_cache.keys():
            if keyword.lower() in question.lower():
                print(f"Cache Hit: {keyword}")
                st = datetime.now()
                # 模拟延时 10~20 秒
                await asyncio.sleep(random.uniform(3, 5))
                et = datetime.now()

                print(f"Time Cost: {(et - st).total_seconds():.2f} seconds")
                return global_rule_cache[keyword]

        calculate_team = CalculateTeam()
        calculate_flow_dict = await calculate_team.run_rule_generate(question=final_question)
        return calculate_flow_dict

    @staticmethod
    def rule_list(keyword: str) -> List:
        """
        列表展示所有结构化规则
        
        Args:
            keyword: 计算问题关键词
        
        Returns:
            List[Dict]: 列表形式展示持久化存储的所有结构化规则
        """
        # 调用算法模块实现参数抽取逻辑
        rule_list = []
        return rule_list