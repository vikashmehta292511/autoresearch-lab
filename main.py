"""
AutoResearch Lab - CLI Version
Generates research papers with all agents + web scraping
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import logging

from agents.problem_finder import ProblemFinderAgent
from agents.hypothesis_generator import HypothesisAgent
from agents.experiment_designer import ExperimentDesignerAgent
from agents.data_analyst import DataAnalysisAgent
from agents.paper_writer import PaperWriterAgent
from utils.memory_store import MemoryStore
from utils.logger import setup_logger


class AutoResearchLab:
    """CLI-based autonomous research system"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.logger = setup_logger("AutoResearchLab", self.output_dir / "system.log")
        
        # Initialize memory
        self.memory = MemoryStore()
        
        # Initialize agents
        self.logger.info("Initializing agents...")
        self.problem_finder = ProblemFinderAgent(self.memory)
        self.hypothesis_agent = HypothesisAgent(self.memory)
        self.experiment_designer = ExperimentDesignerAgent(self.memory)
        self.data_analyst = DataAnalysisAgent(self.memory)
        self.paper_writer = PaperWriterAgent(self.memory)
        
        self.logger.info("✓ All agents initialized")
    
    async def run_research_pipeline(self, research_domain: str) -> dict:
        """
        Execute full research pipeline with all agents
        
        Args:
            research_domain: Research topic
            
        Returns:
            Complete research output
        """
        print(f"\n{'='*80}")
        print(f"AutoResearch Lab - Research Pipeline")
        print('='*80)
        print(f"Domain: {research_domain}\n")
        
        try:
            # Phase 1: Problem Identification (with web scraping)
            print("[1/5]  Identifying research problem (web scraping)...")
            problem_output = await self.problem_finder.identify_problem(research_domain)
            self.memory.store("research_problem", problem_output)
            print(f"✓ Problem: {problem_output['problem_statement'][:80]}...")
            
            # Phase 2: Hypothesis Generation
            print("\n[2/5]  Generating hypothesis...")
            hypothesis_output = await self.hypothesis_agent.generate_hypothesis(problem_output)
            self.memory.store("hypothesis", hypothesis_output)
            print(f"✓ Hypothesis: {hypothesis_output['hypothesis'][:80]}...")
            
            # Phase 3: Experiment Design
            print("\n[3/5]  Designing experiment...")
            experiment_output = await self.experiment_designer.design_experiment(hypothesis_output)
            self.memory.store("experiment_design", experiment_output)
            print(f"✓ Design: {experiment_output['experiment_type']}")
            
            # Phase 4: Data Analysis (simulated)
            print("\n[4/5]  Performing analysis...")
            analysis_output = await self.data_analyst.analyze_experiment(experiment_output)
            self.memory.store("analysis", analysis_output)
            print(f"✓ Analysis complete")
            
            # Phase 5: Paper Writing (Gemini 3000 words)
            print("\n[5/5]  Writing research paper (2500-3000 words with Gemini)...")
            paper_output = await self.paper_writer.write_paper(self.memory.get_all())
            self.memory.store("paper", paper_output)
            print(f"✓ Paper generated: {paper_output['word_count']} words")
            
            # Compile results
            final_output = self._compile_results()
            
            # Save to files
            await self._save_outputs(final_output)
            
            print(f"\n{'='*80}")
            print("✓ RESEARCH PIPELINE COMPLETED SUCCESSFULLY!")
            print('='*80)
            
            return final_output
            
        except Exception as e:
            self.logger.error(f"Pipeline error: {str(e)}", exc_info=True)
            print(f"\n Error: {str(e)}")
            print("Check output/system.log for details")
            raise
    
    def _compile_results(self) -> dict:
        """Compile all results"""
        all_data = self.memory.get_all()
        return {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "pipeline_version": "3.0-cli"
            },
            "research_problem": all_data.get("research_problem"),
            "hypothesis": all_data.get("hypothesis"),
            "experiment_design": all_data.get("experiment_design"),
            "analysis": all_data.get("analysis"),
            "paper": all_data.get("paper")
        }
    
    async def _save_outputs(self, final_output: dict):
        """Save outputs to repository"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = self.output_dir / f"research_{timestamp}"
        run_dir.mkdir(exist_ok=True)
        
        print(f"\n Saving outputs to: {run_dir}")
        
        # Save research paper
        paper_path = run_dir / "research_paper.md"
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(final_output['paper']['content'])
        print(f"✓ Paper saved: {paper_path}")
        
        # Save metadata
        metadata = {
            "timestamp": timestamp,
            "domain": final_output['research_problem']['domain'],
            "problem": final_output['research_problem']['problem_statement'],
            "hypothesis": final_output['hypothesis']['hypothesis'],
            "word_count": final_output['paper']['word_count'],
            "ai_model": final_output['paper'].get('ai_model', 'gemini-1.5-flash'),
            "papers_found": final_output['research_problem'].get('papers_found', 0)
        }
        metadata_path = run_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Metadata saved: {metadata_path}")
        
        # Save pipeline history
        history_path = run_dir / "pipeline_history.json"
        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump(final_output, f, indent=2, default=str)
        print(f"✓ Pipeline history saved: {history_path}")
        
        print(f"\n✓ All outputs saved to: {run_dir}")


async def main():
    """Main entry point"""
    print("="*80)
    print("AutoResearch Lab - Autonomous Research Generation")
    print("Powered by Gemini AI + Web Scraping")
    print("="*80)
    print()
    
    # Get research domain
    research_domain = input("Enter research domain: ").strip()
    
    if not research_domain:
        research_domain = "artificial intelligence"
        print(f"Using default: {research_domain}")
    
    # Initialize system
    lab = AutoResearchLab(output_dir="output")
    
    # Run pipeline
    try:
        result = await lab.run_research_pipeline(research_domain)
        
        print(f"\n Research Paper Summary:")
        print(f"   Title: {result['paper']['title']}")
        print(f"   Words: {result['paper']['word_count']}")
        print(f"   Papers Scraped: {result['research_problem'].get('papers_found', 0)}")
        print(f"   AI Model: {result['paper'].get('ai_model', 'gemini-1.5-flash')}")
        print(f"\n✓ Check output/ folder for complete results!")
        
    except Exception as e:
        print(f"\n Pipeline failed: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)