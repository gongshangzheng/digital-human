"""Speed Run 路由 — N 视频 × M 模型跑批结果画廊（上游脚手架版）

只读 results/speedrun/results.json + 静态服务 outputs/（标注视频 + 封面图）。
上游不做跑批进程管理；下游库覆盖 POST /run 接真实 speedrun 脚本。
"""
import json
import os

from fastapi import APIRouter, Body
from fastapi.responses import FileResponse

from server.config import SPEEDRUN_OUTPUTS_DIR, SPEEDRUN_RESULTS_JSON
from server.utils.file_utils import safe_resolve

router = APIRouter(prefix="/api/speedrun", tags=["speedrun"])

VIDEO_MIME = {
    ".mp4": "video/mp4", ".webm": "video/webm", ".mkv": "video/x-matroska",
    ".mov": "video/quicktime", ".avi": "video/x-msvideo", ".m4v": "video/x-m4v",
}
IMAGE_MIME = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
    ".gif": "image/gif", ".webp": "image/webp",
}


def _load_results():
    if not os.path.isfile(SPEEDRUN_RESULTS_JSON):
        return {"generated_at": None, "results": []}
    try:
        with open(SPEEDRUN_RESULTS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"generated_at": None, "results": []}
    if not isinstance(data, dict):
        return {"generated_at": None, "results": []}
    data.setdefault("results", [])
    return data


@router.get("/results")
async def get_results():
    """跑批结果列表（原样返回 results.json）。

    结果字段契约：{id, model_id, video, gt_label, correct, metrics{top1_label, top1_score},
    output_video, cover_image, status, elapsed_s, gpu_mem_mb, gpu_avg_util, rtf, finished_at}
    output_video / cover_image 为相对 outputs/ 的路径，经 /outputs/{path} 服务。
    """
    return _load_results()


@router.get("/status")
async def get_status():
    """跑批状态。上游脚手架无进程管理，恒 running=false；下游覆盖为真实状态。"""
    data = _load_results()
    return {
        "running": False,
        "results_count": len(data.get("results", [])),
        "generated_at": data.get("generated_at"),
    }


@router.post("/run")
async def run_speedrun(data: dict = Body(...)):
    """启动 speed run（mock）。

    上游脚手架不执行真实跑批；下游库（如 pet-action-recognition）覆盖此端点，
    spawn scripts/speedrun.py 并增量写 results.json。
    """
    return {
        "status": "pending",
        "message": "上游脚手架未实现真实跑批，请在下游库中覆盖此端点",
        "config": data,
    }


@router.get("/outputs/{file_path:path}")
async def serve_output(file_path: str):
    """按需服务跑批产物（标注视频 / 封面图），safe_resolve 防穿越。"""
    safe = safe_resolve(SPEEDRUN_OUTPUTS_DIR, file_path)
    if not safe or not os.path.isfile(safe):
        return {"detail": "Output not found"}, 404
    ext = os.path.splitext(safe)[1].lower()
    media = VIDEO_MIME.get(ext) or IMAGE_MIME.get(ext) or "application/octet-stream"
    return FileResponse(safe, media_type=media, filename=os.path.basename(safe))
