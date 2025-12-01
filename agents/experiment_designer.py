"""
Experiment Designer Agent -  it designs experiments AND generates data
Merged with data generation
"""

import logging
from typing import Dict, List
import random
import numpy as np
import pandas as pd
from datetime import datetime


class ExperimentDesignerAgent:
    """
    Designs experiments and generates synthetic data
    """
    
    def __init__(self, memory_store):
        self.memory = memory_store
        self.logger = logging.getLogger("ExperimentDesignerAgent")
        np.random.seed(42)
        random.seed(42)
    
    async def design_experiment(self, hypothesis_output: Dict) -> Dict:
        """
        Design experiment AND generate data
        
        Args:
            hypothesis_output: Output from HypothesisAgent
            
        Returns:
            Experiment design + dataset
        """
        self.logger.info("Designing experiment and generating data...")
        
        hypothesis = hypothesis_output['hypothesis']
        hypothesis_type = hypothesis_output.get('hypothesis_type', 'causal')
        variables = {
            'independent': hypothesis_output['independent_variables'],
            'dependent': hypothesis_output['dependent_variables'],
            'control': hypothesis_output['control_variables']
        }
        
        # Design experiment
        design = await self._create_design(hypothesis_type, variables)
        methodology = await self._define_methodology(hypothesis_type)
        data_spec = await self._specify_data_requirements(variables, design)
        metrics = await self._define_metrics(variables['dependent'])
        analysis_plan = await self._create_analysis_plan(design)
        
        # Generate dataset
        self.logger.info(f"Generating {design['sample_size']} samples...")
        dataset = await self._generate_data(design, data_spec)
        
        result = {
            "experiment_type": design['type'],
            "design_structure": design['structure'],
            "methodology": methodology,
            "variables": variables,
            "sample_size": design['sample_size'],
            "groups": design['groups'],
            "number_of_groups": len(design['groups']),
            "data_specification": data_spec,
            "metrics": metrics,
            "analysis_plan": analysis_plan,
            "dataset": dataset,  # Include dataset
            "designed_at": datetime.now().isoformat()
        }
        
        self.logger.info(f"✓ Experiment designed: {design['sample_size']} samples")
        return result
    
    async def _create_design(self, hypothesis_type: str, variables: Dict) -> Dict:
        """Create experimental design"""
        
        if hypothesis_type == 'comparative':
            design_type = "Randomized Controlled Trial"
            num_groups = random.choice([2, 3])
        elif hypothesis_type == 'correlational':
            design_type = "Correlational Study"
            num_groups = 1
        else:
            design_type = "Experimental Design"
            num_groups = random.choice([2, 3, 4])
        
        sample_size = random.choice([100, 200, 500])
        samples_per_group = sample_size // num_groups
        
        groups = []
        groups.append({
            "name": "Control Group",
            "size": samples_per_group,
            "treatment": "baseline",
            "effect": 0.0
        })
        
        for i in range(1, num_groups):
            groups.append({
                "name": f"Treatment Group {i}",
                "size": samples_per_group,
                "treatment": f"condition_{i}",
                "effect": random.uniform(0.3, 0.6) * i  # Increasing effect
            })
        
        return {
            "type": design_type,
            "structure": "parallel_groups",
            "sample_size": sample_size,
            "groups": groups,
            "num_groups": num_groups
        }
    
    async def _define_methodology(self, hypothesis_type: str) -> Dict:
        """Define methodology"""
        return {
            "approach": f"{hypothesis_type.title()} research with statistical validation",
            "procedure": [
                "Random assignment to groups",
                "Baseline measurement",
                "Treatment application",
                "Outcome measurement",
                "Statistical analysis"
            ],
            "tools": ["Python", "NumPy", "Pandas", "SciPy", "Matplotlib"]
        }
    
    async def _specify_data_requirements(self, variables: Dict, design: Dict) -> Dict:
        """Specify data requirements"""
        features = []
        
        # Group column
        features.append({
            "name": "group",
            "type": "categorical",
            "categories": [g['name'] for g in design['groups']]
        })
        
        # IVs
        for var in variables['independent'][:2]:
            features.append({
                "name": var,
                "type": "continuous",
                "range": [0, 100],
                "distribution": "normal"
            })
        
        # DVs
        for var in variables['dependent'][:2]:
            features.append({
                "name": var,
                "type": "continuous",
                "range": [0, 1],
                "distribution": "normal"
            })
        
        # CVs
        for var in variables['control'][:2]:
            features.append({
                "name": var,
                "type": random.choice(["continuous", "categorical"]),
                "range": [0, 10]
            })
        
        return {"features": features}
    
    async def _define_metrics(self, dependent_vars: List[str]) -> List[str]:
        """Define metrics"""
        return [
            "mean_difference",
            "statistical_significance",
            "effect_size",
            "confidence_interval"
        ]
    
    async def _create_analysis_plan(self, design: Dict) -> Dict:
        """Create analysis plan"""
        if design['num_groups'] == 2:
            primary = "Independent t-test"
        else:
            primary = "One-way ANOVA"
        
        return {
            "primary_analysis": primary,
            "secondary_analyses": ["Descriptive statistics", "Effect sizes"],
            "significance_level": 0.05
        }
    
    async def _generate_data(self, design: Dict, data_spec: Dict) -> Dict:
        """Generate synthetic dataset"""
        
        all_data = []
        
        for group in design['groups']:
            group_size = group['size']
            group_name = group['name']
            treatment_effect = group['effect']
            
            group_data = {}
            group_data['group'] = [group_name] * group_size
            
            # Generate features
            for feature_spec in data_spec['features']:
                if feature_spec['name'] == 'group':
                    continue
                
                feature_name = feature_spec['name']
                feature_type = feature_spec['type']
                
                if feature_type == 'continuous':
                    mean = 50 + treatment_effect * 15  # Add treatment effect
                    std = 15
                    values = np.random.normal(mean, std, group_size)
                    values = np.clip(values, 0, 100)
                    group_data[feature_name] = values
                
                elif feature_type == 'categorical':
                    categories = feature_spec.get('categories', ['A', 'B', 'C'])
                    group_data[feature_name] = np.random.choice(categories, group_size)
                
                else:
                    group_data[feature_name] = np.random.uniform(0, 10, group_size)
            
            all_data.append(pd.DataFrame(group_data))
        
        # Combine all groups
        dataset = pd.concat(all_data, ignore_index=True)
        
        # Add sample IDs
        dataset.insert(0, 'sample_id', range(1, len(dataset) + 1))
        
        # Add timestamp
        dataset['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            "dataframe": dataset,
            "data": dataset.to_dict('records'),
            "num_samples": len(dataset),
            "num_features": len(dataset.columns),
            "features": list(dataset.columns)
        }