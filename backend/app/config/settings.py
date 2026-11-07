import os
import sys
from contextvars import ContextVar
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from loguru import logger
from autogen_ext.models.openai import OpenAIChatCompletionClient
from langsmith import traceable,get_current_run_tree

load_dotenv()

MODEL = os.getenv("model")
OPENROUTER_API_KEY = os.getenv("openrouter_api_key")
BASE_URL = os.getenv("base_url")

# OpenRouter pricing is model-dependent. Configure these values in USD per
# 1 million tokens for the exact model configured in the environment.
INPUT_PRICE_PER_1M = float(os.getenv("LLM_INPUT_PRICE_PER_1M_USD", "0.10"))
OUTPUT_PRICE_PER_1M = float(os.getenv("LLM_OUTPUT_PRICE_PER_1M_USD", "0.32"))

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = PROJECT_ROOT / "logs"
os.makedirs(LOG_DIR, exist_ok=True)


@dataclass
class LLMUsageCapture:
    """Aggregates usage reported by actual AutoGen model responses."""

    model: str = MODEL or "unknown"
    input_tokens: int = 0
    output_tokens: int = 0
    llm_call_count: int = 0
    usage_reported_call_count: int = 0
    input_cost_usd: float = 0.0
    output_cost_usd: float = 0.0
    source: str = "autogen_response_usage"
    _seen_results: set = field(default_factory=set, repr=False)

    def record_invocation(self) -> None:
        self.llm_call_count += 1

    def record(self, result: Any) -> None:
        usage = getattr(result, "usage", None)
        if usage is None:
            usage = getattr(result, "usage_metadata", None)

        if usage is None:
            return

        prompt_tokens = getattr(usage, "prompt_tokens", None)
        completion_tokens = getattr(usage, "completion_tokens", None)

        # Also support dict-shaped usage metadata.
        if isinstance(usage, dict):
            prompt_tokens = usage.get(
                "prompt_tokens", usage.get("input_tokens", prompt_tokens)
            )
            completion_tokens = usage.get(
                "completion_tokens", usage.get("output_tokens", completion_tokens)
            )

        if prompt_tokens is None or completion_tokens is None:
            return

        # A final streaming result should be counted once.
        identity = id(result)
        if identity in self._seen_results:
            return
        self._seen_results.add(identity)

        prompt_tokens = int(prompt_tokens or 0)
        completion_tokens = int(completion_tokens or 0)

        self.input_tokens += prompt_tokens
        self.output_tokens += completion_tokens
        self.usage_reported_call_count += 1

        self.input_cost_usd += (
            prompt_tokens * INPUT_PRICE_PER_1M / 1_000_000
        )
        self.output_cost_usd += (
            completion_tokens * OUTPUT_PRICE_PER_1M / 1_000_000
        )

        result_model = getattr(result, "model", None)
        if result_model:
            self.model = str(result_model)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def total_cost_usd(self) -> float:
        return self.input_cost_usd + self.output_cost_usd

    def as_dict(self) -> dict:
        return {
            "model": self.model,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "input_cost_usd": round(self.input_cost_usd, 15),
            "output_cost_usd": round(self.output_cost_usd, 15),
            "total_cost_usd": round(self.total_cost_usd, 15),
            "llm_call_count": self.llm_call_count,
            "usage_reported_call_count": self.usage_reported_call_count,
            "source": self.source,
        }


_ACTIVE_USAGE_CAPTURE: ContextVar[Optional[LLMUsageCapture]] = ContextVar(
    "active_llm_usage_capture", default=None
)


