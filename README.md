# Xiaomi 10 (umi) 内核构建（GitHub Actions）

已按参考仓库的构建思路重构：
- 参考来源：`SO-TS/android_kernel_xiaomi_sm8250`
- 参考链接：https://github.com/SO-TS/android_kernel_xiaomi_sm8250

## 现在的构建流程

Workflow：`.github/workflows/build-umi-kernel.yml`

特性：
1. 在 GitHub Actions 云端编译（避免本地准备复杂环境）
2. 使用参考方案一致的关键环节：
   - 依赖安装
   - ZyC Clang 工具链
   - `build.sh` 构建（支持 `device` 与 `ksu`）
3. 构建前预检：
   - 检查 `Makefile`
   - 检查 `${device}_defconfig` 是否存在
   - 输出内核版本（若 `<=5` 给警告，但继续构建）
4. 构建后质量门禁：
   - 必须生成目标设备 zip（文件名含 `_${device}_`）
   - zip 体积必须 >= `min_zip_mb`（默认 200MB，可调）
   - 不达标直接失败，避免“成功但产物错误”
5. 上传产物：通过门禁的 zip + 调试中间文件 + metadata

## 使用

在 Actions 手动触发 **Build Xiaomi 10 (umi) Kernel (Reference-style)**：
- `kernel_repo`：内核 GitHub 地址
- `kernel_branch`：分支
- `device`：默认 `umi`
- `ksu`：是否启用 KernelSU
- `min_zip_mb`：产物最小体积阈值（默认 200）

默认已填：
- `https://github.com/SO-TS/android_kernel_xiaomi_sm8250.git`
- `android16-aptusitu`
- `umi`
- `ksu=false`
- `min_zip_mb=200`

## 备注

你给的参考仓库是 4.x 内核系。当前 workflow 兼容这种来源，同时保留版本提示，便于后续切换到 >5 的内核源时复用同一流程。
