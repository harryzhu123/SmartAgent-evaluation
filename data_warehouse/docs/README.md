# 数据仓库文档 / Data Warehouse Documentation

## 概述 / Overview

本数据仓库用于存储和管理用于大模型训练的SFT（Supervised Fine-Tuning）训练数据和评测数据。

This data warehouse is designed to store and manage SFT (Supervised Fine-Tuning) training data and evaluation data for large language model training.

## 目录结构 / Directory Structure

```
data_warehouse/
├── sft_training_data/          # SFT训练数据 / SFT training data
│   ├── conversation/           # 多轮对话数据 / Multi-turn conversation data
│   ├── instruction/            # 指令-响应数据 / Instruction-response data
│   └── qa/                     # 问答数据 / Question-answer data
├── evaluation_data/            # 评测数据 / Evaluation data
│   ├── benchmark/              # 标准基准测试 / Standard benchmarks
│   ├── custom_test/            # 自定义测试 / Custom tests
│   └── model_comparison/       # 模型对比测试 / Model comparison tests
├── schemas/                    # 数据格式定义 / Data schema definitions
│   ├── sft_training_schema.json
│   └── evaluation_schema.json
├── utils/                      # 工具脚本 / Utility scripts
│   ├── data_utils.py
│   └── data_loader.py
└── docs/                       # 文档 / Documentation
```

## SFT训练数据 / SFT Training Data

### 数据类型 / Data Types

#### 1. 对话数据 (Conversation)
多轮对话格式，适用于对话系统训练。

Multi-turn conversation format, suitable for dialogue system training.

**示例 / Example:**
```json
{
  "id": "conv_001",
  "type": "conversation",
  "conversation": [
    {"role": "system", "content": "你是一个有帮助的AI助手"},
    {"role": "user", "content": "请介绍一下机器学习"},
    {"role": "assistant", "content": "机器学习是..."}
  ],
  "metadata": {
    "language": "zh",
    "domain": "机器学习",
    "difficulty": "easy"
  }
}
```

#### 2. 指令数据 (Instruction)
单轮指令-响应格式，适用于指令跟随训练。

Single-turn instruction-response format, suitable for instruction-following training.

**示例 / Example:**
```json
{
  "id": "inst_001",
  "type": "instruction",
  "instruction": "将以下英文翻译成中文",
  "input": "Machine learning is a subset of AI.",
  "output": "机器学习是人工智能的一个子集。",
  "metadata": {
    "language": "zh",
    "domain": "翻译"
  }
}
```

#### 3. 问答数据 (QA)
问答对格式，适用于知识问答训练。

Question-answer format, suitable for knowledge QA training.

**示例 / Example:**
```json
{
  "id": "qa_001",
  "type": "qa",
  "question": "什么是GPU？",
  "answer": "GPU是图形处理器...",
  "metadata": {
    "language": "zh",
    "domain": "计算机硬件"
  }
}
```

## 评测数据 / Evaluation Data

### 评测类型 / Evaluation Types

#### 1. 基准测试 (Benchmark)
标准化的基准测试，如MMLU、GSM8K等。

Standardized benchmarks such as MMLU, GSM8K, etc.

**示例 / Example:**
```json
{
  "id": "bench_001",
  "eval_type": "benchmark",
  "task": "MMLU - Machine Learning",
  "prompt": "Which of the following...",
  "expected_output": "D",
  "evaluation_criteria": {
    "metrics": ["exact_match"],
    "threshold": 1.0
  },
  "metadata": {
    "benchmark_name": "MMLU",
    "domain": "machine_learning"
  }
}
```

#### 2. 自定义测试 (Custom Test)
定制化的测试用例，用于特定能力评估。

Customized test cases for specific capability assessment.

#### 3. 模型对比 (Model Comparison)
用于不同模型间的A/B测试和对比评估。

For A/B testing and comparative evaluation between different models.

## 使用方法 / Usage

### 加载数据 / Loading Data

