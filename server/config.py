import os

# 仓库根目录（server/ 的上一级）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 各模块路径
MANAGEMENT_DIR = os.path.join(BASE_DIR, "management")
PAPERS_DIR = os.path.join(BASE_DIR, "papers")
EVALUATION_DIR = os.path.join(BASE_DIR, "evaluation")

# 评测输出目录（压缩码流 / 重建视频等，供 /api/evaluation/outputs 端点按需服务）
# 下游库可覆盖：infraredComp 用 results/video/，其它库用 evaluation/outputs/
OUTPUTS_DIR = os.path.join(EVALUATION_DIR, "outputs")

# 训练模块路径（镜像 results/video/ 结构）
# 下游库可覆盖：infraredComp 用 results/training/，其它库用 training/outputs/
TRAINING_DIR = os.path.join(BASE_DIR, "results", "training")
TRAINING_METRICS_JSON = os.path.join(TRAINING_DIR, "metrics.json")  # 训练 run 列表(含 loss_series)
CHECKPOINTS_DIR = os.path.join(TRAINING_DIR, "checkpoints")         # trained .pth state_dicts
TRAINING_LOGS_DIR = os.path.join(TRAINING_DIR, "logs")              # 训练日志
# 训练框架 work_dir 根：{run_id}/vis_data/scalars.json（训练中实时指标）
#                      {run_id}/vis_samples/epoch_N/（逐 epoch 可视化样本 + meta.json）
TRAINING_WORK_DIR = os.path.join(TRAINING_DIR, "work_dirs")
# 训练产物服务根目录（checkpoint + log 文件，供 /api/training/outputs 按需服务）
TRAINING_OUTPUTS_DIR = TRAINING_DIR

# 论文数据库路径（本地独立数据库）
PAPERS_DB = os.path.join(BASE_DIR, "data", "papers.db")

# 数据集浏览模块（文件系统扫描，支持符号链接数据集）
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
THUMBS_DIR = os.path.join(DATASETS_DIR, ".thumbs")  # 视频缩略图磁盘缓存（点目录，浏览时跳过）

# Speed Run 模块（N 视频 × M 模型 跑批结果画廊）
# 下游库可覆盖输出位置；上游脚手架只读 results.json + 静态服务 outputs/
SPEEDRUN_DIR = os.path.join(BASE_DIR, "results", "speedrun")
SPEEDRUN_OUTPUTS_DIR = os.path.join(SPEEDRUN_DIR, "outputs")
SPEEDRUN_RESULTS_JSON = os.path.join(SPEEDRUN_DIR, "results.json")

# 文档列表中文件夹的先后（未列出的排在已知之后）
# 下游库可覆盖：本仓库为数字人文档体系，固定 数字人概述 → 论文笔记 → knowledge；上游脚手架默认空
DOCS_FOLDER_ORDER = ['数字人概述', '论文笔记', 'knowledge']

# CORS 配置
CORS_ORIGINS = [
    "http://localhost:3212",
    "http://127.0.0.1:3212",
]
