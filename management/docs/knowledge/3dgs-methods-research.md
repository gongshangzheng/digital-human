---
task: t4-3
date: 2026-07-09
---

# 3DGS 头部 Avatar 方法调研

对 FlexAvatar、HyperGaussians、MATCH、AniGS 四个 3D Gaussian Splatting 头部 Avatar 方法进行调研，评估其在数字人评测框架中的接入价值与 A10 部署可行性。

---

## 1. FlexAvatar（CVPR 2026）

| 项目 | 内容 |
|------|------|
| **论文** | FlexAvatar: Learning Complete 3D Head Avatars with Partial Supervision |
| **作者** | Tobias Kirschstein, Simon Giebenhain, Matthias Nießner (TUM) |
| **代码** | https://github.com/tobias-kirschstein/flexavatar |
| **输入** | 单张肖像图像 |
| **输出** | 完整 360° 3D 头部 Avatar（可动画、可自由视角渲染） |
| **驱动信号** | FLAME 表情码（135-dim：100 exp + 12 eyes + 2 eyelids + 6 neck + 6 jaw + 9 head_pose） |

### 方法概述

FlexAvatar 是一个基于 transformer 的 encoder-decoder 模型：
1. **编码器 E**：DINOv2 特征提取 → UV 空间 cross-attention → 压缩 avatar code A（32×32×768）
2. **解码器 D**：avatar code + 表情码 → StyleGAN-PixelShuffle 上采样 → 3D Gaussians（~58k 个）
3. **渲染**：gsplat tile-based rasterizer

**核心创新 — Bias Sinks**：引入两个可学习 token（z_2D / z_3D），在训练时区分单目和多视角数据来源。推理时仅使用 z_3D，获得兼具泛化性和完整性的 3D 头部 Avatar。

**Fitting 阶段**：对 encoder 输出的 avatar code 进行优化（200 步，~2 分钟），冻结网络仅优化 latent，提升身份保持和清晰度。

### 评测结果（VFHQ-Test, 3D Portrait Animation）

| 模型 | PSNR↑ | SSIM↑ | LPIPS↓ | CSIM↑ |
|------|-------|-------|--------|-------|
| GAGAvatar | 21.83 | 0.818 | 0.122 | 0.816 |
| LAM | 22.65 | 0.829 | 0.109 | 0.822 |
| **FlexAvatar** | **23.47** | **0.837** | **0.099** | **0.830** |

### 依赖

- PyTorch + CUDA 11.8
- Pixel3DMM（完整追踪功能需要）：easy-pixel3dmm, pytorch3d, nvdiffrast
- 可选：SHeaP（实时表情追踪，用于 live re-enactment）、MODNet（背景抠图）

### A10 可行性

- 训练使用 1× A100，推理应可在 A10 上运行（transformer 模型，显存需求远低于扩散模型）
- 前馈推理（无 fitting）应在秒级完成
- Fitting 阶段 200 步约 2 分钟，可接受
- **已接入评测框架**（driving_mode: pixel3dmm / artalk）

---

## 2. HyperGaussians（CVPR 2026）

| 项目 | 内容 |
|------|------|
| **论文** | HyperGaussians: High-Dimensional Gaussian Splatting for High-Fidelity Animatable Face Avatars |
| **作者** | Gent Serifi, Marcel C. Buehler (ETH Zurich) |
| **代码** | https://github.com/gserifi/HyperGaussians |
| **类型** | Plug-and-play 增强模块（非独立方法） |

### 方法概述

HyperGaussians 不是独立的 Avatar 方法，而是对 3DGS 表示本身的高维扩展：

1. **高维 Gaussians**：将标准 3D Gaussians 扩展为高维多变量 Gaussians，通过可学习的局部 embedding 进行条件化
2. **逆协方差技巧**：高维协方差矩阵求逆计算昂贵，通过重参数化避免直接求逆，使计算效率可接受
3. **即插即用**：可直接集成到现有 3DGS Avatar 方法中（FlashAvatar、GaussianHeadAvatar）

```python
# 使用方式
from hypergaussians import HyperGaussians
hgs_xyz = HyperGaussians(num_gaussians, latent_dim, 3)  # 位置
hgs_rot = HyperGaussians(num_gaussians, latent_dim, 4)  # 旋转
hgs_scl = HyperGaussians(num_gaussians, latent_dim, 3)  # 缩放
```

### 优势

- 高频细节显著提升：眼睛、牙齿、皱纹、镜面反射
- 在 29 个受试者、6 个数据集上验证，数值和视觉均优于标准 3DGS
- 安装简单：`pip install git+https://github.com/gserifi/HyperGaussians.git`

### A10 可行性

