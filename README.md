#  AutoResearch Lab 

**Multi-Agent System for Autonomous Research Paper Generation**

This is my capstone project for the Kaggle 5‑Day AI Agents Intensive Course. It demonstrates how I applied agent workflows, tools, memory and evaluation to build a practical, real‑world AI agent.
It generates professional research papers on ANY topic using AI agents + web scraping.

[![Kaggle 5‑Day AI Agents Intensive](https://img.shields.io/badge/Kaggle-5%20Day%20AI%20Agents%20Intensive%20Course%20with%20Google%20orange.svg)](https://www.kaggle.com/learn-guide/5-day-agents)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Gemini API](https://img.shields.io/badge/AI-Google%20Gemini-green.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


---

##  Features

-  **5 Specialized Agents** working together
-  **Web Scraping** from arXiv for real papers
-  **2500-3000 Words** publication-ready papers
-  **Complete Pipeline** from problem → hypothesis → methodology → analysis → paper
-  **FREE** uses Google Gemini API key
-  **Saves to Repository** in `output/` folder

---

##  Architecture

```
User Input (Domain)
        ↓
[Problem Finder Agent] ← Scrapes arXiv papers
        ↓
[Hypothesis Generator Agent]
        ↓
[Experiment Designer Agent]
        ↓
[Data Analyst Agent]
        ↓
[Paper Writer Agent] ← Uses Gemini AI
        ↓
Output → research_paper.md
```

---

##  Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone repository**
```bash
git clone https://github.com/yourusername/autoresearch-lab.git
cd autoresearch-lab
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Get FREE Gemini API Key**
- Go to: https://makersuite.google.com/app/apikey
- Sign in with Google
- Create API key
- Copy the key

4. **Create .env file**
```bash
echo "GEMINI_API_KEY=your-key-here" > .env
```

5. **Run**
```bash
python main.py
```

6. **Enter domain**
```
Enter research domain: your research domain
```

---

##  Output Structure

```
output/research_20241201_143022/
├── research_paper.md          # paper
├── metadata.json             # Run information
└── pipeline_history.json     # Complete agent outputs
```

---

##  What Each Agent Does

### 1. Problem Finder Agent
- **Scrapes arXiv** for recent papers
- Analyzes 10 papers in the domain
- Identifies research gaps
- Extracts keywords

### 2. Hypothesis Generator Agent
- Creates testable hypothesis
- Identifies variables (IV, DV, CV)
- Defines null/alternative hypotheses
- Establishes research framework

### 3. Experiment Designer Agent
- Designs research methodology
- Specifies sample size
- Defines experimental procedure
- Outlines analysis plan

### 4. Data Analyst Agent
- Simulates statistical analysis
- Calculates p-values and effect sizes
- Interprets results
- Draws conclusions

### 5. Paper Writer Agent
- **Uses Gemini AI** for 3000-word generation
- Integrates all agent outputs
- Follows academic structure
- Includes 12-15 citations
- Professional formatting

---

##  Configuration

### Environment Variables

Create `.env` file:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

### Customize Paper Length

Edit `agents/paper_writer.py` :
```python
"Length: 3500-4000 words"  # Change as needed
```

### Customize Scraping

Edit `agents/problem_finder.py` :
```python
max_results=20  # Fetch more papers
```

---

##  Cost

**FREE!**

- Gemini 2.5 Flash: 
- arXiv API: FREE

**Usage limits:**
- Gemini: 60 requests/minute (free tier)
- arXiv: Unlimited

---

##  Performance

- **Generation Time**: 30-60 seconds
- **Word Count**: 2500-3000 words
- **Papers Scraped**: 5-10 per run
- **Citations**: 12-15 per paper

---

##  Project Structure

```
autoresearch-lab/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── .env                      # API keys
├── README.md                 # This file
│
├── agents/
│   ├── __init__.py
│   ├── problem_finder.py     # With arXiv scraping
│   ├── hypothesis_generator.py
│   ├── experiment_designer.py
│   ├── data_analyst.py
│   └── paper_writer.py       # Gemini 3000 words
│
├── utils/
│   ├── __init__.py
│   ├── memory_store.py       # Context management
│   └── logger.py             # Logging
│
└── output/                    # Generated papers
    └── research_YYYYMMDD_HHMMSS/
        ├── research_paper.md
        ├── metadata.json
        └── pipeline_history.json
```

---

##  Example Domains

You can try these domains:
- Quantum Machine Learning
- Climate Change Mitigation Strategies
- CRISPR Gene Editing Ethics
- Blockchain Scalability Solutions
- Deep Learning for Medical Diagnosis
- Renewable Energy Optimization
- Space Debris Management
- Cybersecurity in IoT Devices

---

##  Acknowledgments

- **Google Gemini** - AI generation
- **arXiv** - Research papers
- **Python community** - Libraries and tools

Built as the Capstone Project for the 5‑Day AI Agents Intensive Course with Google (Kaggle‑Mentors).
Thanks to the Kaggle community, mentors, and Google researchers for guidance and resources.

---

**Made for researchers and students worldwide**


*Generate professional research papers in 60 seconds, not weeks.*



