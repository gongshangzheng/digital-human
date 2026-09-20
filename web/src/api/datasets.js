import request from './request'

// 数据集列表（datasets/ 一级子目录扫描）
export const listDatasets = () => request.get('/datasets')

// 目录浏览（服务端分页）
export const browseDataset = (id, params) => request.get(`/datasets/${id}/browse`, { params })

// 视频缩略图 URL（中间帧，后端磁盘缓存）
export const getThumbUrl = (id, path) =>
  `/api/datasets/${id}/thumb?path=${encodeURIComponent(path)}`

// 原文件 URL（图片直显 / 视频按需播放）
export const getFileUrl = (id, path) =>
  `/api/datasets/${id}/file?path=${encodeURIComponent(path)}`
