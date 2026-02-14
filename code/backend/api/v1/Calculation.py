from ast import Dict
from fastapi import APIRouter
from service.CalculationService import CalculationService
from schema.schema import ResponseBase, WorkflowResponse, CalculationCreate, CalculationTask
from utils.response import ResponseModel

router = APIRouter(prefix="/calculation", tags=["Calculation"])

@router.post(
    "/execute",
    summary="执行计算任务",
    response_model=ResponseBase,
)
async def execute_calculation_task(rule:Dict, text:str):
    """
    执行计算任务
    
    Args:
        rule: 计算规则
        text: 输入待计算文本（病人信息）
    
    Returns:
        ResponseBase: 包含计算结果的响应模型
    """
    try:
        # Step1 参数抽取
        params = await CalculationService.extract_parameters(rule, text)
        
        # Step2 计算执行
        result = await CalculationService.execute_calculation(rule, params)
        return ResponseModel.generate_success_response(data=result)
    except Exception as e:
        raise
        return ResponseModel.generate_error_response(message=str(e))

