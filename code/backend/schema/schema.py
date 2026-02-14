import pydantic

class ResponseBase(pydantic.BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

# class WorkflowResponse(pydantic.BaseModel):
#     steps: List[dict]
#     initial_state: dict