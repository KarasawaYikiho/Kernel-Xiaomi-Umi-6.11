# 贡献指南

[English Guide](./CONTRIBUTING.md)

感谢你参与改进 **Kernel-Xiaomi-Umi**。

## 适用范围

本仓库是**迁移编排仓库**（工作流 + 脚本 + 诊断），不是完整内核源码仓库。

## 开始前请先阅读

1. `README.zh-CN.md`
2. `Porting/README.md`
3. `Tools/Porting/README.md`
4. 最新 `PORTING_PLAN.md` 与 `Porting/CHANGELOG.md`

## 分支策略

遵循 `Porting/BRANCHING.md`：

- `port/phase*`：阶段性开发
- `port/hotfix-*`：紧急修复

## Pull Request 要求

请使用 PR 模板，并至少包含：

- 变更内容与动机
- 验证证据（run/artifacts/本地检查）
- 涉及 workflow/script 时的风险与回滚方案

## 参考源策略

允许使用的外部参考：

- `SO-TS/android_kernel_xiaomi_sm8250`
- `yefxx/xiaomi-umi-linux-kernel`
- `UtsavBalar1231/android_kernel_xiaomi_sm8150`
- `UtsavBalar1231/display-drivers`
- `UtsavBalar1231/camera-kernel`
- 作者 ID 发现源：`liyafe1997`（Strawing）

规则：

- 作者 ID 仅用于发现，集成前必须明确到具体仓库。
- 参考源仅作对比/借鉴输入，不做整树盲拷贝。
- 禁止导入官方 ROM 专有 blob。

## 质量要求

- 行为或输出变化时必须同步更新文档。
- 优先保证 CI 可复现，不接受仅本地可用改动。
- 新诊断脚本放在 `Tools/Porting/` 并补充索引文档。
- `Porting/CHANGELOG.md` 保持里程碑级、简洁记录。

## 安全要求

- 禁止提交密钥、令牌等敏感信息。
- 保持 `.gitignore` 干净，避免本地噪声入库。
- 生成工件默认视为临时产物，除非明确要求追踪。
