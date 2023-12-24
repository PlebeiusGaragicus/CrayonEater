import os
import datetime

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
                os.getenv("FLOW_DEMO", None) is None: # TODO this is hardcoded and should not be
        logger.error("ENV vars not set in .env")
        exit(1)


def get_resource(name):
    return HERE.parent / "resources" / name


def get_path(dir, filename) -> str:
    return str(HERE.parent / dir / filename)


def get_timestamp():
    # return datetime.datetime.now().replace(microsecond=0).isoformat()
    return datetime.datetime.now().replace(microsecond=0).isoformat().replace(":", "-")

# set timezone to Los Angeles
# os.environ['TZ'] = 'America/Los_Angeles'