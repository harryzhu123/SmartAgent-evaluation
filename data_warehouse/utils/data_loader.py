"""
Data Loader for SFT Training and Evaluation
Provides convenient functions to load and prepare data for model training and evaluation
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


class SFTDataLoader:
    """Loader for SFT training data"""
    
    def __init__(self, data_root: str = "data_warehouse/sft_training_data"):
        self.data_root = Path(data_root)
    
    def load_conversations(self, shuffle: bool = False) -> List[Dict[str, Any]]:
        """Load all conversation data"""
        data = []
        conv_path = self.data_root / "conversation"
        
        for json_file in conv_path.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
                if isinstance(file_data, list):
                    data.extend(file_data)
                else:
                    data.append(file_data)
        
        if shuffle:
            random.shuffle(data)
        
        return data
    
    def load_instructions(self, shuffle: bool = False) -> List[Dict[str, Any]]:
        """Load all instruction data"""
        data = []
        inst_path = self.data_root / "instruction"
        
        for json_file in inst_path.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
                if isinstance(file_data, list):
                    data.extend(file_data)
                else:
                    data.append(file_data)
        
        if shuffle:
            random.shuffle(data)
        
        return data
    
    def load_qa(self, shuffle: bool = False) -> List[Dict[str, Any]]:
        """Load all QA data"""
        data = []
        qa_path = self.data_root / "qa"
        
        for json_file in qa_path.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
                if isinstance(file_data, list):
                    data.extend(file_data)
                else:
                    data.append(file_data)
        
        if shuffle:
            random.shuffle(data)
        
        return data
    
    def load_all(self, shuffle: bool = False) -> List[Dict[str, Any]]:
        """Load all SFT training data"""
        data = []
        data.extend(self.load_conversations())
        data.extend(self.load_instructions())
        data.extend(self.load_qa())
        
        if shuffle:
            random.shuffle(data)
        
        return data
    
    def load_by_language(self, language: str, shuffle: bool = False) -> List[Dict[str, Any]]:
        """Load data filtered by language"""
        all_data = self.load_all()
        filtered_data = [
            item for item in all_data 
            if item.get("metadata", {}).get("language") == language
        ]
        
        if shuffle:
            random.shuffle(filtered_data)
        
        return filtered_data
    
    def load_by_domain(self, domain: str, shuffle: bool = False) -> List[Dict[str, Any]]:
        """Load data filtered by domain"""
        all_data = self.load_all()
        filtered_data = [
            item for item in all_data 
            if item.get("metadata", {}).get("domain") == domain
        ]
        
        if shuffle:
            random.shuffle(filtered_data)
        
        return filtered_data
    
    def split_train_val(self, data: List[Dict[str, Any]], 
                        val_ratio: float = 0.1) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Split data into training and validation sets"""
        random.shuffle(data)
        split_idx = int(len(data) * (1 - val_ratio))
        return data[:split_idx], data[split_idx:]


class EvaluationDataLoader:
    """Loader for evaluation data"""
    
    def __init__(self, data_root: str = "data_warehouse/evaluation_data"):
        self.data_root = Path(data_root)
    
    def load_benchmarks(self) -> List[Dict[str, Any]]:
        """Load all benchmark data"""
        data = []
        bench_path = self.data_root / "benchmark"
        
        for json_file in bench_path.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
                if isinstance(file_data, list):
                    data.extend(file_data)
                else:
                    data.append(file_data)
        
        return data
    
    def load_custom_tests(self) -> List[Dict[str, Any]]:
        """Load all custom test data"""
        data = []
        custom_path = self.data_root / "custom_test"
        
        for json_file in custom_path.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
                if isinstance(file_data, list):
                    data.extend(file_data)
                else:
                    data.append(file_data)
        
        return data
    
    def load_model_comparisons(self) -> List[Dict[str, Any]]:
        """Load all model comparison data"""
        data = []
        comp_path = self.data_root / "model_comparison"
        
        for json_file in comp_path.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
                if isinstance(file_data, list):
                    data.extend(file_data)
                else:
                    data.append(file_data)
        
        return data
    
    def load_all(self) -> List[Dict[str, Any]]:
        """Load all evaluation data"""
        data = []
        data.extend(self.load_benchmarks())
        data.extend(self.load_custom_tests())
        data.extend(self.load_model_comparisons())
        return data
    
    def load_by_benchmark(self, benchmark_name: str) -> List[Dict[str, Any]]:
        """Load data filtered by benchmark name"""
        all_data = self.load_all()
        filtered_data = [
            item for item in all_data 
            if item.get("metadata", {}).get("benchmark_name") == benchmark_name
        ]
        return filtered_data
    
    def load_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        """Load data filtered by domain"""
        all_data = self.load_all()
        filtered_data = [
            item for item in all_data 
            if item.get("metadata", {}).get("domain") == domain
        ]
        return filtered_data
    
    def load_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """Load data filtered by difficulty"""
        all_data = self.load_all()
        filtered_data = [
            item for item in all_data 
            if item.get("metadata", {}).get("difficulty") == difficulty
        ]
        return filtered_data


# Example usage
if __name__ == "__main__":
    # Load SFT training data
    print("Loading SFT Training Data...")
    sft_loader = SFTDataLoader()
    
    conversations = sft_loader.load_conversations()
    print(f"Loaded {len(conversations)} conversation samples")
    
    instructions = sft_loader.load_instructions()
    print(f"Loaded {len(instructions)} instruction samples")
    
    qa_data = sft_loader.load_qa()
    print(f"Loaded {len(qa_data)} QA samples")
    
    # Load by language
    zh_data = sft_loader.load_by_language("zh")
    print(f"Loaded {len(zh_data)} Chinese samples")
    
    # Load evaluation data
    print("\nLoading Evaluation Data...")
    eval_loader = EvaluationDataLoader()
    
    benchmarks = eval_loader.load_benchmarks()
    print(f"Loaded {len(benchmarks)} benchmark samples")
    
    custom_tests = eval_loader.load_custom_tests()
    print(f"Loaded {len(custom_tests)} custom test samples")
    
    comparisons = eval_loader.load_model_comparisons()
    print(f"Loaded {len(comparisons)} model comparison samples")
