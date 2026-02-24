from typing import Dict
from fastapi import APIRouter
from service.CalculationService import CalculationService
from schema.schema import ResponseBase, CalculationRequest
from utils.response import ResponseModel

from data.rules.rules import *

router = APIRouter(prefix="/calculation", tags=["Calculation"])

@router.post(
    "/execute",
    summary="执行计算任务",
    response_model=ResponseBase,
)
async def execute_calculation_task(request: CalculationRequest):
    """
    执行计算任务
    
    Args:
        request: 包含计算规则和输入文本的请求模型
            rule: 计算规则
            text: 输入待计算文本（病人信息）
    
    Returns:
        Dict: 包含计算结果的字典
            input_source_list: 输入参数来源列表
            execution_steps: 计算执行步骤列表
            final_result: 最终计算结果
    """
    try:
        # Step1 参数抽取
        rule = request.rule
        # rule = CALCULATOR_2
        extract_result = await CalculationService.extract_parameters(question="", text=request.text, rule=rule)
        params = extract_result.get("input_dict", {})
        input_source_list = extract_result.get("input_source_list", [])
        print(f"input_source_list: \n{input_source_list}")
        # Step2 计算执行
        cal_result = await CalculationService.execute_calculation(params=params, rule=rule)
        final_result = cal_result.get("final_result", None)
        execution_steps = cal_result.get("execution_steps", [])

        return ResponseModel.generate_success_response(
            data = {
                "input_source_list": input_source_list,
                "execution_steps": execution_steps,
                "final_result": final_result
            }
        )
    except Exception as e:
        raise
        return ResponseModel.generate_error_response(message=str(e))

