import os
import sys

from google import genai


def get_dynamic_model(logger):
    """
    Retrieves the model ID. Performs interactive selection only for Gemini
    if no model is specified.
    """
    env_model = os.getenv("MODEL_NAME")
    provider = os.getenv("active_provider", "gemini").lower()

    if env_model and env_model.strip():
        return env_model

    if provider == "ollama":
        return "phi3.5"

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY missing in environment.")
            sys.exit(1)
        return "gpt-4o-mini"

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY missing for interactive selection.")
            sys.exit(1)

        logger.warning("MODEL_NAME undefined. Initializing Gemini model discovery.")

        try:
            client = genai.Client(api_key=api_key)
            available_models = []

            for m in client.models.list():
                m_name = getattr(m, "name", str(m))

                if "gemini" in m_name.lower():
                    available_models.append(m_name)

            if not available_models:
                available_models = [
                    "models/gemini-1.5-flash",
                    "models/gemini-1.5-flash-lite",
                ]

            print("\n[AI Model Selection Menu]")
            for idx, model in enumerate(available_models):
                print(f"  ({idx}) {model}")

            user_input = input("\nSelect model index [Default 0]: ").strip()
            idx = (
                int(user_input)
                if user_input.isdigit() and int(user_input) < len(available_models)
                else 0
            )

            selection = available_models[idx]
            if not selection.startswith("models/"):
                selection = f"models/{selection}"

            logger.info(f"Model confirmed: {selection}")
            return selection

        except Exception as e:
            logger.error(f"Failed to retrieve Gemini models: {e}")
            return "models/gemini-1.5-flash-lite"


def get_llm_config(model_name):
    """
    Constructs the provider-specific LLM configuration.
    """
    provider = os.getenv("active_provider", "gemini").lower()
    config = {
        "model": model_name,
        "cache_seed": None,
        "max_retries": 5,
        "retry_wait": 30,
    }

    if provider == "gemini":
        config.update({"api_key": os.getenv("GEMINI_API_KEY"), "api_type": "google"})
    elif provider == "ollama":
        config.update(
            {
                "base_url": "http://localhost:11434/v1",
                "api_key": "ollama",
            }
        )
    elif provider == "openai":
        config.update({"api_key": os.getenv("OPENAI_API_KEY")})

    return {"config_list": [config], "cache_seed": None}
