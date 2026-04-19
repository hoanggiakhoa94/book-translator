from typing import Optional

from config import prompts
from config.prompts import PromptStyle


class PromptBuilder:
    """Handles building translation prompts"""

    STYLE_REFINEMENT_GUIDELINES = """
**BỔ SUNG CHẤT VĂN:**
- Không dịch bám chữ từng từ. Ưu tiên giữ ý, nhịp và cảm xúc của câu.
- Tái cấu trúc câu linh hoạt theo văn phong tiếng Việt tự nhiên; tránh câu cứng hoặc lặp mô-típ.
- Giữ nhất quán giọng điệu nhân vật trong cùng ngữ cảnh, đặc biệt ở hội thoại dài.
- Chọn từ gợi hình, giàu sắc thái nhưng không phô trương; tránh sáo ngữ hoặc dịch máy.
- Duy trì mạch đọc trơn tru giữa các câu liên tiếp như một đoạn văn đã biên tập.
""".strip()

    @staticmethod
    def build_translation_prompt(
            text: str,
            additional_info: Optional[str],
            prompt_style: PromptStyle
    ) -> str:
        """Build prompt based on selected style."""
        base_prompt = {
            PromptStyle.Modern: prompts.MODERN_PROMPT,
            PromptStyle.ChinaFantasy: prompts.CHINA_FANTASY_PROMPT,
            PromptStyle.BookInfo: prompts.BOOK_INFO_PROMPT,
            PromptStyle.Sentences: prompts.SENTENCES_PROMPT,
            PromptStyle.IncompleteHandle: prompts.INCOMPLETE_HANDLE_PROMPT,
        }[PromptStyle(prompt_style)]

        if PromptStyle(prompt_style) in {
            PromptStyle.Modern,
            PromptStyle.ChinaFantasy,
            PromptStyle.IncompleteHandle,
        }:
            base_prompt = f"{base_prompt}\n\n{PromptBuilder.STYLE_REFINEMENT_GUIDELINES}"

        text = f"[**NỘI DUNG ĐOẠN VĂN**]\n{text.strip()}\n[**NỘI DUNG ĐOẠN VĂN**]"
        if additional_info:
            return f"{base_prompt}\n{text}\n{base_prompt}\n\n{additional_info}".strip()
        return f"{base_prompt}\n{text}\n{base_prompt}".strip()
