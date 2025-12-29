"""
示例脚本：演示如何使用数据仓库
Example Script: Demonstrates how to use the data warehouse
"""

import sys
from pathlib import Path

# 添加data_warehouse到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from data_warehouse.utils.data_loader import SFTDataLoader, EvaluationDataLoader
from data_warehouse.utils.data_utils import DataWarehouse, print_statistics


def main():
    print("=" * 70)
    print("数据仓库示例脚本 / Data Warehouse Example Script")
    print("=" * 70)
    print()
    
    # 1. 显示统计信息 / Show statistics
    print("1. 数据仓库统计 / Data Warehouse Statistics")
    print("-" * 70)
    print_statistics()
    print()
    
    # 2. 加载SFT训练数据 / Load SFT training data
    print("2. 加载SFT训练数据示例 / Loading SFT Training Data Examples")
    print("-" * 70)
    sft_loader = SFTDataLoader()
    
    # 加载对话数据
    conversations = sft_loader.load_conversations()
    print(f"✓ 已加载 {len(conversations)} 个对话样本")
    if conversations:
        print(f"  示例: {conversations[0]['id']} - {conversations[0]['metadata']['domain']}")
    
    # 加载指令数据
    instructions = sft_loader.load_instructions()
    print(f"✓ 已加载 {len(instructions)} 个指令样本")
    if instructions:
        print(f"  示例: {instructions[0]['id']} - {instructions[0]['instruction'][:50]}...")
    
    # 加载问答数据
    qa_data = sft_loader.load_qa()
    print(f"✓ 已加载 {len(qa_data)} 个问答样本")
    if qa_data:
        print(f"  示例: {qa_data[0]['id']} - {qa_data[0]['question'][:50]}...")
    
    # 按语言过滤
    zh_data = sft_loader.load_by_language("zh")
    en_data = sft_loader.load_by_language("en")
    print(f"✓ 中文样本: {len(zh_data)} 个, 英文样本: {len(en_data)} 个")
    print()
    
    # 3. 加载评测数据 / Load evaluation data
    print("3. 加载评测数据示例 / Loading Evaluation Data Examples")
    print("-" * 70)
    eval_loader = EvaluationDataLoader()
    
    # 加载基准测试
    benchmarks = eval_loader.load_benchmarks()
    print(f"✓ 已加载 {len(benchmarks)} 个基准测试")
    if benchmarks:
        print(f"  示例: {benchmarks[0]['id']} - {benchmarks[0]['task']}")
    
    # 加载自定义测试
    custom_tests = eval_loader.load_custom_tests()
    print(f"✓ 已加载 {len(custom_tests)} 个自定义测试")
    if custom_tests:
        print(f"  示例: {custom_tests[0]['id']} - {custom_tests[0]['task']}")
    
    # 加载模型对比测试
    comparisons = eval_loader.load_model_comparisons()
    print(f"✓ 已加载 {len(comparisons)} 个模型对比测试")
    if comparisons:
        print(f"  示例: {comparisons[0]['id']} - {comparisons[0]['task']}")
    
    # 按难度过滤
    easy_tasks = eval_loader.load_by_difficulty("easy")
    medium_tasks = eval_loader.load_by_difficulty("medium")
    print(f"✓ 简单任务: {len(easy_tasks)} 个, 中等任务: {len(medium_tasks)} 个")
    print()
    
    # 4. 数据验证示例 / Data validation example
    print("4. 数据验证示例 / Data Validation Example")
    print("-" * 70)
    dw = DataWarehouse()
    
    # 验证一个训练样本
    if conversations:
        is_valid, errors = dw.validate_data(conversations[0], "sft_training")
        print(f"✓ 验证对话数据: {'通过' if is_valid else '失败'}")
        if errors:
            for error in errors:
                print(f"  错误: {error}")
    
    # 验证一个评测样本
    if benchmarks:
        is_valid, errors = dw.validate_data(benchmarks[0], "evaluation")
        print(f"✓ 验证评测数据: {'通过' if is_valid else '失败'}")
        if errors:
            for error in errors:
                print(f"  错误: {error}")
    print()
    
    # 5. 数据分割示例 / Data splitting example
    print("5. 数据分割示例 / Data Splitting Example")
    print("-" * 70)
    all_sft_data = sft_loader.load_all()
    train_data, val_data = sft_loader.split_train_val(all_sft_data, val_ratio=0.2)
    print(f"✓ 总样本数: {len(all_sft_data)}")
    print(f"✓ 训练集: {len(train_data)} 个样本 ({len(train_data)/len(all_sft_data)*100:.1f}%)")
    print(f"✓ 验证集: {len(val_data)} 个样本 ({len(val_data)/len(all_sft_data)*100:.1f}%)")
    print()
    
    # 6. 展示数据样本 / Show data samples
    print("6. 数据样本展示 / Data Sample Display")
    print("-" * 70)
    
    if instructions:
        print("指令数据示例 / Instruction Sample:")
        sample = instructions[0]
        print(f"  ID: {sample['id']}")
        print(f"  类型: {sample['type']}")
        print(f"  指令: {sample['instruction']}")
        print(f"  输出: {sample['output'][:100]}...")
        print(f"  语言: {sample['metadata']['language']}")
        print(f"  领域: {sample['metadata']['domain']}")
    print()
    
    if benchmarks:
        print("评测数据示例 / Evaluation Sample:")
        sample = benchmarks[0]
        print(f"  ID: {sample['id']}")
        print(f"  任务: {sample['task']}")
        print(f"  提示: {sample['prompt'][:100]}...")
        print(f"  预期输出: {sample['expected_output']}")
        print(f"  评估指标: {sample['evaluation_criteria']['metrics']}")
    
    print()
    print("=" * 70)
    print("示例运行完成！/ Example completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
