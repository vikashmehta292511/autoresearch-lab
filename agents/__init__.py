"""
AutoResearch Lab - Agents Package
All specialized research agents
"""

from .problem_finder import ProblemFinderAgent
from .hypothesis_generator import HypothesisAgent
from .experiment_designer import ExperimentDesignerAgent
from .data_analyst import DataAnalysisAgent
from .paper_writer import PaperWriterAgent

__all__ = [
    
    'ProblemFinderAgent',
    'HypothesisAgent',
    'ExperimentDesignerAgent',
    'DataAnalysisAgent',
    'PaperWriterAgent'
]

__version__ = '1.0.0'