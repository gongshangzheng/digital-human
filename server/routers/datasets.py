"""数据集浏览路由 — 文件系统扫描 + 分页浏览 + 视频缩略图

数据源 = 仓库根 datasets/ 目录（每个一级子目录/符号链接 = 一个数据集）。
只读：不提供任何写接口。缩略图按需生成并缓存在 datasets/.thumbs/。
"""
import hashlib
import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from server.config import DATASETS_DIR, THUMBS_DIR

router = APIRouter(prefix="/api/datasets", tags=["datasets"])

VIDEO_EXTS = {".mp4", ".webm", ".mkv", ".mov", ".avi", ".m4v"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}

VIDEO_MIME = {
    ".mp4": "video/mp4", ".webm": "video/webm", ".mkv": "video/x-matroska",
    ".mov": "video/quicktime", ".avi": "video/x-msvideo", ".m4v": "video/x-m4v",
}
IMAGE_MIME = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
    ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp",
}


def _dataset_root(dataset_id: str) -> Optional[str]:
    """解析数据集根目录。允许 datasets/{id} 是指向外部的符号链接。"""
    if not dataset_id or "/" in dataset_id or dataset_id.startswith("."):
        return None
    entry = os.path.join(DATASETS_DIR, dataset_id)
    if not os.path.isdir(entry):
        return None
    return os.path.realpath(entry)


def _resolve_in_dataset(dataset_id: str, rel_path: str) -> Optional[str]:
    """将相对路径解析到数据集根目录内（防路径穿越）。"""
    root = _dataset_root(dataset_id)
    if root is None or not isinstance(rel_path, str):
        return None
    rel = rel_path.lstrip("/")
    path = os.path.realpath(os.path.join(root, rel))
    if path != root and not path.startswith(root + os.sep):
        return None
    return path


@router.get("")
async def list_datasets():
    """数据集列表：datasets/ 下每个一级子目录（含符号链接），浅层统计子目录/文件数。"""
    datasets = []
    if not os.path.isdir(DATASETS_DIR):
        return datasets
    for name in sorted(os.listdir(DATASETS_DIR)):
        if name.startswith("."):
            continue
        entry = os.path.join(DATASETS_DIR, name)
        if not os.path.isdir(entry):
            continue
        subdirs = files = 0
        try:
            for child in os.listdir(entry):
                if child.startswith("."):
                    continue
                if os.path.isdir(os.path.join(entry, child)):
                    subdirs += 1
                else:
                    files += 1
        except OSError:
            continue
        datasets.append({
            "id": name,
            "name": name,
            "is_symlink": os.path.islink(entry),
            "real_path": os.path.realpath(entry),
            "subdirs": subdirs,
            "files": files,
        })
    return datasets


@router.get("/{dataset_id}/browse")
async def browse_dataset(
    dataset_id: str,
    path: str = Query(""),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    """目录浏览（服务端分页）。目录在前、文件在后，均按名称排序。"""
    target = _resolve_in_dataset(dataset_id, path)
    if target is None or not os.path.isdir(target):
        raise HTTPException(status_code=404, detail="Directory not found")

    dirs, files = [], []
    for name in sorted(os.listdir(target)):
        if name.startswith("."):
            continue
        full = os.path.join(target, name)
        rel = os.path.join(path, name) if path else name
        if os.path.isdir(full):
            dirs.append({"name": name, "path": rel, "is_dir": True,
                         "is_image": False, "is_video": False, "size": 0})
        else:
            ext = os.path.splitext(name)[1].lower()
            try:
                fsize = os.path.getsize(full)
            except OSError:
                fsize = 0
            files.append({"name": name, "path": rel, "is_dir": False,
                          "is_image": ext in IMAGE_EXTS, "is_video": ext in VIDEO_EXTS,
                          "size": fsize})

    items = dirs + files
    total = len(items)
    pages = (total + size - 1) // size if total > 0 else 0
    start = (page - 1) * size
    return {
        "dataset_id": dataset_id, "path": path,
        "items": items[start:start + size],
        "total": total, "page": page, "size": size, "pages": pages,
    }


@router.get("/{dataset_id}/thumb")
async def get_thumbnail(dataset_id: str, path: str = Query(...)):
    """视频缩略图：中间帧 JPEG q80，datasets/.thumbs/{md5[:16]}.jpg 磁盘缓存。"""
    target = _resolve_in_dataset(dataset_id, path)
    if target is None or not os.path.isfile(target):
        raise HTTPException(status_code=404, detail="File not found")

    os.makedirs(THUMBS_DIR, exist_ok=True)
    key = hashlib.md5(target.encode()).hexdigest()[:16]
    thumb_path = os.path.join(THUMBS_DIR, key + ".jpg")
    if not os.path.isfile(thumb_path):
        try:
            import cv2  # 惰性 import：仅缓存 miss 时需要
        except ImportError:
            raise HTTPException(status_code=404, detail="Thumbnail unavailable (cv2 not installed)")
        cap = cv2.VideoCapture(target)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total > 2:
            cap.set(cv2.CAP_PROP_POS_FRAMES, total // 2)
        ok, frame = cap.read()
        cap.release()
        if not ok or frame is None:
            raise HTTPException(status_code=500, detail="Failed to extract frame")
        cv2.imwrite(thumb_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return FileResponse(thumb_path, media_type="image/jpeg")


@router.get("/{dataset_id}/file")
async def get_file(dataset_id: str, path: str = Query(...)):
    """原文件服务（图片/视频预览用）。"""
    target = _resolve_in_dataset(dataset_id, path)
    if target is None or not os.path.isfile(target):
        raise HTTPException(status_code=404, detail="File not found")
    ext = os.path.splitext(target)[1].lower()
    media = VIDEO_MIME.get(ext) or IMAGE_MIME.get(ext) or "application/octet-stream"
    return FileResponse(target, media_type=media, filename=os.path.basename(target))
