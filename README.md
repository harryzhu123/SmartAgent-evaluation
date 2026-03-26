# SmartAgent-evaluation

大模型SFT训练与评测数据仓库 / LLM SFT Training and Evaluation Data Warehouse

## 项目简介 / Project Overview

本项目提供了一个完整的数据仓库解决方案，用于存储和管理大语言模型（LLM）的监督微调（SFT）训练数据和评测数据。数据仓库采用标准化的数据格式，支持多种数据类型和评估方式，便于数据管理和模型训练。

This project provides a complete data warehouse solution for storing and managing Supervised Fine-Tuning (SFT) training data and evaluation data for Large Language Models (LLMs). The warehouse uses standardized data formats, supports multiple data types and evaluation methods, facilitating data management and model training.

## 主要特性 / Key Features

- ✅ **标准化数据格式** / Standardized data formats with JSON schema validation
- ✅ **多类型数据支持** / Multiple data type support (conversation, instruction, QA)
- ✅ **完整的评测体系** / Comprehensive evaluation system (benchmarks, custom tests, model comparison)
- ✅ **双语支持** / Bilingual support (Chinese and English)
- ✅ **便捷的工具集** / Convenient utilities for data loading and validation
- ✅ **详细的文档** / Detailed documentation and examples

## 数据仓库结构 / Warehouse Structure

```
data_warehouse/
├── sft_training_data/          # SFT训练数据
│   ├── conversation/           # 多轮对话 (2 samples)
│   ├── instruction/            # 指令跟随 (3 samples)
│   └── qa/                     # 问答数据 (3 samples)
├── evaluation_data/            # 评测数据
│   ├── benchmark/              # 标准基准测试 (3 samples)
│   ├── custom_test/            # 自定义测试 (2 samples)
│   └── model_comparison/       # 模型对比 (2 samples)
├── schemas/                    # 数据格式定义
│   ├── sft_training_schema.json
│   └── evaluation_schema.json
├── utils/                      # 工具脚本
│   ├── data_utils.py
│   └── data_loader.py
├── docs/                       # 详细文档
│   └── README.md
├── config.json                 # 配置文件
└── metadata.json              # 元数据跟踪
```

## 快速开始 / Quick Start

### 1. 查看数据统计 / View Statistics

```python
from data_warehouse.utils.data_utils import print_statistics

print_statistics()
```

### 2. 加载训练数据 / Load Training Data

```python
from data_warehouse.utils.data_loader import SFTDataLoader

# 创建加载器 / Create loader
loader = SFTDataLoader()

# 加载不同类型的数据 / Load different types of data
conversations = loader.load_conversations()
instructions = loader.load_instructions()
qa_data = loader.load_qa()

# 加载所有数据 / Load all data
all_data = loader.load_all(shuffle=True)

# 按语言过滤 / Filter by language
chinese_data = loader.load_by_language("zh")
```

### 3. 加载评测数据 / Load Evaluation Data

```python
from data_warehouse.utils.data_loader import EvaluationDataLoader

# 创建加载器 / Create loader
eval_loader = EvaluationDataLoader()

# 加载不同类型的评测数据 / Load different types of evaluation data
benchmarks = eval_loader.load_benchmarks()
custom_tests = eval_loader.load_custom_tests()
comparisons = eval_loader.load_model_comparisons()

# 按难度过滤 / Filter by difficulty
medium_tasks = eval_loader.load_by_difficulty("medium")
```

### 4. 添加新数据 / Add New Data

```python
from data_warehouse.utils.data_utils import DataWarehouse

dw = DataWarehouse()

# 添加SFT训练数据 / Add SFT training data
new_training_data = {
    "id": "inst_004",
    "type": "instruction",
    "instruction": "Write a hello world program",
    "output": "print('Hello, World!')",
    "metadata": {
        "language": "en",
        "domain": "programming"
    }
}
dw.add_sft_data(new_training_data, "new_instruction.json")
```

## 数据格式说明 / Data Format

### SFT训练数据类型 / SFT Training Data Types

1. **对话数据 (Conversation)**: 多轮对话，包含system/user/assistant角色
2. **指令数据 (Instruction)**: 指令-输入-输出格式
3. **问答数据 (QA)**: 问题-答案对

### 评测数据类型 / Evaluation Data Types

1. **基准测试 (Benchmark)**: 标准化测试（MMLU、GSM8K等）
2. **自定义测试 (Custom Test)**: 定制化测试用例
3. **模型对比 (Model Comparison)**: A/B测试和对比评估

### 支持的评估指标 / Supported Metrics

- `accuracy`: 准确率
- `bleu`: BLEU分数（机器翻译）
- `rouge`: ROUGE分数（文本摘要）
- `f1`: F1分数
- `exact_match`: 精确匹配
- `semantic_similarity`: 语义相似度
- `human_eval`: 人工评估

## 详细文档 / Detailed Documentation

完整的使用指南和API文档请参考：
[数据仓库文档](data_warehouse/docs/README.md)

For complete usage guide and API documentation, see:
[Data Warehouse Documentation](data_warehouse/docs/README.md)

## 数据覆盖 / Data Coverage

### 当前数据统计 / Current Statistics

- **SFT训练数据**: 8个样本 (2个对话 + 3个指令 + 3个问答)
- **评测数据**: 7个样本 (3个基准测试 + 2个自定义测试 + 2个模型对比)
- **支持语言**: 中文、英文
- **覆盖领域**: 机器学习、编程、翻译、NLP、数学等

### 支持的领域 / Supported Domains

- 机器学习 / Machine Learning
- 深度学习 / Deep Learning
- 自然语言处理 / Natural Language Processing
- 编程 / Programming
- 数学 / Mathematics
- 翻译 / Translation
- 问答系统 / Question Answering
- 对话系统 / Dialogue Systems

## 工具使用 / Utilities

### 数据验证 / Data Validation

```python
from data_warehouse.utils.data_utils import DataWarehouse

dw = DataWarehouse()
is_valid, errors = dw.validate_data(your_data, "sft_training")
if not is_valid:
    print(f"Validation errors: {errors}")
```

### 数据分割 / Data Splitting

```python
from data_warehouse.utils.data_loader import SFTDataLoader

loader = SFTDataLoader()
all_data = loader.load_all()
train_data, val_data = loader.split_train_val(all_data, val_ratio=0.1)
```

## 贡献指南 / Contributing

我们欢迎各种形式的贡献！包括但不限于：

- 添加新的训练数据
- 添加新的评测数据
- 改进工具和文档
- 报告问题和建议

Please feel free to contribute by:

- Adding new training data
- Adding new evaluation data
- Improving utilities and documentation
- Reporting issues and suggestions

## 版本历史 / Version History

- **v1.0.0** (2024-01-15): 初始版本，包含基础数据仓库结构和示例数据

## 许可证 / License

请根据项目需求添加适当的许可证。
Please add appropriate license based on project requirements.

## 联系方式 / Contact

如有问题或建议，请通过 GitHub Issues 联系。
For questions or suggestions, please contact via GitHub Issues.