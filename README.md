# Detecting AI Influence in Student Writing

This repository supports a research project on **detecting varying levels of AI involvement in student writing**, ranging from fully human-written texts to lightly AI-edited and fully AI-generated versions.

The goal is to move beyond binary *AI vs human* detection and instead study **how detection systems behave across realistic educational edge cases**, with an emphasis on **reliability, interpretability, and fairness**.

---

## Project Overview

Large Language Models (LLMs) are increasingly used in student writing for editing, rewriting, and content generation. This raises challenges related to authorship, academic integrity, and equitable assessment.

This project investigates:
- How detection tools respond to **different degrees of AI influence**
- Whether lightly AI-edited student writing is disproportionately flagged
- How well detectors generalize across **LLMs and writing topics**
- What kinds of errors matter most in educational settings

---

## Repository Structure (Minimal)

- `data/` — local copies of the student essay data and derived JSONL structures (`train.csv`, `ell_essay_families_structure_V2.jsonl`)  
- `notebooks/` — exploratory and generation notebooks (`Essay_JSON*.ipynb`)  
- `prompts/` — centralised, versioned prompt templates used for LLM-based generation (see `prompts/README.md`)  
- `docs/` — project materials such as the NORA poster  
- `Gemini API/` — auxiliary scripts and configuration for running Gemini-based generation (kept as-is)

---

## Dataset Design

Each student-written paragraph is versioned into three controlled variants:

1. **Original** — authentic, unaltered student text  
2. **AI-Refined** — light grammar and style edits, meaning preserved  
3. **Fully AI-Written** — same meaning, rewritten by an LLM  

This structure is designed to reflect **real classroom usage**, not synthetic or extreme cases.

---

## LLMs Used for Text Generation

Planned / ongoing generation using multiple model families:
- OpenAI (GPT series)
- Google Gemini
- Meta LLaMA
- Other open-source LLMs

Generation is **prompt-controlled** to ensure:
- Meaning preservation
- Comparable intervention strength
- Separation between editing and full generation
Prompt templates for each aspect (grammar, vocabulary, cohesion, syntax, and full rewrite) are versioned in `prompts/ai_influence_v1.yaml`.

---

## Detection Tools Evaluated

The project benchmarks detection systems with different design philosophies:

- **Proprietary detectors** (e.g., GPTZero)
- **Open-source classifiers** (e.g., RoBERTa-based models)

Evaluation focuses not only on accuracy, but also on:
- False positives on authentic student writing
- Sensitivity to fluency and grammatical improvement
- Agreement and disagreement across tools

---

## Project Progress

### Phase 1 — Dataset Construction
- [x] Collect authentic student-written texts  
- [x] Define AI influence levels (original / edited / generated)  
- [ ] Expand topics and writing genres  

### Phase 2 — LLM-Based Generation
- [x] Design controlled prompts  
- [ ] Generate variants using multiple LLMs  
- [ ] Validate meaning preservation  

### Phase 3 — Detection Benchmarking
- [x] Run proprietary detector evaluations  
- [x] Run open-source detector evaluations  
- [ ] Add additional detection models  
- [ ] Normalize detector outputs  

### Phase 4 — Analysis & Interpretability
- [x] Identify systematic false positives  
- [ ] Cross-LLM generalization analysis  
- [ ] Error typology by influence level  
- [ ] Educational interpretability analysis  

### Phase 5 — Release & Reporting
- [ ] Reproducible evaluation scripts  
- [ ] Paper / extended study  
- [ ] Public benchmark release  

---

## Why This Matters

Current AI detection tools are often evaluated on **synthetic or extreme benchmarks**.  
This project instead focuses on **realistic educational scenarios**, where:
- Students may legitimately use AI for light editing
- Detection errors can have serious consequences
- Interpretability and fairness matter as much as raw performance

The aim is to support **more transparent and educationally aligned AI detection research**.

---

## Acknowledgments

to be added.

---

## Data Sources and Availability

The original student essays used in this project come from the **Feedback Prize – English Language Learning** competition (`train.csv`) on Kaggle: https://www.kaggle.com/competitions/feedback-prize-english-language-learning.

Due to licensing and data-sharing constraints, **we cannot redistribute the original student texts**. This repository will instead provide **augmented and model-generated variants**, along with derived annotations and metadata where permitted.

---

## Citation

Citation information is **coming soon**.  
Once the corresponding paper or report is available, we will add a recommended citation here.

---

## Contributions

- Faruk Özgür  
- Ibrahim Riza Hallac

---

## Related Material

- Poster: *Detecting AI Influence in Student Writing* (NORA / AI4AfL) — [`docs/poster/NORA_2024_poster.pdf`](docs/poster/NORA_2024_poster.pdf)
