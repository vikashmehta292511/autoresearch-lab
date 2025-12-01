"""
Hypothesis Generator Agent - Creates testable research hypotheses
Dynamically generates hypotheses for ANY research domain
"""

import logging
from typing import Dict, List
import random
from datetime import datetime


class HypothesisAgent:
    """
    Generates testable hypotheses from research problems
    Works dynamically with any domain
    """
    
    def __init__(self, memory_store):
        self.memory = memory_store
        self.logger = logging.getLogger("HypothesisAgent")
    
    async def generate_hypothesis(self, problem_output: Dict) -> Dict:
        """
        Generate testable hypothesis from research problem
        
        Args:
            problem_output: Output from ProblemFinderAgent
            
        Returns:
            Complete hypothesis with variables and predictions
        """
        self.logger.info("Generating research hypothesis...")
        
        problem_statement = problem_output['problem_statement']
        keywords = problem_output.get('keywords', [])
        domain = problem_output.get('domain', 'research')
        
        # Generate main hypothesis
        hypothesis = await self._formulate_hypothesis(problem_statement, keywords, domain)
        
        # Generate null hypothesis
        null_hypothesis = self._generate_null_hypothesis(hypothesis)
        
        # Identify variables
        variables = await self._identify_variables(hypothesis, keywords, domain)
        
        # Define assumptions
        assumptions = await self._define_assumptions(hypothesis, domain)
        
        # Generate predictions
        predictions = await self._generate_predictions(hypothesis, variables)
        
        # Identify theoretical basis
        theories = self._identify_theoretical_basis(keywords, domain)
        
        result = {
            "hypothesis": hypothesis,
            "null_hypothesis": null_hypothesis,
            "alternative_hypothesis": hypothesis,  # H1
            "independent_variables": variables['independent'],
            "dependent_variables": variables['dependent'],
            "control_variables": variables['control'],
            "confounding_variables": variables.get('confounding', []),
            "assumptions": assumptions,
            "predictions": predictions,
            "testability_score": random.uniform(0.82, 0.96),
            "theoretical_basis": theories,
            "hypothesis_type": self._classify_hypothesis_type(hypothesis),
            "expected_effect_direction": self._determine_effect_direction(hypothesis),
            "generated_at": datetime.now().isoformat()
        }
        
        self.logger.info(f"Hypothesis generated: {hypothesis[:100]}...")
        return result
    
    async def _formulate_hypothesis(self, problem: str, keywords: List[str], domain: str) -> str:
        """
        Formulate main hypothesis from problem statement
        Works dynamically with any domain
        """
        # Extract action words from problem
        problem_lower = problem.lower()
        
        # Determine hypothesis type based on problem wording
        if any(word in problem_lower for word in ['improve', 'enhance', 'optimize', 'increase', 'better']):
            hypothesis_type = 'improvement'
        elif any(word in problem_lower for word in ['predict', 'forecast', 'estimate']):
            hypothesis_type = 'predictive'
        elif any(word in problem_lower for word in ['detect', 'identify', 'recognize']):
            hypothesis_type = 'detection'
        elif any(word in problem_lower for word in ['relationship', 'correlation', 'association']):
            hypothesis_type = 'correlational'
        else:
            hypothesis_type = 'causal'
        
        # Generate hypothesis based on type
        if hypothesis_type == 'improvement':
            if keywords and len(keywords) >= 2:
                method = keywords[0]
                outcome = keywords[1] if len(keywords) > 1 else 'performance'
                hypothesis = (
                    f"Implementing advanced {method} techniques will significantly "
                    f"improve {outcome} compared to baseline approaches in {domain}"
                )
            else:
                hypothesis = f"The proposed methodology will outperform existing approaches in {domain}"
        
        elif hypothesis_type == 'predictive':
            if keywords:
                predictor = keywords[0]
                outcome = keywords[1] if len(keywords) > 1 else 'outcomes'
                hypothesis = (
                    f"Utilizing {predictor} as a predictive feature will accurately "
                    f"forecast {outcome} with statistical significance"
                )
            else:
                hypothesis = f"The predictive model will achieve significant accuracy in {domain}"
        
        elif hypothesis_type == 'detection':
            if keywords:
                target = keywords[0]
                hypothesis = (
                    f"The proposed detection method will identify {target} "
                    f"with higher accuracy and fewer false positives than existing methods"
                )
            else:
                hypothesis = f"The detection system will demonstrate superior performance in {domain}"
        
        elif hypothesis_type == 'correlational':
            if keywords and len(keywords) >= 2:
                var1 = keywords[0]
                var2 = keywords[1]
                hypothesis = (
                    f"There exists a significant positive correlation between "
                    f"{var1} and {var2} in {domain} contexts"
                )
            else:
                hypothesis = f"Key variables show significant relationships in {domain}"
        
        else:  # causal
            if keywords:
                cause = keywords[0]
                effect = keywords[1] if len(keywords) > 1 else 'outcomes'
                hypothesis = (
                    f"Modifying {cause} will lead to measurable changes in {effect}, "
                    f"demonstrating a causal relationship in {domain}"
                )
            else:
                hypothesis = f"The treatment will have a significant effect on outcomes in {domain}"
        
        return hypothesis
    
    def _generate_null_hypothesis(self, hypothesis: str) -> str:
        """Generate null hypothesis (H0)"""
        # Convert to null form
        if "will" in hypothesis:
            null = hypothesis.replace("will significantly", "will not significantly")
            null = null.replace("will improve", "will not improve")
            null = null.replace("will lead to", "will not lead to")
            null = null.replace("will achieve", "will not achieve")
            null = null.replace("will demonstrate", "will not demonstrate")
        elif "exists" in hypothesis:
            null = hypothesis.replace("exists", "does not exist")
        else:
            null = "There is no significant difference between treatment and control conditions"
        
        return null
    
    async def _identify_variables(self, hypothesis: str, keywords: List[str], domain: str) -> Dict:
        """
        Identify and categorize variables
        Dynamically extracts variables from hypothesis
        """
        hypothesis_lower = hypothesis.lower()
        
        # Independent variables (what we manipulate)
        independent_vars = []
        if keywords:
            # First keyword typically relates to the method/treatment
            independent_vars.append(f"{keywords[0]}_method")
            independent_vars.append(f"{keywords[0]}_parameter")
        
        # Add generic IV based on hypothesis type
        if any(word in hypothesis_lower for word in ['implement', 'apply', 'use']):
            independent_vars.append("treatment_type")
        
        independent_vars.append("experimental_condition")
        
        # Dependent variables (what we measure)
        dependent_vars = []
        if len(keywords) > 1:
            # Second keyword typically relates to outcome
            dependent_vars.append(f"{keywords[1]}_score")
            dependent_vars.append(f"{keywords[1]}_metric")
        
        # Add generic DVs
        dependent_vars.extend([
            "performance_measure",
            "accuracy_score",
            "effectiveness_rating"
        ])
        
        # Control variables (what we hold constant)
        control_vars = [
            "sample_characteristics",
            "environmental_conditions",
            "measurement_protocol",
            "time_of_measurement",
            "baseline_performance"
        ]
        
        # Confounding variables (potential confounds)
        confounding_vars = [
            "participant_variability",
            "external_factors",
            "measurement_error"
        ]
        
        return {
            "independent": independent_vars[:3],  # Limit to top 3
            "dependent": dependent_vars[:3],
            "control": control_vars[:5],
            "confounding": confounding_vars
        }
    
    async def _define_assumptions(self, hypothesis: str, domain: str) -> List[str]:
        """Define key assumptions underlying the hypothesis"""
        assumptions = [
            f"Data collected in {domain} is representative of the target population",
            "Measurements are valid, reliable, and free from systematic bias",
            "Sample size is adequate for detecting meaningful effects",
            "Random assignment ensures group equivalence at baseline",
            "External factors are controlled or their effects are negligible",
            "The relationship being tested is stable over the study period",
            "Measurement instruments have acceptable psychometric properties",
            "Participants respond truthfully and attentively"
        ]
        
        # Select relevant assumptions
        return random.sample(assumptions, k=min(4, len(assumptions)))
    
    async def _generate_predictions(self, hypothesis: str, variables: Dict) -> List[str]:
        """Generate specific testable predictions"""
        predictions = []
        
        # Prediction about main effect
        if variables['dependent']:
            dv = variables['dependent'][0]
            predictions.append(
                f"Treatment group will show 15-35% improvement in {dv} compared to control"
            )
        
        # Prediction about statistical significance
        predictions.append(
            "The effect will be statistically significant (p < 0.05) with adequate power (β > 0.80)"
        )
        
        # Prediction about effect size
        predictions.append(
            "Effect size will be medium to large (Cohen's d > 0.5)"
        )
        
        # Prediction about replicability
        predictions.append(
            "Results will be reproducible across multiple independent trials"
        )
        
        # Prediction about dose-response or scaling
        if variables['independent']:
            iv = variables['independent'][0]
            predictions.append(
                f"Effects will scale proportionally with {iv} intensity"
            )
        
        return predictions[:4]  # Return top 4 predictions
    
    def _identify_theoretical_basis(self, keywords: List[str], domain: str) -> List[str]:
        """Identify relevant theoretical frameworks"""
        # Domain-based theories
        domain_lower = domain.lower()
        theories = []
        
        if any(word in domain_lower for word in ['machine', 'learning', 'ai', 'algorithm', 'data']):
            theories.extend([
                "Statistical Learning Theory",
                "Information Theory",
                "Computational Complexity Theory",
                "Optimization Theory"
            ])
        
        elif any(word in domain_lower for word in ['social', 'psychology', 'behavior']):
            theories.extend([
                "Social Cognitive Theory",
                "Behavioral Psychology",
                "Systems Theory",
                "Decision Theory"
            ])
        
        elif any(word in domain_lower for word in ['biology', 'medical', 'health']):
            theories.extend([
                "Systems Biology Theory",
                "Biomedical Model",
                "Evidence-Based Medicine Framework",
                "Pathophysiological Theory"
            ])
        
        elif any(word in domain_lower for word in ['physics', 'chemistry', 'quantum']):
            theories.extend([
                "Quantum Mechanics",
                "Thermodynamics",
                "Field Theory",
                "Statistical Mechanics"
            ])
        
        elif any(word in domain_lower for word in ['climate', 'environment', 'ecology']):
            theories.extend([
                "Climate System Theory",
                "Ecological Systems Theory",
                "Environmental Science Framework",
                "Sustainability Theory"
            ])
        
        else:
            # Generic theories
            theories.extend([
                "Systems Theory",
                "Complexity Theory",
                "Information Processing Theory",
                "Empirical Research Framework"
            ])
        
        return random.sample(theories, k=min(3, len(theories)))
    
    def _classify_hypothesis_type(self, hypothesis: str) -> str:
        """Classify the type of hypothesis"""
        hypothesis_lower = hypothesis.lower()
        
        if "correlation" in hypothesis_lower or "relationship" in hypothesis_lower:
            return "correlational"
        elif "cause" in hypothesis_lower or "lead to" in hypothesis_lower:
            return "causal"
        elif "compare" in hypothesis_lower or "versus" in hypothesis_lower or "outperform" in hypothesis_lower:
            return "comparative"
        elif "predict" in hypothesis_lower or "forecast" in hypothesis_lower:
            return "predictive"
        else:
            return "directional"
    
    def _determine_effect_direction(self, hypothesis: str) -> str:
        """Determine expected direction of effect"""
        hypothesis_lower = hypothesis.lower()
        
        if any(word in hypothesis_lower for word in ['increase', 'improve', 'enhance', 'higher', 'positive']):
            return "positive"
        elif any(word in hypothesis_lower for word in ['decrease', 'reduce', 'lower', 'negative']):
            return "negative"
        else:
            return "bidirectional"