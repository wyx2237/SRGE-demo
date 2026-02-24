from ast import Dict
from fastapi import APIRouter
from service.RuleService import RuleService
from service.CalculationService import CalculationService
from schema.schema import ResponseBase, RuleGenerateRequest
from utils.response import ResponseModel

router = APIRouter(prefix="/rule", tags=["Rule"])

@router.post("/generate", response_model=ResponseBase)
async def generate_rule(request: RuleGenerateRequest):
    """
    生成计算规则
    
    Args:
        request: 包含计算问题描述、知识补充和患者信息文本的请求模型
            question: 计算问题描述
            knowledge: 计算知识补充
            text: 患者信息文本
        
    Returns:
        Dict: 包含计算规则的字典
    """
    print(request)
    calculate_flow_dict = await RuleService.rule_generate(request.question, request.knowledge, request.text)
    
    return ResponseModel.generate_success_response(data={"structured_rule": calculate_flow_dict})

@router.get("/list", response_model=ResponseBase)
async def get_rule_list(keyword: str = ""):
    """
    获取所有结构化规则
    
    Args:
        keyword: 计算问题关键词（供筛选）
        

    Returns:
        List[Dict]: 列表形式展示持久化存储的所有结构化规则
    """
    rule_list = await RuleService.rule_list(keyword)
    return ResponseModel.generate_success_response(data=rule_list)
