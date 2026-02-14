backend 项目结构

main.py 主程序入口
api/ 接口目录
    v1/ 版本1接口目录
    v2/ ...

entity/ 实体目录
logs/ 日志目录
schema/ 数据模型目录
service/ 服务目录
    |-- core/ 核心服务目录

utils/ 工具目录
    |-- logger.py 日志工具
    |-- model_request.py 模型请求工具
    |-- regex_function.py 正则表达式工具
    |-- response.py 响应工具
