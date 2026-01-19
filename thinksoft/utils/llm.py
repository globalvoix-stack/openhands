import warnings

import httpx

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    import litellm

from thinksoft.core.config import LLMConfig, ThinksoftConfig
from thinksoft.core.logger import thinksoft_logger as logger
from thinksoft.llm import bedrock


def get_supported_llm_models(config: ThinksoftConfig) -> list[str]:
    """Get all models supported by LiteLLM.

    This function combines models from litellm and Bedrock, removing any
    error-prone Bedrock models.

    Returns:
        list[str]: A sorted list of unique model names.
    """
    litellm_model_list = litellm.model_list + list(litellm.model_cost.keys())
    litellm_model_list_without_bedrock = bedrock.remove_error_modelId(
        litellm_model_list
    )
    # TODO: for bedrock, this is using the default config
    llm_config: LLMConfig = config.get_llm_config()
    bedrock_model_list = []
    if (
        llm_config.aws_region_name
        and llm_config.aws_access_key_id
        and llm_config.aws_secret_access_key
    ):
        bedrock_model_list = bedrock.list_foundation_models(
            llm_config.aws_region_name,
            llm_config.aws_access_key_id.get_secret_value(),
            llm_config.aws_secret_access_key.get_secret_value(),
        )
    model_list = litellm_model_list_without_bedrock + bedrock_model_list
    for llm_config in config.llms.values():
        ollama_base_url = llm_config.ollama_base_url
        if llm_config.model.startswith('ollama'):
            if not ollama_base_url:
                ollama_base_url = llm_config.base_url
        if ollama_base_url:
            ollama_url = ollama_base_url.strip('/') + '/api/tags'
            try:
                ollama_models_list = httpx.get(ollama_url, timeout=3).json()['models']  # noqa: ASYNC100
                for model in ollama_models_list:
                    model_list.append('ollama/' + model['name'])
                break
            except httpx.HTTPError as e:
                logger.error(f'Error getting OLLAMA models: {e}')

    # Add Thinksoft provider models
    thinksoft_models = [
        'thinksoft/claude-sonnet-4-20250514',
        'thinksoft/claude-sonnet-4-5-20250929',
        'thinksoft/gpt-5-2025-08-07',
        'thinksoft/gpt-5-mini-2025-08-07',
        'thinksoft/claude-opus-4-20250514',
        'thinksoft/claude-opus-4-5-20251101',
        'thinksoft/gemini-2.5-pro',
        'thinksoft/o3',
        'thinksoft/o4-mini',
        'thinksoft/devstral-small-2505',
        'thinksoft/devstral-small-2507',
        'thinksoft/devstral-medium-2507',
        'thinksoft/kimi-k2-0711-preview',
        'thinksoft/qwen3-coder-480b',
    ]
    model_list = thinksoft_models + model_list

    # Add Clarifai provider models (via OpenAI-compatible endpoint)
    clarifai_models = [
        # clarifai featured models
        'clarifai/openai.chat-completion.gpt-oss-120b',
        'clarifai/openai.chat-completion.gpt-oss-20b',
        'clarifai/openai.chat-completion.gpt-5',
        'clarifai/openai.chat-completion.gpt-5-mini',
        'clarifai/qwen.qwen3.qwen3-next-80B-A3B-Thinking',
        'clarifai/qwen.qwenLM.Qwen3-30B-A3B-Instruct-2507',
        'clarifai/qwen.qwenLM.Qwen3-30B-A3B-Thinking-2507',
        'clarifai/qwen.qwenLM.Qwen3-14B',
        'clarifai/qwen.qwenCoder.Qwen3-Coder-30B-A3B-Instruct',
        'clarifai/deepseek-ai.deepseek-chat.DeepSeek-R1-0528-Qwen3-8B',
        'clarifai/deepseek-ai.deepseek-chat.DeepSeek-V3_1',
        'clarifai/zai.completion.GLM_4_5',
        'clarifai/moonshotai.kimi.Kimi-K2-Instruct',
    ]
    model_list = clarifai_models + model_list

    return sorted(set(model_list))
