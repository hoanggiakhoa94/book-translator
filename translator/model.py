import logging

from google.generativeai import GenerativeModel
import google.generativeai as genai

from config import settings
from config.models import ModelConfig, get_retry_model_configs


class ModelManager:
    """Handles model initialization and selection."""

    def __init__(self, model_config: ModelConfig):
        self.primary_model = self._initialize_model(model_config)
        self.primary_batch_size = model_config.BATCH_SIZE

        lightweight_retry_config, full_retry_config = get_retry_model_configs(model_config.MODEL_NAME)

        self.lite_model, self.lite_batch_size = self._initialize_model_with_fallback(
            model_config=lightweight_retry_config,
            fallback_config=model_config,
            fallback_reason="lightweight retry",
        )
        self.pro_model, self.pro_batch_size = self._initialize_model_with_fallback(
            model_config=full_retry_config,
            fallback_config=model_config,
            fallback_reason="high-quality retry",
        )

    def _initialize_model(self, model_config: ModelConfig) -> GenerativeModel:
        """Initialize a Gemini model with the given configuration."""
        if not model_config.MODEL_NAME:
            raise ValueError("Model name must be provided")

        genai.configure(api_key=settings.get_api_key())
        model = genai.GenerativeModel(
            model_name=model_config.MODEL_NAME,
            generation_config=model_config.GENERATION_CONFIG,
            safety_settings=model_config.SAFETY_SETTINGS,
        )
        logging.info("Successfully initialized model: %s", model_config.MODEL_NAME)
        return model

    def _initialize_model_with_fallback(
        self,
        model_config: ModelConfig,
        fallback_config: ModelConfig,
        fallback_reason: str,
    ) -> tuple[GenerativeModel, int]:
        """Initialize model and fallback to primary config when model is unavailable."""
        try:
            return self._initialize_model(model_config), model_config.BATCH_SIZE
        except Exception as exc:
            logging.warning(
                "Could not initialize %s model '%s' (%s). Falling back to primary model '%s'.",
                fallback_reason,
                model_config.MODEL_NAME,
                exc,
                fallback_config.MODEL_NAME,
            )
            return self.primary_model, fallback_config.BATCH_SIZE

    def select_model_for_task(self, is_retry: bool) -> GenerativeModel:
        """Select the appropriate model based on whether this is a retry."""
        return self.pro_model if is_retry else self.primary_model
