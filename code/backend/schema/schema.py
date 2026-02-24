from pydantic import BaseModel
from typing import Optional, Any, Dict

class ResponseBase(BaseModel):
    code: int
    message: str
    data: Dict = {}

class RuleGenerateRequest(BaseModel):
    question: str
    knowledge: str
    text: str

class CalculationRequest(BaseModel):
    rule: Dict
    text: str
    
# class WorkflowResponse(pydantic.BaseModel):
#     steps: List[dict]
#     initial_state: dict