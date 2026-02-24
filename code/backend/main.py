from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 导入路由模块
from api.v1 import Dashboard, Calculation, Rule

# 初始化 FastAPI 应用，更新元数据为 SURGE
app = FastAPI(
    title="SURGE Engine API", 
    description="Backend for SURGE Clinical Calculation System",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI 地址
    redoc_url="/redoc"
)

# --- CORS 配置 ---
# 允许前端 (通常开发环境是 localhost:3000 或 8080) 访问
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173", # Vite 默认端口
    "*"                      # 开发阶段允许所有，生产环境建议指定具体域名
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 注册路由模块 ---
# 将 Dashboard 和 Calculation 模块挂载到主应用
app.include_router(Dashboard.router)
app.include_router(Calculation.router)
app.include_router(Rule.router)

# --- 根路径检查 ---
@app.get("/", tags=["Health"])
async def root():
    return {
        "system": "SURGE",
        "status": "Online",
        "message": "Welcome to SURGE Backend. Visit /docs for API documentation."
    }

if __name__ == "__main__":
    # 启动服务器
    # reload=True 意味着当你修改代码保存后，服务会自动重启
    print("🚀 Starting SURGE Backend System...")
    uvicorn.run("main:app", host="0.0.0.0", port=5175, reload=True)