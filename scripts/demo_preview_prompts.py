"""
Small demo showing how to load the essay prompts and see exactly what would be
sent to an LLM API, using a very short sample essay.

This script does NOT call any external API. It only prints:
- a chat-style message list (for OpenAI / LLaMA-style clients)
- a single text prompt (for Gemini-style clients)
"""

from __future__ import annotations

from textwrap import indent
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ai_detection_benchmark.prompts import get_prompt, list_prompts  # noqa: E402


SAMPLE_ESSAY = (
    "I think using phones in class can be helpful, because students can search "
    "information fast, but sometimes it makes them distracted and they do not "
    "listen the teacher."
)


def preview_prompt(prompt_id: str) -> None:
    tmpl = get_prompt(prompt_id)
    print("=" * 80)
    print(f"Prompt ID : {tmpl.id}")
    print(f"Version   : {tmpl.prompt_version}")
    print(f"Task type : {tmpl.task_type}")
    print(f"Aspects   : {', '.join(tmpl.aspects)}")
    print("-" * 80)

    # Chat-style messages (e.g. for OpenAI / LLaMA chat APIs)
    messages = tmpl.build_chat_messages(essay_text=SAMPLE_ESSAY)
    print("Chat-style messages:\n")
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        print(f"[{role}]")
        print(indent(content, "  "))
        print()

    # Single text prompt (e.g. for Gemini-style APIs)
    full_text = tmpl.build_text_prompt(essay_text=SAMPLE_ESSAY)
    print("-" * 80)
    print("Single-string prompt (Gemini-style):\n")
    print(indent(full_text, "  "))
    print()


if __name__ == "__main__":
    # Preview all prompts defined in ai_influence_v1.yaml
    for tmpl in list_prompts():
        preview_prompt(tmpl.id)
