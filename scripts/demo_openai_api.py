"""
Minimal OpenAI demo using the prompt templates.

Requires:
  export OPENAI_API_KEY="..."
  pip install openai
"""

from pathlib import Path
import sys

from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ai_detection_benchmark.prompts import get_prompt  # noqa: E402


MODEL = "gpt-5-nano"

# Pick one of the PROMPT_IDs below to test.
PROMPT_ID = "v1.ai_refined_grammar"

# Short synthetic essays to quickly inspect prompt behavior.
SAMPLE_ESSAYS = {
    "grammar_1": (
        "I think phones in class can be helpful because students can search fast, "
        "but sometimes it make them distracted and they not listen the teacher."
    ),
    "grammar_2": (
        "My friend say school start too early, and it make us tired in the morning. "
        "I agree because students is not focus when they sleepy."
    ),
    "vocab_1": (
        "The movie was good and the actors were good. The story was good too, "
        "but the ending was good only in some parts."
    ),
    "vocab_2": (
        "I think this plan is nice because it is nice for students and nice for teachers. "
        "It is a nice way to do the project."
    ),
    "cohesion_1": (
        "I like team sports. You can learn to cooperate. People can make friends. "
        "It keeps you healthy."
    ),
    "cohesion_2": (
        "Schools should teach coding. It helps with problem solving. "
        "Jobs need these skills. Students feel more confident."
    ),
    "syntax_1": (
        "In my opinion the rule should be changed because many students have jobs "
        "after school and they need time to rest and do homework which makes it hard."
    ),
    "syntax_2": (
        "Some students learn faster. Others need more time. It can be helpful, "
        "but it can also be confusing for them."
    ),
    "full_rewrite_1": (
        "I agree that students should read every day because reading helps you "
        "learn new words and you can understand different ideas."
    ),
    "full_rewrite_2": (
        "I disagree with wearing uniforms at school. They are uncomfortable and "
        "students want to show their style."
    ),
}


def main() -> None:
    client = OpenAI()
    tmpl = get_prompt(PROMPT_ID)
    sample_key = "grammar_1"
    messages = tmpl.build_chat_messages(essay_text=SAMPLE_ESSAYS[sample_key])

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    print(f"Prompt ID: {PROMPT_ID}")
    print(f"Sample: {sample_key}")
    print()
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
