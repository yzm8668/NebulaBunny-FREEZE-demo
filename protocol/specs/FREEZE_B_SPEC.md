# FREEZE-B 协议规范（proto_version = 1.0.0）

FREEZE-B 是一个「结果-only 包」，用于承载 drift / execution / stability 等指标，完全不包含策略逻辑实现。

它通常在以下场景使用：
- 向审计方 / 合规部门展示某策略在一段时间内的表现；
- 向潜在合作方证明：在指定五指纹下，策略运行结果满足某些门槛（stability gates）；
- 与 FREEZE-A 结合，形成「结构 + 结果」的完整证据链。

---

## 核心字段（顶层）

- `proto_version`（string，必选）
  - 协议版本号，当前固定为 `"1.0.0"`。

- `package_type`（string，必选）
  - 固定为 `"FREEZE_B"`。

- `metadata`（object，必选）
  - 描述本结果包的基本信息和五指纹。

- `drift`（object，必选）
  - 漂移相关指标（如 backtest vs shadow vs live 的对比）。

- `execution_audit`（object，必选）
  - 执行质量相关指标（成交价、滑点、成交比、maker/taker 比例等）。

- `quantile_distribution`（object，必选）
  - 在不同市场 regime 下 drift 的分位数（p50 / p90 / p95 等），以及 out-of-band 比例。

- `stress_windows`（object[]，必选）
  - 针对特定时间窗口（如高波动、低流动性）构造的压力测试结果。

- `stability_gates`（object，必选）
  - 一系列「是否达标」的稳定性门槛，例如：
    - `drift_median_bps <= X`
    - `max_drawdown <= Y`
    - 等等，以布尔标记 + 阈值形式记录。

- `manifest`（object，必选）
  - 结果文件清单。

- `hashes` / `evidence` / `ots`（可选）
  - 与 FREEZE-A 中含义类似，用于增强包的完整性与时间戳证明。

---

## metadata 字段

`metadata` 至少包含：

- `id`（string，必选）
  - FREEZE-B 包 ID。

- `five_fingerprint`（object，必选）
  - 五指纹结构，指向某一特定的 code/data/spec/seed/env 组合。

- `description`（string，可选）
  - 对本结果包的口语化解释，例如「BTCUSDT 4h TWAP-MA，2025 Q1 影子盘审计结果」。

---

## drift / execution_audit / quantile_distribution

本版本不强制细化这些字段的内部结构，仅给出建议方向：

- `drift`
  - 例如：
    - `backtest_vs_shadow_bps`：分位数统计；
    - `shadow_vs_live_bps`：分位数统计；
    - 各类聚合统计（mean / median / max 等）。

- `execution_audit`
  - 例如：
    - `avg_slippage_bps`
    - `maker_ratio`
    - `partial_fill_ratio`
    - `venue_breakdown` 等。

- `quantile_distribution`
  - 建议按「市场 regime」进行分桶，例如：
    - `vol_high` / `vol_low`
    - `spread_wide` / `spread_tight`
  - 每个桶记录 p50 / p90 / p95 以及 out-of-band 频率。

---

## stress_windows / stability_gates

- `stress_windows`（array）
  - 每个元素可以包含：
    - `label`：窗口名称；
    - `start` / `end`：时间范围；
    - 一组关键指标（如 MDD、drift_bps 上界等）。

- `stability_gates`（object）
  - 典型结构可以是：
    - `gate_name`：
      - `passed`（bool）
      - `threshold`（number 或 string）
      - `observed`（number 或 string）

---

## 兼容性与扩展约定

- 与 FREEZE-A 类似：
  - `proto_version = "1.0.0"`；
  - 可以在保持向后兼容的前提下新增字段；
  - 破坏性修改必须 bump 主版本。
