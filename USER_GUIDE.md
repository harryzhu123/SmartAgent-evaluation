# 数据仓库使用指南 / Data Warehouse User Guide

## 目录 / Table of Contents

1. [简介 / Introduction](#简介--introduction)
2. [快速开始 / Quick Start](#快速开始--quick-start)
3. [数据结构 / Data Structure](#数据结构--data-structure)
4. [API文档 / API Documentation](#api文档--api-documentation)
5. [示例 / Examples](#示例--examples)
6. [最佳实践 / Best Practices](#最佳实践--best-practices)
7. [故障排除 / Troubleshooting](#故障排除--troubleshooting)

---

## 简介 / Introduction

SmartAgent数据仓库是一个专门为大语言模型（LLM）训练和评测设计的数据管理系统。它提供：

- 标准化的数据格式
- 灵活的数据加载工具
- 完整的数据验证机制
- 丰富的示例数据

SmartAgent Data Warehouse is a data management system designed specifically for LLM training and evaluation, providing standardized formats, flexible loading tools, complete validation mechanisms, and rich sample data.

---

## 快速开始 / Quick Start

### 安装 / Installation

无需安装外部依赖，仅需Python 3.7+即可使用。

No external dependencies required, only Python 3.7+ needed.

```bash
# 克隆仓库 / Clone repository
git clone https://github.com/harryzhu123/SmartAgent-evaluation.git
cd SmartAgent-evaluation

# 运行示例 / Run example
python example.py
```

### 第一个程序 / First Program

```python
from data_warehouse.utils import SFTDataLoader, print_statistics

# 显示统计信息 / Show statistics
print_statistics()

# 加载数据 / Load data
loader = SFTDataLoader()
data = loader.load_all()

print(f"Loaded {len(data)} samples")
```

---

## 数据结构 / Data Structure

### SFT训练数据 / SFT Training Data

训练数据分为三种类型 / Training data is divided into three types:

#### 1. 对话数据 (Conversation)

用于训练多轮对话能力 / For training multi-turn dialogue capabilities

**字段说明 / Field Description:**
- `id`: 唯一标识符 / Unique identifier
- `type`: 固定为 "conversation"
- `conversation`: 对话数组，包含多个消息 / Conversation array with multiple messages
  - `role`: 角色 (system/user/assistant)
  - `content`: 消息内容 / Message content
- `metadata`: 元数据 / Metadata

**使用场景 / Use Cases:**
- 客服对话系统 / Customer service dialogue
- 教育辅导对话 / Educational tutoring
- 技术问答对话 / Technical Q&A dialogue

#### 2. 指令数据 (Instruction)

用于训练指令跟随能力 / For training instruction-following capabilities

**字段说明 / Field Description:**
- `id`: 唯一标识符 / Unique identifier
- `type`: 固定为 "instruction"
- `instruction`: 指令内容 / Instruction content
- `input`: 可选的输入上下文 / Optional input context
- `output`: 期望的输出 / Expected output
- `metadata`: 元数据 / Metadata

**使用场景 / Use Cases:**
- 文本翻译 / Text translation
- 文本摘要 / Text summarization
- 代码生成 / Code generation
- 数据转换 / Data transformation

#### 3. 问答数据 (QA)

用于训练问答能力 / For training Q&A capabilities

**字段说明 / Field Description:**
- `id`: 唯一标识符 / Unique identifier
- `type`: 固定为 "qa"
- `question`: 问题 / Question
- `answer`: 答案 / Answer
- `metadata`: 元数据 / Metadata

**使用场景 / Use Cases:**
- 知识问答 / Knowledge Q&A
- 常见问题解答 / FAQ
- 学术问答 / Academic Q&A

### 评测数据 / Evaluation Data

评测数据分为三种类型 / Evaluation data is divided into three types:

#### 1. 基准测试 (Benchmark)

标准化的基准测试 / Standardized benchmarks

**常见基准 / Common Benchmarks:**
- MMLU: 多任务语言理解 / Massive Multitask Language Understanding
- GSM8K: 数学问题求解 / Grade School Math
- HumanEval: 代码生成评测 / Code generation evaluation
- C-Eval: 中文综合评测 / Chinese comprehensive evaluation

#### 2. 自定义测试 (Custom Test)

针对特定能力的定制化测试 / Customized tests for specific capabilities

#### 3. 模型对比 (Model Comparison)

用于A/B测试和模型对比 / For A/B testing and model comparison

---

## API文档 / API Documentation

### SFTDataLoader

SFT训练数据加载器 / SFT training data loader

#### Methods

##### `load_all(shuffle=False)`
加载所有训练数据 / Load all training data

**参数 / Parameters:**
- `shuffle` (bool): 是否随机打乱数据 / Whether to shuffle data

**返回 / Returns:**
- List[Dict]: 数据列表 / List of data samples

##### `load_conversations(shuffle=False)`
加载对话数据 / Load conversation data

##### `load_instructions(shuffle=False)`
加载指令数据 / Load instruction data

##### `load_qa(shuffle=False)`
加载问答数据 / Load QA data

##### `load_by_language(language, shuffle=False)`
按语言过滤数据 / Filter data by language

**参数 / Parameters:**
- `language` (str): 语言代码，如 "zh", "en" / Language code

##### `load_by_domain(domain, shuffle=False)`
按领域过滤数据 / Filter data by domain

**参数 / Parameters:**
- `domain` (str): 领域名称 / Domain name

##### `split_train_val(data, val_ratio=0.1)`
分割训练和验证数据 / Split training and validation data

**参数 / Parameters:**
- `data` (List[Dict]): 要分割的数据 / Data to split
- `val_ratio` (float): 验证集比例 / Validation ratio

**返回 / Returns:**
- Tuple[List, List]: (训练集, 验证集) / (train_set, val_set)

### EvaluationDataLoader

评测数据加载器 / Evaluation data loader

#### Methods

##### `load_all()`
加载所有评测数据 / Load all evaluation data

##### `load_benchmarks()`
加载基准测试数据 / Load benchmark data

##### `load_custom_tests()`
加载自定义测试数据 / Load custom test data

##### `load_model_comparisons()`
加载模型对比数据 / Load model comparison data

##### `load_by_benchmark(benchmark_name)`
按基准名称过滤 / Filter by benchmark name

##### `load_by_domain(domain)`
按领域过滤 / Filter by domain

##### `load_by_difficulty(difficulty)`
按难度过滤 / Filter by difficulty

**参数 / Parameters:**
- `difficulty` (str): "easy", "medium", 或 "hard"

### DataWarehouse

数据仓库管理类 / Data warehouse management class

#### Methods

##### `get_all_sft_data(data_type=None)`
获取所有SFT数据 / Get all SFT data

##### `get_all_evaluation_data(eval_type=None)`
获取所有评测数据 / Get all evaluation data

##### `get_statistics()`
获取统计信息 / Get statistics

**返回 / Returns:**
- Dict: 包含统计信息的字典 / Dictionary containing statistics

##### `validate_data(data, schema_type)`
验证数据 / Validate data

**参数 / Parameters:**
- `data` (Dict): 要验证的数据 / Data to validate
- `schema_type` (str): "sft_training" 或 "evaluation"

**返回 / Returns:**
- Tuple[bool, List[str]]: (是否有效, 错误列表) / (is_valid, errors)

##### `add_sft_data(data, filename)`
添加SFT数据 / Add SFT data

##### `add_evaluation_data(data, filename)`
添加评测数据 / Add evaluation data

---

## 示例 / Examples

### 示例1: 加载和过滤数据

```python
from data_warehouse.utils import SFTDataLoader

loader = SFTDataLoader()

# 加载中文数据 / Load Chinese data
zh_data = loader.load_by_language("zh")
print(f"Chinese samples: {len(zh_data)}")

# 加载编程领域数据 / Load programming domain data
coding_data = loader.load_by_domain("编程")
print(f"Coding samples: {len(coding_data)}")

# 加载并打乱所有数据 / Load and shuffle all data
all_data = loader.load_all(shuffle=True)
```

### 示例2: 训练数据准备

```python
from data_warehouse.utils import SFTDataLoader

loader = SFTDataLoader()

# 加载所有数据 / Load all data
all_data = loader.load_all()

# 分割训练和验证集 / Split train and validation
train_data, val_data = loader.split_train_val(all_data, val_ratio=0.2)

print(f"Training samples: {len(train_data)}")
print(f"Validation samples: {len(val_data)}")

# 处理训练数据 / Process training data
for sample in train_data:
    # 你的训练代码 / Your training code
    pass
```

### 示例3: 评测数据使用

```python
from data_warehouse.utils import EvaluationDataLoader

eval_loader = EvaluationDataLoader()

# 加载基准测试 / Load benchmarks
benchmarks = eval_loader.load_benchmarks()

# 运行评测 / Run evaluation
for test in benchmarks:
    prompt = test['prompt']
    expected = test['expected_output']
    # 运行你的模型 / Run your model
    # model_output = your_model(prompt)
    # 比较结果 / Compare results
```

### 示例4: 添加新数据

```python
from data_warehouse.utils import DataWarehouse

dw = DataWarehouse()

# 准备新数据 / Prepare new data
new_instruction = {
    "id": "inst_new_001",
    "type": "instruction",
    "instruction": "解释什么是Transformer架构",
    "output": "Transformer是一种基于自注意力机制的神经网络架构...",
    "metadata": {
        "language": "zh",
        "domain": "深度学习",
        "difficulty": "medium",
        "source": "自定义数据",
        "tags": ["Transformer", "架构", "深度学习"]
    }
}

# 添加到数据仓库 / Add to warehouse
success = dw.add_sft_data(new_instruction, "custom_instructions.json")
if success:
    print("Data added successfully!")
```

---

## 最佳实践 / Best Practices

### 1. 数据质量 / Data Quality

- ✅ 确保数据准确无误 / Ensure data accuracy
- ✅ 避免重复数据 / Avoid duplicate data
- ✅ 保持格式一致性 / Maintain format consistency
- ✅ 提供完整的元数据 / Provide complete metadata

### 2. 数据组织 / Data Organization

- ✅ 按类型分类存储 / Store by type
- ✅ 使用有意义的文件名 / Use meaningful filenames
- ✅ 添加描述性标签 / Add descriptive tags
- ✅ 记录数据来源 / Record data sources

### 3. 数据平衡 / Data Balance

- ✅ 平衡不同领域的数据 / Balance data across domains
- ✅ 平衡不同难度的数据 / Balance difficulty levels
- ✅ 考虑语言分布 / Consider language distribution

### 4. 版本控制 / Version Control

- ✅ 记录数据变更 / Track data changes
- ✅ 使用版本号 / Use version numbers
- ✅ 保持变更日志 / Maintain changelog

---

## 故障排除 / Troubleshooting

### 问题1: 导入错误

**错误:** `ModuleNotFoundError: No module named 'data_warehouse'`

**解决方案:**
```bash
# 确保在正确的目录 / Ensure in correct directory
cd /path/to/SmartAgent-evaluation

# 或添加到Python路径 / Or add to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/SmartAgent-evaluation"
```

### 问题2: 数据加载失败

**错误:** 无法加载JSON文件

**解决方案:**
- 检查文件路径是否正确 / Check file path
- 确认JSON格式正确 / Verify JSON format
- 检查文件编码为UTF-8 / Check UTF-8 encoding

### 问题3: 验证失败

**错误:** 数据验证不通过

**解决方案:**
- 检查必需字段 / Check required fields
- 确认数据类型正确 / Verify data types
- 参考schema定义 / Refer to schema definition

---

## 更多资源 / More Resources

- [快速参考指南 / Quick Reference](QUICK_REFERENCE.md)
- [详细文档 / Detailed Documentation](data_warehouse/docs/README.md)
- [示例脚本 / Example Script](example.py)
- [Schema定义 / Schema Definitions](data_warehouse/schemas/)

---

## 贡献 / Contributing

欢迎贡献！请参考以下步骤：

1. Fork项目 / Fork the project
2. 创建特性分支 / Create feature branch
3. 提交更改 / Commit changes
4. 推送到分支 / Push to branch
5. 创建Pull Request / Create Pull Request

---

## 许可证 / License

MIT License - 详见 [LICENSE](LICENSE) 文件
