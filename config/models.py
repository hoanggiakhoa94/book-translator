from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

from google.generativeai.types import HarmCategory, HarmBlockThreshold
from PyQt5.QtCore import QSettings


DEFAULT_PRIMARY_MODEL = "gemini-2.5-flash"
DEFAULT_LIGHTWEIGHT_MODEL = "gemini-2.5-flash"
DEFAULT_RETRY_MODEL = "gemini-2.5-pro"
DEFAULT_BOOK_INFO_MODEL = "gemini-2.5-flash"

MODEL_ALIASES = {
    "gemini-2.0-flash-thinking": "gemini-2.0-flash-thinking-exp-01-21",
}

# Ordered list shown in UI. Keep modern models first while preserving legacy options.
SUPPORTED_MODELS: List[str] = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite-preview-06-17",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-thinking-exp-01-21",
    "gemini-1.5-pro",
]

MODEL_BATCH_SIZES = {
    "gemini-2.5-flash": 12,
    "gemini-2.5-pro": 3,
    "gemini-2.5-flash-lite-preview-06-17": 16,
    "gemini-2.0-flash": 12,
    "gemini-2.0-flash-lite": 15,
    "gemini-2.0-flash-thinking-exp-01-21": 8,
    "gemini-1.5-pro": 2,
}


def get_generation_config() -> Dict[str, Any]:
    """Get generation config from settings or return defaults."""
    settings = QSettings("NovelTranslator", "Config")
    temperature = settings.value("ModelTemperature", 0.20, type=float)
    top_p = settings.value("ModelTopP", 0.90, type=float)
    top_k = settings.value("ModelTopK", 40, type=int)
    sampling_customized = settings.value("ModelSamplingCustomized", False, type=bool)

    # Backward-compatible quality bump for older installs that still have legacy defaults.
    if not sampling_customized and temperature == 0.0 and top_p == 0.95 and top_k == 40:
        temperature = 0.20
        top_p = 0.90

    return {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }


SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}


@dataclass
class ModelConfig:
    MODEL_NAME: str
    BATCH_SIZE: int
    GENERATION_CONFIG: Dict[str, Any]
    SAFETY_SETTINGS: Dict[HarmCategory, HarmBlockThreshold]


def _resolve_model_name(model_name: str) -> str:
    normalized_name = (model_name or DEFAULT_PRIMARY_MODEL).strip()
    if not normalized_name:
        normalized_name = DEFAULT_PRIMARY_MODEL
    return MODEL_ALIASES.get(normalized_name, normalized_name)


def _infer_batch_size(model_name: str) -> int:
    lowered = model_name.lower()
    if "pro" in lowered:
        return 3
    if "lite" in lowered:
        return 15
    if "thinking" in lowered:
        return 8
    if "flash" in lowered:
        return 12
    return 8


def build_model_config(model_name: str, batch_size: int = None) -> ModelConfig:
    resolved_model = _resolve_model_name(model_name)
    resolved_batch_size = batch_size or MODEL_BATCH_SIZES.get(resolved_model, _infer_batch_size(resolved_model))
    return ModelConfig(
        MODEL_NAME=resolved_model,
        BATCH_SIZE=resolved_batch_size,
        GENERATION_CONFIG=get_generation_config(),
        SAFETY_SETTINGS=SAFETY_SETTINGS,
    )


def get_available_model_names() -> List[str]:
    """Return model names to display in UI controls."""
    return list(SUPPORTED_MODELS)


def get_model_config(model_name: str) -> ModelConfig:
    """Get model configuration for the specified model with current settings."""
    return build_model_config(model_name)


def get_lightweight_model_config() -> ModelConfig:
    """Get model config used for high-volume translation subtasks."""
    return get_model_config(DEFAULT_LIGHTWEIGHT_MODEL)


def get_book_info_model_config() -> ModelConfig:
    """Get model config used for downloader metadata translation."""
    return get_model_config(DEFAULT_BOOK_INFO_MODEL)


def get_retry_model_configs(primary_model_name: str) -> Tuple[ModelConfig, ModelConfig]:
    """Return (lightweight_retry_model, high_quality_retry_model) configs."""
    primary = _resolve_model_name(primary_model_name)

    lightweight_retry_name = DEFAULT_LIGHTWEIGHT_MODEL
    if primary == lightweight_retry_name:
        lightweight_retry_name = primary

    full_retry_name = DEFAULT_RETRY_MODEL
    if primary == full_retry_name:
        full_retry_name = primary

    return (
        get_model_config(lightweight_retry_name),
        get_model_config(full_retry_name),
    )
