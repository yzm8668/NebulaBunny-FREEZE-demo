# nebula-freeze (protocol layer)

本仓库只包含 NebulaBunny 的「协议层」与「示例层」内容，用于开源发布。
它不包含任何 drift/execution/stress/replay 等商业闭源内核。

结构说明：
- protocol/  （MIT 开源协议层）
  - schemas/：FREEZE-A / FREEZE-B / five_fingerprint 的 JSON Schema
  - specs/：协议文档、字段定义、可复现说明
  - cli/nb_freeze/：nb-freeze CLI 的开源壳（generate-a / validate-a/b）
  - examples/：FREEZE-A/B 示例包（合成数据）
  - validator/：结构校验 + OTS 验证脚本（无任何策略或执行逻辑）

- engine-proprietary/ （不开源，BCL 商业内核）
  *此目录只在本地存在，不会推送至 GitHub。*
  *包括 drift_engine / execution_engine / stress_cost_engine / replay_engine 等真正逻辑。*

本仓库只是协议层定义，不包含任何策略、撮合、费用、延迟、风控等逻辑。

后续发布到 GitHub 时，engine-proprietary/ 将完全被排除。
