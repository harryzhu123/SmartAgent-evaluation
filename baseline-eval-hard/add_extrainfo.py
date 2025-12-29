import json
import os
import sys
def add_extrainfo(original_file, predictions_file, output_file):
    """
    将原始数据中的 extra_info 添加到推理输出中
    
    Args:
        original_file: 原始数据文件路径
        predictions_file: 推理输出文件路径
        output_file: 输出文件路径
    """
    # 读取原始数据
    with open(original_file, "r") as f:
        original_data = json.load(f)

    # 读取推理输出
    with open(predictions_file, "r") as f:
        predictions = [json.loads(line) for line in f]

    # 合并 extra_info
    assert len(original_data) == len(predictions), "数据长度不匹配！"

    with open(output_file, "w", encoding="utf-8") as f:
        for orig, pred in zip(original_data, predictions):
            pred["extra_info"] = orig.get("extra_info", {})
            f.write(json.dumps(pred, ensure_ascii=False) + "\n")

    print(f"✅ 已保存到 {output_file}")
def convert_jsonl_to_json(input_file, output_file, remove_fields=None):
    """
    将 JSONL 文件转换为 JSON 文件
    
    Args:
        input_file: 输入的 JSONL 文件路径
        output_file: 输出的 JSON 文件路径
        remove_fields: 要移除的字段列表
    """
    if remove_fields is None:
        remove_fields = []
    
    # 读取 JSONL 文件
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                record = json.loads(line)
                
                # 处理 prompt 字段：删除所有 <|image_pad|>，只保留倒数第二个 <|im_start|> 之后的内容
                if 'prompt' in record:
                    prompt = record['prompt']
                    # 删除所有 <|image_pad|>
                    prompt = prompt.replace('<|image_pad|>', '')
                    # 找到所有 <|im_start|> 的位置
                    positions = []
                    start = 0
                    while True:
                        pos = prompt.find('<|im_start|>', start)
                        if pos == -1:
                            break
                        positions.append(pos)
                        start = pos + 1
                    
                    # 如果有至少2个 <|im_start|>，保留倒数第二个之后的内容
                    if len(positions) >= 2:
                        prompt = prompt[positions[-2]:]
                    elif len(positions) == 1:
                        # 只有1个，就保留这1个之后的内容
                        prompt = prompt[positions[0]:]
                    # 如果没有 <|im_start|>，保持原样
                    
                    record['prompt'] = prompt
                
                # 移除指定字段
                for field in remove_fields:
                    record.pop(field, None)
                data.append(record)
            except json.JSONDecodeError as e:
                print(f"⚠️  警告: 第 {line_num} 行解析失败: {e}")
                continue
    
    # 写入 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 输出统计信息
    print(f"✅ 转换完成!")
    print(f"   输入: {input_file} (JSONL 格式, {len(data)} 条记录)")
    print(f"   输出: {output_file} (JSON 格式)")
    
    if remove_fields:
        print(f"   已移除字段: {', '.join(remove_fields)}")
    
    if data:
        print(f"   保留字段: {', '.join(data[0].keys())}")
    
    # 显示文件大小
    size = os.path.getsize(output_file)
    if size > 1024 * 1024:
        print(f"   文件大小: {size / (1024 * 1024):.2f} MB")
    else:
        print(f"   文件大小: {size / 1024:.2f} KB")

if __name__ == "__main__":
    add_extrainfo(
        original_file="/data/zhuhairui/data/smartagent/smartagent-val-multiturn-eval.json",
        predictions_file="generated_predictions.jsonl",
        output_file="smartagent_predictions_with_extra_info.jsonl"
    )
    convert_jsonl_to_json(
        input_file="smartagent_predictions_with_extra_info.jsonl",
        output_file="smartagent_predictions_with_extra_info.json",
        remove_fields=[]  # 不移除任何字段，只处理 prompt
    )


