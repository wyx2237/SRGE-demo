# 需要完成的事项
1. 选取合适的例子作为演示 （4个，每个2-3个指标；每个指标对应Structured Rule 预先实现并放在指定位置）
2. 3个主要界面的API对接和实现（dashboard, calculation, atomic tool
3. 是否需要数据库单独实现？目前倾向于简单文件存储形式
4. 
5. 

## Calculation
- question -> structured rule
- structured rule + emr -> result

需要按照前端展示形式来优化后端产生数据应该包括哪些

####

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

# 启动命令
uvicorn main:app --host 0.0.0.0 --port 9000