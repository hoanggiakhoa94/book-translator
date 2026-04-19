import json
import re
from typing import Optional, Tuple

from config import prompts
from config.prompts import PromptStyle


class PromptBuilder:
    """Builds translation prompts from templates."""

    @staticmethod
    def _extract_context(additional_info: Optional[str]) -> Tuple[str, str]:
        """Extract glossary and previous context from optional metadata text."""
        if not additional_info:
            return "", ""

        data = additional_info.strip()
        glossary = ""
        previous_context = ""

        glossary_match = re.search(r"\[GLOSSARY\](.*?)\[/GLOSSARY\]", data, re.DOTALL)
        context_match = re.search(r"\[PREVIOUS_CONTEXT\](.*?)\[/PREVIOUS_CONTEXT\]", data, re.DOTALL)

        if glossary_match or context_match:
            if glossary_match:
                glossary = glossary_match.group(1).strip()
            if context_match:
                previous_context = context_match.group(1).strip()
            return glossary, previous_context

        # Backward-compatible default: treat free-form info as glossary.
        return data, ""

    @staticmethod
    def _format_sentences_list(text: str) -> str:
        """Format sentence list payload for SENTENCES_PROMPT."""
        raw = text.strip()
        if not raw:
            return "[]"

        if raw.startswith("[") and raw.endswith("]"):
            return raw

        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        if not lines:
            return "[]"

        return json.dumps(lines, ensure_ascii=False, indent=2)

    @staticmethod
    def build_translation_prompt(
        text: str,
        additional_info: Optional[str],
        prompt_style: PromptStyle,
    ) -> str:
        """Build prompt based on selected style."""
        style = PromptStyle(prompt_style)
        template = {
            PromptStyle.Modern: prompts.MODERN_PROMPT,
            PromptStyle.ChinaFantasy: prompts.CHINA_FANTASY_PROMPT,
            PromptStyle.BookInfo: prompts.BOOK_INFO_PROMPT,
            PromptStyle.Sentences: prompts.SENTENCES_PROMPT,
            PromptStyle.IncompleteHandle: prompts.INCOMPLETE_HANDLE_PROMPT,
        }[style]

        source_text = text.strip()
        glossary, previous_context = PromptBuilder._extract_context(additional_info)
        sentences_list = PromptBuilder._format_sentences_list(source_text)

        result = template
        replacements = {
            "{source_text}": source_text,
            "{sentences_list}": sentences_list,
            "{glossary}": glossary,
            "{previous_context}": previous_context,
        }
        for token, value in replacements.items():
            result = result.replace(token, value)

        # If prompt template has no placeholders but caller still passes metadata,
        # keep backward compatibility by appending metadata to the end.
        if additional_info and "{glossary}" not in template and "{previous_context}" not in template:
            result = f"{result}\n\n{additional_info.strip()}"

        return result.strip()
