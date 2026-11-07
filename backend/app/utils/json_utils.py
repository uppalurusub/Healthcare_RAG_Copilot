import json
import re

from app.config.settings import settings
logger = settings.get_logger()


def extract_json(content: str):

    try:

        return json.loads(content)

    except Exception:

        logger.warning(
            "Direct JSON Parsing Failed"
        )

    try:

        content = content.replace(
            "```json",
            ""
        )

        content = content.replace(
            "```",
            ""
        )

        content = content.strip()

        return json.loads(content)

    except Exception:

        logger.warning(
            "Markdown Cleanup Failed"
        )

    try:

        match = re.search(
            r"\{.*\}",
            content,
            re.DOTALL
        )

        if match:

            return json.loads(
                match.group(0)
            )

    except Exception:

        logger.warning(
            "Regex JSON Extraction Failed"
        )

    raise Exception(
        f"Unable to parse JSON.\n\n{content}"
    )