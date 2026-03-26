"""
Data Warehouse Utilities
Utilities for managing and validating data in the warehouse
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class DataWarehouse:
    """Main class for interacting with the data warehouse"""
    
    def __init__(self, warehouse_root: str = "data_warehouse"):
        self.warehouse_root = Path(warehouse_root)
        self.sft_training_path = self.warehouse_root / "sft_training_data"
        self.evaluation_path = self.warehouse_root / "evaluation_data"
        self.schemas_path = self.warehouse_root / "schemas"
        
    def get_all_sft_data(self, data_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load all SFT training data
        
        Args:
            data_type: Optional filter by type (conversation, instruction, qa)
        
        Returns:
            List of training data samples
        """
        all_data = []
        search_path = self.sft_training_path / data_type if data_type else self.sft_training_path
        
        for json_file in search_path.rglob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
        
        return all_data
    
    def get_all_evaluation_data(self, eval_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load all evaluation data
        
        Args:
            eval_type: Optional filter by type (benchmark, custom_test, model_comparison)
        
        Returns:
            List of evaluation data samples
        """
        all_data = []
        search_path = self.evaluation_path / eval_type if eval_type else self.evaluation_path
        
        for json_file in search_path.rglob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
        
        return all_data
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the data warehouse
        
        Returns:
            Dictionary containing statistics
        """
        stats = {
            "sft_training_data": {
                "total": 0,
                "by_type": {}
            },
            "evaluation_data": {
                "total": 0,
                "by_type": {}
            }
        }
        
        # SFT training data stats
        for data_type in ["conversation", "instruction", "qa"]:
            data = self.get_all_sft_data(data_type)
            count = len(data)
            stats["sft_training_data"]["by_type"][data_type] = count
            stats["sft_training_data"]["total"] += count
        
        # Evaluation data stats
        for eval_type in ["benchmark", "custom_test", "model_comparison"]:
            data = self.get_all_evaluation_data(eval_type)
            count = len(data)
            stats["evaluation_data"]["by_type"][eval_type] = count
            stats["evaluation_data"]["total"] += count
        
        return stats
    
    def validate_data(self, data: Dict[str, Any], schema_type: str) -> tuple[bool, List[str]]:
        """
        Validate data against schema
        
        Args:
            data: Data to validate
            schema_type: Type of schema (sft_training or evaluation)
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Basic validation - check required fields
        if schema_type == "sft_training":
            if "id" not in data:
                errors.append("Missing required field: id")
            if "type" not in data:
                errors.append("Missing required field: type")
            elif data["type"] not in ["conversation", "instruction", "qa"]:
                errors.append(f"Invalid type: {data['type']}")
            
            # Type-specific validation
            if data.get("type") == "conversation" and "conversation" not in data:
                errors.append("conversation type requires 'conversation' field")
            elif data.get("type") == "instruction" and ("instruction" not in data or "output" not in data):
                errors.append("instruction type requires 'instruction' and 'output' fields")
            elif data.get("type") == "qa" and ("question" not in data or "answer" not in data):
                errors.append("qa type requires 'question' and 'answer' fields")
        
        elif schema_type == "evaluation":
            if "id" not in data:
                errors.append("Missing required field: id")
            if "eval_type" not in data:
                errors.append("Missing required field: eval_type")
            elif data["eval_type"] not in ["benchmark", "custom_test", "model_comparison"]:
                errors.append(f"Invalid eval_type: {data['eval_type']}")
            if "task" not in data:
                errors.append("Missing required field: task")
            if "prompt" not in data:
                errors.append("Missing required field: prompt")
        
        return len(errors) == 0, errors
    
    def add_sft_data(self, data: Dict[str, Any], filename: str) -> bool:
        """
        Add new SFT training data to the warehouse
        
        Args:
            data: Training data to add
            filename: Name of the file to save
        
        Returns:
            True if successful
        """
        is_valid, errors = self.validate_data(data, "sft_training")
        if not is_valid:
            print(f"Validation errors: {errors}")
            return False
        
        data_type = data.get("type")
        if data_type not in ["conversation", "instruction", "qa"]:
            print(f"Invalid data type: {data_type}")
            return False
        
        output_path = self.sft_training_path / data_type / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    
    def add_evaluation_data(self, data: Dict[str, Any], filename: str) -> bool:
        """
        Add new evaluation data to the warehouse
        
        Args:
            data: Evaluation data to add
            filename: Name of the file to save
        
        Returns:
            True if successful
        """
        is_valid, errors = self.validate_data(data, "evaluation")
        if not is_valid:
            print(f"Validation errors: {errors}")
            return False
        
        eval_type = data.get("eval_type")
        if eval_type not in ["benchmark", "custom_test", "model_comparison"]:
            print(f"Invalid eval type: {eval_type}")
            return False
        
        output_path = self.evaluation_path / eval_type / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True


def print_statistics():
    """Print warehouse statistics"""
    dw = DataWarehouse()
    stats = dw.get_statistics()
    
    print("=" * 60)
    print("Data Warehouse Statistics")
    print("=" * 60)
    print("\nSFT Training Data:")
    print(f"  Total samples: {stats['sft_training_data']['total']}")
    for data_type, count in stats['sft_training_data']['by_type'].items():
        print(f"    - {data_type}: {count}")
    
    print("\nEvaluation Data:")
    print(f"  Total samples: {stats['evaluation_data']['total']}")
    for eval_type, count in stats['evaluation_data']['by_type'].items():
        print(f"    - {eval_type}: {count}")
    print("=" * 60)


if __name__ == "__main__":
    print_statistics()
