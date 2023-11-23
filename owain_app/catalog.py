
import os

import json
from typing import List, Dict

from loguru import logger

class Catalog:
    def __init__(self, base_path: str = None):
        if base_path is None:
            # Set base_path to the parent directory of the directory where catalog.py is located
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_path = base_path
        self.data_path = os.path.join(base_path, 'data')
        self.figures_path = os.path.join(base_path, 'figures')
        self.interaction_path = os.path.join(base_path, 'owain_app')
        self.test_path = os.path.join(base_path, 'tests')

    def save_dataset(self, dataset, rule_names, notation_type='set_notation'):
        dataset_name = '_and_'.join(rule_names)
        dir_path = os.path.join(self.data_path, notation_type, dataset_name)
        os.makedirs(dir_path, exist_ok=True)

        train_file = os.path.join(dir_path, 'train.jsonl')
        test_file = os.path.join(dir_path, 'test.jsonl')

        self._save_jsonl(dataset['train'], train_file)
        self._save_jsonl(dataset['test'], test_file)
        logger.info(f"Dataset for rules {dataset_name} saved in {dir_path}")

    def _save_jsonl(self, data, filepath):
        try:
            with open(filepath, 'w') as f:
                for item in data:
                    if isinstance(item, set):
                        item = list(item)  # Convert set to list
                    json.dump(item, f)
                    f.write('\n')
            logger.info(f"Data successfully saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving data to {filepath}: {e}")


    def data_load(self, rule_names: List[str], notation_type: str = 'set_notation') -> Dict[str, List[str]]:
        dataset_dir = os.path.join(self.data_path, f'{notation_type}_{"_and_".join(rule_names)}')
        train_file = os.path.join(dataset_dir, 'train.jsonl')
        test_file = os.path.join(dataset_dir, 'test.jsonl')

        return {
            'train': self._load_jsonl(train_file, notation_type),
            'test': self._load_jsonl(test_file, notation_type)
        }

    def data_save(self, data: Dict[str, List[str]], rule_names: List[str], notation_type: str = 'set_notation'):
        dataset_dir = os.path.join(self.data_path, f'{notation_type}_{"_and_".join(rule_names)}')
        os.makedirs(dataset_dir, exist_ok=True)

        train_file = os.path.join(dataset_dir, 'train.jsonl')
        test_file = os.path.join(dataset_dir, 'test.jsonl')

        self._save_jsonl(data['train'], train_file)
        self._save_jsonl(data['test'], test_file)

    def load_dataset(self, rule_names, notation_type='set_notation'):
        dataset_name = '_and_'.join(rule_names)
        dir_path = os.path.join(self.data_path, notation_type, dataset_name)
        
        train_file = os.path.join(dir_path, 'train.jsonl')
        test_file = os.path.join(dir_path, 'test.jsonl')

        train_data = self._load_jsonl(train_file, notation_type)
        test_data = self._load_jsonl(test_file, notation_type)

        return {'train': train_data, 'test': test_data}

    def _load_jsonl(self, filepath, notation_type):
        data = []
        with open(filepath, 'r') as file:
            for line in file:
                item = json.loads(line)
                if notation_type == 'set_notation':
                    item = set(item)  # Convert list back to set for set notation
                data.append(item)
        return data
    
    def save_response(self, response, filename):
        response_file = os.path.join(self.interaction_path, filename)
        with open(response_file, 'w') as file:
            file.write(response)
        logger.info(f"Response saved to {response_file}")


    # Additional methods can be added for other stages like interaction results and k-fold validation results.
