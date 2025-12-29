# 快速参考指南 / Quick Reference Guide

## 常用命令 / Common Commands

### 查看统计信息 / View Statistics

```bash
python -c "from data_warehouse.utils import print_statistics; print_statistics()"
```

### 运行示例 / Run Example

```bash
python example.py
```

## 常用代码片段 / Common Code Snippets

### 加载所有训练数据 / Load All Training Data

```python
from data_warehouse.utils import SFTDataLoader

loader = SFTDataLoader()
data = loader.load_all(shuffle=True)
```

### 加载特定类型数据 / Load Specific Data Type

```python
# 对话数据 / Conversations
conversations = loader.load_conversations()

# 指令数据 / Instructions
instructions = loader.load_instructions()

# 问答数据 / QA
qa_data = loader.load_qa()
```

### 按语言过滤 / Filter by Language

```python
chinese_data = loader.load_by_language("zh")
english_data = loader.load_by_language("en")
```

### 按领域过滤 / Filter by Domain

```python
ml_data = loader.load_by_domain("机器学习")
coding_data = loader.load_by_domain("编程")
```

### 数据分割 / Split Data

```python
train_data, val_data = loader.split_train_val(data, val_ratio=0.2)
```

### 加载评测数据 / Load Evaluation Data

```python
from data_warehouse.utils import EvaluationDataLoader

eval_loader = EvaluationDataLoader()

# 所有评测数据 / All evaluation data
all_eval = eval_loader.load_all()

# 基准测试 / Benchmarks
benchmarks = eval_loader.load_benchmarks()

# 自定义测试 / Custom tests
custom = eval_loader.load_custom_tests()

# 模型对比 / Model comparisons
comparisons = eval_loader.load_model_comparisons()
```

### 按难度过滤评测数据 / Filter Evaluation by Difficulty

```python
easy = eval_loader.load_by_difficulty("easy")
medium = eval_loader.load_by_difficulty("medium")
hard = eval_loader.load_by_difficulty("hard")
```

### 验证数据 / Validate Data

```python
from data_warehouse.utils import DataWarehouse

dw = DataWarehouse()

# 验证SFT训练数据 / Validate SFT training data
is_valid, errors = dw.validate_data(your_data, "sft_training")

# 验证评测数据 / Validate evaluation data
is_valid, errors = dw.validate_data(your_eval_data, "evaluation")
```

### 添加新数据 / Add New Data

```python
# 添加训练数据 / Add training data
new_data = {
    "id": "new_001",
    "type": "instruction",
    "instruction": "Your instruction",
    "output": "Your output",
    "metadata": {
        "language": "zh",
        "domain": "编程"
    }
}
dw.add_sft_data(new_data, "new_data.json")

# 添加评测数据 / Add evaluation data
new_eval = {
    "id": "eval_new_001",
    "eval_type": "benchmark",
    "task": "Your task",
    "prompt": "Your prompt",
    "expected_output": "Expected result"
}
dw.add_evaluation_data(new_eval, "new_eval.json")
```

### 获取统计信息 / Get Statistics

```python
stats = dw.get_statistics()
print(f"Total SFT samples: {stats['sft_training_data']['total']}")
print(f"Total evaluation samples: {stats['evaluation_data']['total']}")
```

## 数据格式模板 / Data Format Templates

### SFT训练数据模板 / SFT Training Data Templates

#### 对话格式 / Conversation Format

```json
{
  "id": "conv_xxx",
  "type": "conversation",
  "conversation": [
    {"role": "system", "content": "系统提示"},
    {"role": "user", "content": "用户消息"},
    {"role": "assistant", "content": "助手回复"}
  ],
  "metadata": {
    "language": "zh",
    "domain": "领域",
    "difficulty": "easy"
  }
}
```

#### 指令格式 / Instruction Format

```json
{
  "id": "inst_xxx",
  "type": "instruction",
  "instruction": "指令内容",
  "input": "可选的输入",
  "output": "期望的输出",
  "metadata": {
    "language": "zh",
    "domain": "领域"
  }
}
```

#### 问答格式 / QA Format

```json
{
  "id": "qa_xxx",
  "type": "qa",
  "question": "问题",
  "answer": "答案",
  "metadata": {
    "language": "zh",
    "domain": "领域"
  }
}
```

### 评测数据模板 / Evaluation Data Templates

#### 基准测试格式 / Benchmark Format

```json
{
  "id": "bench_xxx",
  "eval_type": "benchmark",
  "task": "任务名称",
  "prompt": "测试提示",
  "expected_output": "期望输出",
  "evaluation_criteria": {
    "metrics": ["exact_match"],
    "threshold": 1.0
  },
  "metadata": {
    "benchmark_name": "基准名称",
    "language": "zh",
    "domain": "领域"
  }
}
```

## 支持的值 / Supported Values

### 数据类型 / Data Types
- SFT: `conversation`, `instruction`, `qa`
- Evaluation: `benchmark`, `custom_test`, `model_comparison`

### 语言代码 / Language Codes
- 中文: `zh`
- 英文: `en`

### 难度等级 / Difficulty Levels
- `easy` (简单)
- `medium` (中等)
- `hard` (困难)

### 评估指标 / Evaluation Metrics
- `accuracy` - 准确率
- `bleu` - BLEU分数
- `rouge` - ROUGE分数
- `f1` - F1分数
- `perplexity` - 困惑度
- `human_eval` - 人工评估
- `exact_match` - 精确匹配
- `semantic_similarity` - 语义相似度

## 文件路径 / File Paths

- SFT对话数据: `data_warehouse/sft_training_data/conversation/`
- SFT指令数据: `data_warehouse/sft_training_data/instruction/`
- SFT问答数据: `data_warehouse/sft_training_data/qa/`
- 基准测试: `data_warehouse/evaluation_data/benchmark/`
- 自定义测试: `data_warehouse/evaluation_data/custom_test/`
- 模型对比: `data_warehouse/evaluation_data/model_comparison/`
- Schema定义: `data_warehouse/schemas/`
- 工具脚本: `data_warehouse/utils/`

## 常见问题 / FAQ

**Q: 如何添加新的数据类型？**
A: 在相应目录创建子目录，更新schema，在data_loader中添加加载方法。

**Q: 支持哪些数据格式？**
A: 目前支持JSON格式，建议使用UTF-8编码。

**Q: 如何处理大量数据？**
A: 可以将数据分成多个JSON文件，loader会自动加载所有文件。

**Q: 元数据是必需的吗？**
A: 不是必需的，但强烈建议添加以便更好地管理和过滤数据。
