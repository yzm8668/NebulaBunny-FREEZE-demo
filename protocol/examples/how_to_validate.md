# 如何验证 FREEZE-A 示例包 (freeze_a_example)

本说明帮助新用户在没有任何 NebulaBunny 主工程的前提下，独立验证 FREEZE-A 包的结构。

---

## 1. 克隆仓库
git clone https://github.com/yourname/nebula-freeze.git

cd nebula-freeze/protocol/cli

---

## 2. 安装 nb-freeze (本地开发模式)
pip install -e .

---

## 3. 验证 FREEZE-A 示例包结构
示例包路径：

nebula-freeze/protocol/examples/freeze_a_example/

你应当看到：

[nb-freeze] FREEZE-A structure looks OK.

---

## 4. 方法说明

### FREEZE-A 用来提供：
- 五指纹（code_git_hash / data_version / spec_hash / random_seed / env_fingerprint）
- 文件清单 manifest
- 哈希 hashes（用于审计和完整性验证）
- 可选的 evidence/ots 时间戳目录

### 它不包含：
- 策略代码
- 执行逻辑
- drift / quantile / stress 等分析结果

---

## 5. 如何做破坏性测试

试着删掉 metadata.json 中的 `proto_version` 再验证：

python -m nb_freeze.validate_a ../examples/freeze_a_example


你会看到 validator 给出明确的错误提示。

FREEZE-A 协议设计出来，就是为了让结构验证无需任何信任。

---
