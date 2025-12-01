# NebulaBunny — nebula-freeze v1.0 发布前检查表

此 checklist 用于在 “推送到 GitHub 开源” 前进行人工确认。

----------------------------------------
1. Git 文件排查
----------------------------------------
- [ ] 运行：git ls-files | grep "engine-proprietary"  
      结果必须为空（engine-proprietary/ 不得被提交）
- [ ] .gitignore 中已明确排除 engine-proprietary/
- [ ] git status 中无误提交的敏感文件

----------------------------------------
2. README / SPEC 文档校验
----------------------------------------
- [ ] README 清楚说明 “本仓库只包含协议层，不含任何 drift/execution 内核”
- [ ] specs/ 中的 FREEZE_A_SPEC、FREEZE_B_SPEC、five_fingerprint.md 与 schema 保持一致
- [ ] reproducibility_principles.md 中无策略细节

----------------------------------------
3. 示例包审查
----------------------------------------
- [ ] freeze_a_example/ 为合成数据
- [ ] freeze_b_example/ 为合成数据
- [ ] 示例包中无真实账户信息 / 无 API Keys / 无内部敏感指标

----------------------------------------
4. validator 校验
----------------------------------------
- [ ] python protocol/validator/validate_freeze_a.py protocol/examples/freeze_a_example → PASS
- [ ] python protocol/validator/validate_freeze_b.py protocol/examples/freeze_b_example → PASS
- [ ] 如有 OTS 示例，确保 ots/info 输出正常或文档注明使用的是演示证书

----------------------------------------
5. LICENSE 校验
----------------------------------------
- [ ] protocol/ 层文件为 MIT LICENSE
- [ ] engine-proprietary/ 层文件为 LICENSE_BCL

----------------------------------------
6. 结构与版本号
----------------------------------------
- [ ] proto_version 全部为 "1.0.0"
- [ ] schema 中未出现未定义字段
- [ ] 有效 JSON 通过 json.tool 自检

----------------------------------------
7. 最终确认
----------------------------------------
- [ ] README、specs、examples 仅包含面向开源的演示内容
- [ ] engine-proprietary/ 中无算法、无业务参数（仅保留空目录）
- [ ] 准备打 tag：v1.0.0
