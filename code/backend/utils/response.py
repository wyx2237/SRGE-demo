from typing import Any, Dict, Optional

class ResponseModel:
    @staticmethod
    def generate_response(
        code: int,
        message: str,
        data: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        自动生成返回响应字典。
        
        :param code: 状态码，200表示成功，其他值表示错误。
        :param message: 响应消息
        :param data: 返回的数据
        :return: 返回的字典数据
        """
        response = {
            "code": code,
            "message": message,
            "data": data or {},  # 如果没有数据，返回空字典
        }
        return response

    @staticmethod
    def generate_success_response(code: int=200, data: Optional[Any] = None, message: str="操作成功") -> Dict[str, Any]:
        """
        自动生成成功的响应。
        :param data: 返回的数据（如果有）
        :return: 成功响应的字典
        """
        return ResponseModel.generate_response(
            code=code,
            message=message,
            data=data
        )

    @staticmethod
    def generate_error_response(code: int=400, message: str="请求失败") -> Dict[str, Any]:
        """
        自动生成失败的响应。
        
        :param code: 错误的状态码
        :param message: 错误消息
        :return: 返回的错误响应字典
        """
        return ResponseModel.generate_response(code=code, message=message, data=None)