```python
from data_warehouse.utils.data_loader import SFTDataLoader, EvaluationDataLoader

# 加载SFT训练数据 / Load SFT training data
sft_loader = SFTDataLoader()
conversations = sft_loader.load_conversations()
instructions = sft_loader.load_instructions()
qa_data = sft_loader.load_qa()

# 按语言过滤 / Filter by language
zh_data = sft_loader.load_by_language("zh")

# 加载评测数据 / Load evaluation data
eval_loader = EvaluationDataLoader()
benchmarks = eval_loader.load_benchmarks()
custom_tests = eval_loader.load_custom_tests()
```

### 数据统计 / Data Statistics

```python
from data_warehouse.utils.data_utils import DataWarehouse

dw = DataWarehouse()
stats = dw.get_statistics()
print(stats)
```

### 添加新数据 / Adding New Data

```python
from data_warehouse.utils.data_utils import DataWarehouse

dw = DataWarehouse()

# 添加SFT训练数据 / Add SFT training data
new_data = {
    "id": "new_001",
    "type": "instruction",
    "instruction": "Translate to English",
    "input": "你好世界",
    "output": "Hello World"
}
dw.add_sft_data(new_data, "new_instruction.json")

# 添加评测数据 / Add evaluation data
new_eval = {
    "id": "eval_001",
    "eval_type": "benchmark",
    "task": "Translation Test",
    "prompt": "Translate: 你好",
    "expected_output": "Hello"
}
dw.add_evaluation_data(new_eval, "new_benchmark.json")
```

## 数据格式规范 / Data Format Specifications

### 必需字段 / Required Fields

#### SFT训练数据 / SFT Training Data
- `id`: 唯一标识符 / Unique identifier
- `type`: 数据类型 (conversation/instruction/qa)
- 类型特定字段 / Type-specific fields:
  - conversation: `conversation` array
  - instruction: `instruction`, `output`
  - qa: `question`, `answer`

#### 评测数据 / Evaluation Data
- `id`: 唯一标识符 / Unique identifier
- `eval_type`: 评测类型 (benchmark/custom_test/model_comparison)
- `task`: 任务名称 / Task name
- `prompt`: 输入提示 / Input prompt

### 元数据字段 / Metadata Fields

可选但推荐包含以下元数据字段：

Optional but recommended metadata fields:

- `language`: 语言代码 (zh, en, etc.)
- `domain`: 领域或主题
- `difficulty`: 难度等级 (easy/medium/hard)
- `source`: 数据来源
- `created_at`: 创建时间 (ISO 8601格式)
- `tags`: 标签数组

## 评估指标 / Evaluation Metrics

支持的评估指标 / Supported metrics:

- `accuracy`: 准确率
- `bleu`: BLEU分数（机器翻译）
- `rouge`: ROUGE分数（文本摘要）
- `f1`: F1分数
- `perplexity`: 困惑度
- `human_eval`: 人工评估
- `exact_match`: 精确匹配
- `semantic_similarity`: 语义相似度

## 最佳实践 / Best Practices

1. **数据质量 / Data Quality**: 确保数据准确、完整、格式规范
2. **元数据完整性 / Metadata Completeness**: 尽可能提供完整的元数据信息
3. **版本控制 / Version Control**: 使用版本号追踪数据变更
4. **数据平衡 / Data Balance**: 注意不同类型、难度、领域的数据平衡
5. **定期验证 / Regular Validation**: 定期使用验证工具检查数据完整性

## 扩展指南 / Extension Guide

### 添加新的数据类型 / Adding New Data Types

1. 在相应目录下创建子目录
2. 更新schema定义
3. 在data_loader中添加加载方法
4. 更新文档

### 自定义评估指标 / Custom Evaluation Metrics

在evaluation_criteria中可以添加自定义指标和阈值。

## 许可证 / License

请根据项目需求添加适当的许可证信息。

Please add appropriate license information based on project requirements.

## 贡献指南 / Contributing

欢迎贡献数据和改进建议！请遵循以下步骤：

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 发起Pull Request

## 联系方式 / Contact

如有问题或建议，请通过GitHub Issues联系。

For questions or suggestions, please contact via GitHub Issues.
