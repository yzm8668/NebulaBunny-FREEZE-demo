# five_fingerprint 规范

five_fingerprint 是 NebulaBunny 可复现体系的核心指纹，用于唯一标识一次「环境 + 口径 + 随机性」组合。

结构定义：
- 满足 `five_fingerprint.schema.json`；
- 顶层包含 5 个字段：

1. `code_git_hash`（string）
   - 负责记录代码版本；
   - 一般为完整或截断的 Git commit hash；
   - 要求：能在仓库中唯一定位到某个 commit。

2. `data_version`（string）
   - 负责记录数据快照版本；
   - 可以是日期区间 + 供应商标识 + 内部校验号的组合；
   - 要求：给定 data_version，应能在内部数据仓库中唯一定址。

3. `spec_hash`（string）
   - 负责记录撮合 / 费用 / 精度 / 风控等「口径」的指纹；
   - 通常定义为 `SHA1(engine_spec.yaml)[:12]`；
   - 一旦 engine_spec.yaml 有任何更改（包括门槛、费用、撮合规则），必须重新计算 spec_hash。

4. `random_seed`（integer）
   - 负责记录全局随机种子；
   - 涉及随机化策略 / Monte Carlo / 采样等场景时，必须固定此种子以实现可复现。

5. `env_fingerprint`（string）
   - 负责记录运行环境指纹；
   - 建议由以下信息组合得到：
     - OS（含版本）
     - Python 版本
     - 关键依赖库及版本（如 numpy/pandas/numba/blas 实现等）
   - 具体格式可以是：
     - JSON dump 的哈希；
     - 或者经过压缩后的短字符串，只要能在内部展开即可。

---

## 设计原则

- five_fingerprint 应当是：
  - **人类可读**（至少能手动对照）；
  - **机器可解析**（用于自动比对）；
  - **单调稳定**（同一套环境与口径下，多次生成应一致）。

- 在 FREEZE-A / FREEZE-B / 其他证据包中：
  - five_fingerprint 是连接不同 artefact 的主键；
  - 任何一指纹发生变化，都应该视作一个新的「世界线」。

---

## 版本与扩展

- 当前版本只定义这 5 个字段；
- 不建议随意增加第 6、7 个字段；
- 如确有扩展需求，可以：
  - 在上层 metadata 中增加补充信息；
  - 或者在 `env_fingerprint` 内部结构里嵌入更多细节。
