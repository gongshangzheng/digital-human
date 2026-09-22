"""FastAPI 主入口 — Digital Human 数字人研发管理平台后端"""
import sys
import os

# 确保能 import server 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from server.config import CORS_ORIGINS, MANAGEMENT_DIR
from server.routers import management, papers, evaluation, training, datasets, speedrun

app = FastAPI(
    title="Digital Human 数字人研发管理平台 API",
    description="为前端提供项目管理、论文搜集、评测体系的数据接口",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(management.router)
app.include_router(papers.router)
app.include_router(evaluation.router)
app.include_router(training.router)
app.include_router(datasets.router)
app.include_router(speedrun.router)

# 文档图片资产：management/docs/_assets/ 以只读静态目录暴露给 wiki 文档引用
# 引用约定：`![图 N · 说明](/api/management/docs-assets/<slug>/<file>)`
# 目录不存在时自动创建（check_dir=False 保证空仓库也能启动）
DOC_ASSETS_DIR = os.path.join(MANAGEMENT_DIR, "docs", "_assets")
os.makedirs(DOC_ASSETS_DIR, exist_ok=True)
app.mount(
    "/api/management/docs-assets",
    StaticFiles(directory=DOC_ASSETS_DIR, check_dir=False),
    name="doc-assets",
)


@app.get("/")
async def root():
    return {"message": "Digital Human 数字人研发管理平台 API", "docs": "/docs"}


@app.get("/api/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="0.0.0.0", port=8812, reload=True)
