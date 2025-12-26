"""
Generate synthetic variants from controlled demo essays using prompt templates.

Usage:
  export OPENAI_API_KEY="..."
  python scripts/generate_ai_variants.py \
      --model gpt-5-mini \
      --input data/controlled_demo_essays_10.csv \
      --output data/controlled_demo_essays_10_generated.csv
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List

from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ai_detection_benchmark.prompts import get_prompt, list_prompts  # noqa: E402


DEFAULT_MODEL = "gpt-5-mini"
DEFAULT_SLEEP_SECONDS = 0.0
INTENT_TO_PROMPT_ID = {
    "grammar": "v1.ai_refined_grammar",
    "vocabulary": "v1.ai_refined_vocabulary",
    "cohesion": "v1.ai_refined_cohesion",
    "syntax": "v1.ai_refined_syntax",
    "full_rewrite": "v1.ai_full_rewrite",
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _default_input_path() -> Path:
    return _repo_root() / "data" / "controlled_demo_essays_10.csv"


def _default_output_path() -> Path:
    return _repo_root() / "data" / "controlled_demo_essays_10_generated.csv"


def _select_prompt_ids(prompt_ids: List[str] | None) -> List[str]:
    if prompt_ids:
        return prompt_ids
    return [tmpl.id for tmpl in list_prompts()]


def _iter_rows(input_path: Path) -> Iterable[dict]:
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def _write_header(output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "source_text_id",
                "source_text",
                "prompt_id",
                "prompt_version",
                "variant",
                "level",
                "aspects",
                "model",
                "generated_text",
                "status",
                "error",
                "generated_at",
            ],
        )
        writer.writeheader()


def _append_row(output_path: Path, row: dict) -> None:
    with output_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writerow(row)


def generate(
    input_path: Path,
    output_path: Path,
    model: str,
    prompt_ids: List[str],
    sleep_seconds: float,
    dry_run: bool,
    intent_only: bool,
) -> None:
    client = OpenAI()
    _write_header(output_path)

    for row in _iter_rows(input_path):
        source_text_id = row.get("text_id", "")
        source_text = row.get("full_text", "")
        intent = (row.get("intent") or "").strip()

        if intent_only:
            if intent not in INTENT_TO_PROMPT_ID:
                raise ValueError(
                    f"Unknown or missing intent '{intent}' for text_id='{source_text_id}'"
                )
            prompt_id_list = [INTENT_TO_PROMPT_ID[intent]]
        else:
            prompt_id_list = prompt_ids

        for prompt_id in prompt_id_list:
            tmpl = get_prompt(prompt_id)
            messages = tmpl.build_chat_messages(essay_text=source_text)

            if dry_run:
                print(f"\n--- {prompt_id} / {source_text_id} ---")
                for msg in messages:
                    print(f"[{msg['role']}] {msg['content']}")
                continue

            status = "OK"
            error = ""
            generated_text = ""

            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                )
                generated_text = response.choices[0].message.content or ""
            except Exception as exc:
                status = "ERROR"
                error = str(exc)

            out_row = {
                "source_text_id": source_text_id,
                "source_text": source_text,
                "prompt_id": tmpl.id,
                "prompt_version": tmpl.prompt_version,
                "variant": tmpl.variant,
                "level": tmpl.level,
                "aspects": ",".join(tmpl.aspects),
                "model": model,
                "generated_text": generated_text,
                "status": status,
                "error": error,
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
            _append_row(output_path, out_row)

            if sleep_seconds > 0:
                time.sleep(sleep_seconds)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--input", type=Path, default=_default_input_path())
    parser.add_argument("--output", type=Path, default=_default_output_path())
    parser.add_argument(
        "--prompt-id",
        action="append",
        dest="prompt_ids",
        help="Prompt ID to run (repeatable). Defaults to all prompts.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=DEFAULT_SLEEP_SECONDS,
        help="Sleep between API calls (seconds).",
    )
    parser.add_argument(
        "--intent-only",
        action="store_true",
        help="Use each row's intent to select exactly one prompt per essay.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print prompts only; do not call the API.",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    prompt_ids = _select_prompt_ids(args.prompt_ids)

    if args.output.exists():
        print(f"ERROR: output file exists: {args.output}", file=sys.stderr)
        print("Use a new output path or remove the existing file.", file=sys.stderr)
        return 2

    generate(
        input_path=args.input,
        output_path=args.output,
        model=args.model,
        prompt_ids=prompt_ids,
        sleep_seconds=args.sleep,
        dry_run=args.dry_run,
        intent_only=args.intent_only,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
