"""
Loader utilities for essay prompt templates.

The actual prompt texts live in YAML (`ai_influence_v1.yaml`) so they are easy
to read, edit, and version. This module simply loads them and exposes small
helper functions for use in notebooks / scripts.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping

import re

import yaml


PROMPT_FILE = Path(__file__).resolve().parents[2] / "prompts" / "ai_influence_v1.yaml"


@dataclass(frozen=True)
class PromptTemplate:
    id: str
    prompt_version: int
    task_type: str
    variant: str
    level: str
    description: str
    system: str
    user: str
    output_format: str
    aspects: List[str]
    placeholders: List[str]

    def _all_template_placeholders(self) -> List[str]:
        """Return all `{name}` placeholders used across system/user/output_format."""
        pattern = re.compile(r"{([a-zA-Z0-9_]+)}")
        text = f"{self.system}\n{self.user}\n{self.output_format}"
        return pattern.findall(text)

    def _validate_template_placeholders(self) -> None:
        """
        Validate that the declared `placeholders` list matches the placeholders
        actually used in the template strings.
        """
        declared = set(self.placeholders)
        found = set(self._all_template_placeholders())
        if declared != found:
            raise ValueError(
                f"Placeholder mismatch for prompt '{self.id}': "
                f"declared={sorted(declared)} found={sorted(found)}"
            )

    def _validate_call_placeholders(self, values: Mapping[str, object]) -> None:
        """
        Validate that all required placeholders have been supplied when
        formatting the template.
        """
        missing = [name for name in self.placeholders if name not in values]
        if missing:
            raise ValueError(
                f"Missing values for placeholders {missing} when using prompt '{self.id}'"
            )

    def format_user(self, **values: object) -> str:
        """
        Format the user instruction text, checking that all placeholders are
        provided and there are no unresolved template variables.
        """
        self._validate_call_placeholders(values)
        try:
            return self.user.format(**values)
        except KeyError as exc:
            raise ValueError(
                f"Unfilled placeholder '{exc.args[0]}' in prompt '{self.id}'"
            ) from exc

    def build_text_prompt(self, **values: object) -> str:
        """
        Build a single string prompt (useful for Gemini-style APIs) that combines
        system, user, and output-format instructions.
        """
        user_text = self.format_user(**values).strip()
        parts = [self.system.strip(), user_text, self.output_format.strip()]
        return "\n\n".join(p for p in parts if p)

    def build_chat_messages(self, **values: object) -> List[Dict[str, str]]:
        """
        Build messages in a generic chat format:
        - one system message
        - one user message (user + output_format appended)
        """
        user_text = self.format_user(**values).strip()
        user_with_format = f"{user_text}\n\n{self.output_format.strip()}".strip()
        return [
            {"role": "system", "content": self.system.strip()},
            {"role": "user", "content": user_with_format},
        ]


def _load_prompts() -> Dict[str, PromptTemplate]:
    raw = yaml.safe_load(PROMPT_FILE.read_text(encoding="utf-8")) or []
    prompts: Dict[str, PromptTemplate] = {}
    for entry in raw:
        tmpl = PromptTemplate(
            id=entry["id"],
            prompt_version=int(entry.get("prompt_version", 1)),
            task_type=entry.get("task_type", ""),
            variant=entry["variant"],
            level=entry["level"],
            description=entry.get("description", ""),
            system=entry.get("system", ""),
            user=entry.get("user", ""),
            output_format=entry.get("output_format", ""),
            aspects=list(entry.get("aspects", [])),
            placeholders=list(entry.get("placeholders", [])),
        )
        tmpl._validate_template_placeholders()
        prompts[tmpl.id] = tmpl
    return prompts


_PROMPTS_BY_ID: Dict[str, PromptTemplate] = _load_prompts()


def list_prompts() -> List[PromptTemplate]:
    """Return all available prompt templates."""
    return list(_PROMPTS_BY_ID.values())


def get_prompt(prompt_id: str) -> PromptTemplate:
    """
    Retrieve a prompt template by its full ID (e.g. 'v1.ai_refined_light').

    Raises KeyError if the ID is unknown.
    """
    return _PROMPTS_BY_ID[prompt_id]