- 逆协方差技巧使计算开销可控
- 依赖底座模型（FlashAvatar/GaussianHeadAvatar）的硬件需求
- **接入价值**：可作为 FlexAvatar 或其他 3DGS 方法的增强模块，但需要修改底座模型代码

---

## 3. MATCH（CVPR 2026）

| 项目 | 内容 |
|------|------|
| **论文** | MATCH: Feed-forward Gaussian Registration for Head Avatar Creation and Editing |
| **作者** | Malte Prinzler, Paulo Gotardo, Siyu Tang, Timo Bolkart (ETH Zürich, Google) |
| **代码** | https://github.com/malteprinzler/match |
| **输入** | 标定多视角图像 |
| **输出** | 静态 Gaussian splat 纹理（0.5 秒） |

### 方法概述

MATCH 是一个前馈多视角 Gaussian 配准方法：

1. **输入**：标定的多视角图像（需要多相机采集系统）
2. **粗网格推理**：TEMPEH 推理粗网格 + UV 渲染
3. **MATCH 推理**：registration-guided attention block → 每个 UV-map token 仅关注对应网格区域的图像 token → 静态 Gaussian splat 纹理
4. **应用**：编辑、表情迁移、快速 Avatar 优化

**GEM Avatar 流程**（从多视角视频创建可动画 Avatar）：
1. MATCH 预测 Gaussian splat 纹理
2. FLAME 配准
3. PCA 降维
4. 表情特征预测
5. 系数回归器训练

### 优势

- 比最近基线快 10 倍
- 跨受试者和表情的密集语义对应
- 支持编辑和表情迁移

### 依赖（复杂）

- CUDA 12.6, gsplat_2dgs_sm90, dqtorch, pytorch3d, kaolin, GEM, TEMPEH, Sapiens, opendr, chumpy
- 多个 git 仓库需要手动编译安装

### A10 可行性

- **需要多视角输入**（非单图方法），需要多相机采集系统
- 依赖 SM90 架构（gsplat_2dgs_sm90），A10 可能不兼容
- 设置极其复杂（15+ 依赖需手动编译）
- **接入价值低**：不适用于单图/音频驱动场景，且硬件依赖可能不满足

---

## 4. AniGS（CVPR 2025）

| 项目 | 内容 |
|------|------|
| **论文** | AniGS: Animatable Gaussian Avatar from a Single Image with Inconsistent Gaussian Reconstruction |
| **作者** | Lingteng Qiu, et al. |
| **arXiv** | 2412.02684 |
| **项目页** | https://lingtengqiu.github.io/2024/AniGS/ |
| **输入** | 单张图像 |
| **输出** | 可动画 3D 人体 Avatar（全身，非仅头部） |

### 方法概述

AniGS 是一个两阶段的单图→可动画 Avatar 方法：

**阶段 1：多视角生成**
- 使用 transformer-based 视频生成模型（参考图像引导）
- 生成多视角正则姿态图像 + 对应的法线图
- 在大规模视频数据集上预训练以提升泛化性

**阶段 2：4DGS 重建**
- 将重建问题重新定义为 4D 任务
- 使用 4D Gaussian Splatting (4DGS) 优化处理生成视角间的不一致性
- 实现实时渲染

### 优势

- 单张图像即可生成可动画 3D Avatar
- 使用生成模型解决多视角歧义
- 实时动画渲染

### 限制

- **全身 Avatar**（非仅头部），与头部数字人场景不完全匹配
- 依赖视频扩散模型（阶段 1 GPU 需求高）
- 4DGS 优化阶段需要额外时间

### A10 可行性

- 阶段 1（视频扩散模型）显存需求高，A10 可能不足
- 阶段 2（4DGS 优化）应在 A10 上可行
- **接入价值中等**：全身 Avatar 方向，可作为技术路线参考，但直接接入头部数字人评测框架价值有限

---

## 总结对比

| 方法 | 类型 | 输入 | 头部/全身 | A10 可行性 | 接入价值 | 状态 |
|------|------|------|----------|-----------|---------|------|
| **FlexAvatar** | 独立方法 | 单图 | 头部 | ✅ 可行 | ⭐⭐⭐ 高 | 已接入 |
| **HyperGaussians** | 增强模块 | - | 头部 | ✅ 可行 | ⭐⭐ 中 | 可作为增强 |
| **MATCH** | 独立方法 | 多视角 | 头部 | ❌ 需多视角+SM90 | ⭐ 低 | 不接入 |
| **AniGS** | 独立方法 | 单图 | 全身 | ⚠️ 扩散模型显存高 | ⭐ 中 | 参考价值 |

### 下一步

1. **FlexAvatar**：已在评测框架中创建适配器，待 GPU 环境验证
2. **HyperGaussians**：可考虑集成到 FlexAvatar 适配器中作为渲染增强
3. **MATCH/AniGS**：记录为技术路线参考，暂不接入
