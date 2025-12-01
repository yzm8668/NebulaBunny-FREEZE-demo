# FREEZE-A 协议规范（proto_version = 1.0.0）

FREEZE-A 是一个「结构与环境证据包」，用于描述一次回测 / 影子 / 演化运行所依赖的：
- 代码指纹
- 数据版本
- 口径指纹（spec_hash）
- 随机种子
- 运行环境指纹（env_fingerprint）
- 以及与之相关的关键文件清单与哈希

其目标：
1. 让第三方在 **不接触策略细节** 的前提下，验证「我手上的结果包」确实来自某个明确的五指纹组合；
2. 为 FREEZE-B（结果包）的验证提供基础锚点。

---

## 核心字段（顶层）

- `proto_version`（string，必选）
  - 协议版本号，当前固定为 `"1.0.0"`。
  - 未来如果有 **破坏性修改**，必须将主版本号从 `1.x` 升级到 `2.0.0`，并提供迁移指引。

- `package_type`（string，必选）
  - 固定为 `"FREEZE_A"`，用于与 FREEZE_B 等其他包类型区分。

- `metadata`（object，必选）
  - 对当前 FREEZE-A 包的整体描述。

- `manifest`（object，必选）
  - 对应包内所有文件的清单。

- `hashes`（object，必选）
  - 文件哈希（通常为 sha256）的集中存放处。

- `evidence`（object，可选）
  - 电子签名、cosign 证明等附加证据，可为空。

- `ots`（object，可选）
  - 与 OpenTimestamps 相关的元数据（例如证明文件名、Bitcoin block merkle root 等）。

---

## metadata 字段

`metadata` 必须至少包含：

- `id`（string，必选）
  - FREEZE-A 包的唯一 ID，可使用 UUID 或策略自定义 ID。

- `five_fingerprint`（object，必选）
  - 五指纹结构，满足 `five_fingerprint.schema.json`。

- `description`（string，可选）
  - 对本包用途的自然语言描述，例如「BTCUSDT 4h TWAP MA 回测基线」。

- `universe`（string[]，可选）
  - 本次回测 / 影子所覆盖的品种列表，例如：`["BTCUSDT", "ETHUSDT"]`。

- `time_range`（object，可选）
  - `start`（string）：回测起始时间（ISO-8601 字符串）。
  - `end`（string）：回测结束时间（ISO-8601 字符串）。

---

## manifest.files

`manifest.files` 是一个数组，每个元素至少包含：

- `path`（string，必选）
  - 文件在包中的相对路径，例如 `"result/result.json"`。

- `role`（string，必选）
  - 文件的逻辑角色，例如：
    - `"result"`：主结果文件；
    - `"config"`：运行配置；
    - `"evidence"`：证据类文件等。

- `hash_key`（string，可选但推荐）
  - 指向 `hashes` 中某个键，用于获取该文件的哈希信息。

---

## hashes

`hashes` 是一个对象，键通常为文件路径或逻辑键。

每个值为：

- `algorithm`（string，必选）
  - 如 `"sha256"`。

- `value`（string，必选）
  - 哈希值的 16 进制字符串。

建议：
- 默认使用 `sha256`；
- 如果未来支持多种算法，可在 `algorithm` 中明确标注。

---

## 兼容性与扩展约定

- 本版本协议为 `proto_version = "1.0.0"`；
- 在不破坏既有字段含义、类型、必选性的前提下，可以新增可选字段；
- 增加可选字段 **不需要** 提升主版本，只需要提升到例如 `"1.1.0"`；
- 删除字段或改变字段语义视为破坏性修改，需要提升主版本（例如从 1.x 到 2.0.0）并在文档中提供迁移说明。
