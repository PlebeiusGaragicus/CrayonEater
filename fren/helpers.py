import os

import logging
logger = logging.getLogger()

from pathlib import Path
HERE = Path(__file__).parent




OpenAIClient = None
# https://platform.openai.com/docs/guides/text-to-speech
OpenAIVoices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']

# Environment Check Function
def assert_env():
    if os.getenv("OPENAI_API_KEY", None) is None or \
        os.getenv("ASSEMBLYAI_API_KEY", None) is None or \
            os.getenv("BASE_API_URL", None) is None or \
                os.getenv("FLOW_ID", None) is None:
        logger.error("ENV vars not set in .env")
        exit(1)
