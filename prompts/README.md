# Prompt Templates

This folder centralises all prompt templates used for generating AI-influenced essay variants.

- `ai_influence_v1.yaml`  
  - Source of truth for prompts.  
  - Each entry has: `id`, `prompt_version`, `task_type`, `variant`, `level`, `aspects`, `placeholders`, `system`, `user`, `output_format`.  
  - Placeholders (currently `essay_text`) must match the `{...}` tokens in the text.

- `essay_prompts_v1.py`  
  - Loader and helper utilities.  
  - Validates placeholders on load and when formatting.  
  - Main methods: `get_prompt(id)`, `list_prompts()`, `build_chat_messages(...)`, `build_text_prompt(...)`.

- `demo_preview_prompts.py`  
  - Small demo that fills a short sample essay into each prompt and prints:  
    - Chat-style messages (for OpenAI / LLaMA-style clients).  
    - Single-string prompts (for Gemini-style APIs).  
  - Run from repo root: `python prompts/demo_preview_prompts.py`.

