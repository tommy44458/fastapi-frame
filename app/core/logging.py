import logging

from config import SERVER_CONFIG


_NOISY_LIBS = ("httpx", "httpcore", "multipart", "asyncio")


def configure_logging() -> None:
    level = logging.DEBUG if SERVER_CONFIG.DEBUG_LOG else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    for name in _NOISY_LIBS:
        logging.getLogger(name).setLevel(logging.WARNING)