class UsageTrackedOpenAIChatCompletionClient(OpenAIChatCompletionClient):
    """AutoGen client that records usage from completed model responses."""

    """ @traceable(
        name="autogen_llm_call",
        run_type="llm"
    ) """
    @traceable(
        name="openrouter_autogen_llm",
        run_type="llm",
        metadata={
            "ls_provider": "openrouter",
            "ls_model_name": MODEL
        },
        process_inputs=lambda inputs: {"model": MODEL},
        process_outputs=lambda output: {"status": "completed"}
    )
    async def create(self, *args, **kwargs):
        capture = _ACTIVE_USAGE_CAPTURE.get()
        if capture is not None:
            capture.record_invocation()
        result = await super().create(*args, **kwargs)
        """ capture = _ACTIVE_USAGE_CAPTURE.get()
        if capture is not None:
            capture.record(result)
        return result """
        usage = getattr(result, "usage", None)

        if usage is not None:

            input_tokens = int(
                getattr(usage, "prompt_tokens", 0) or 0
            )

            output_tokens = int(
                getattr(usage, "completion_tokens", 0) or 0
            )

            total_tokens = input_tokens + output_tokens

            # Calculate costs using configured OpenRouter rates.
            input_cost = (
                input_tokens * INPUT_PRICE_PER_1M / 1_000_000
            )

            output_cost = (
                output_tokens * OUTPUT_PRICE_PER_1M / 1_000_000
            )

            total_cost = input_cost + output_cost

            # Attach actual invocation usage and calculated cost
            # to the current LangSmith LLM run.
            run_tree = get_current_run_tree()

            if run_tree is not None:
                run_tree.set(
                    usage_metadata={
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "total_tokens": total_tokens,
                        "input_cost": input_cost,
                        "output_cost": output_cost,
                        "total_cost": total_cost
                    }
                )

            # Preserve existing MLflow usage aggregation.
            if capture is not None:
                capture.record(result)

        return result

    async def create_stream(self, *args, **kwargs):
        capture = _ACTIVE_USAGE_CAPTURE.get()
        if capture is not None:
            capture.record_invocation()
        async for item in super().create_stream(*args, **kwargs):
            capture = _ACTIVE_USAGE_CAPTURE.get()
            if capture is not None:
                # AutoGen streaming yields text chunks and, at completion,
                # a CreateResult containing aggregate usage.
                capture.record(item)
            yield item


class Settings:
    log_dir: str = str(LOG_DIR)
    model: str = MODEL

    def get_logger(self, name: str = __name__):
        return logger.bind(module=name)

    @staticmethod
    def get_model_client():
        if not MODEL:
            raise ValueError("Environment variable 'model' is not configured.")
        if not OPENROUTER_API_KEY:
            raise ValueError("Environment variable 'openrouter_api_key' is not configured.")
        if not BASE_URL:
            raise ValueError("Environment variable 'base_url' is not configured.")

        return UsageTrackedOpenAIChatCompletionClient(
            model=MODEL,
            api_key=OPENROUTER_API_KEY,
            base_url=BASE_URL,
            max_tokens=1024,
            temperature=0.0,
            model_info={
                "vision": False,
                "function_calling": True,
                "json_output": True,
                "family": "unknown",
                "structured_output": True,
            },
        )


class LoggerManager:
    @staticmethod
    def info(message: str):
        logger.info(message)

    @staticmethod
    def warning(message: str):
        logger.warning(message)

    @staticmethod
    def error(message: str):
        logger.error(message)

    @staticmethod
    def debug(message: str):
        logger.debug(message)

    @staticmethod
    def critical(message: str):
        logger.critical(message)


logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)
logger.add(
    f"{LOG_DIR}/application.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="INFO",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
)
logger.add(
    f"{LOG_DIR}/error.log",
    rotation="5 MB",
    retention="60 days",
    compression="zip",
    level="ERROR",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
)

settings = Settings()


class usage_capture:
    """Context manager that makes a per-request collector available to the client."""

    def __init__(self, capture: Optional[LLMUsageCapture] = None):
        self.capture = capture or LLMUsageCapture()
        self._token = None

    def __enter__(self):
        self._token = _ACTIVE_USAGE_CAPTURE.set(self.capture)
        return self.capture

    def __exit__(self, exc_type, exc_value, traceback):
        if self._token is not None:
            _ACTIVE_USAGE_CAPTURE.reset(self._token)
        return False
