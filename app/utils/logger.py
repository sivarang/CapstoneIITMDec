f"""
Centralized Logger
"""

from pathlib import Path
import logging
import sys
import tempfile

# ---------------------------------------------------------------------
# Log Directory
# ---------------------------------------------------------------------

LOG_DIR = Path(tempfile.gettempdir()) / "router_support_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "router_support.log"

# ---------------------------------------------------------------------
# Logger Configuration
# ---------------------------------------------------------------------

logger = logging.getLogger("RouterSupport")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# ---------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------

def log_agent_start(agent_name: str):
    logger.info("=" * 60)
    logger.info(f"Starting {agent_name}")


def log_agent_end(agent_name: str):
    logger.info(f"Completed {agent_name}")
    logger.info("=" * 60)


def log_router(vendor: str, model: str):
    logger.info(
        f"Router detected | Vendor={vendor} | Model={model}"
    )


def log_rag(query: str):
    logger.info(f"RAG Query: {query}")


def log_docs(count: int):
    logger.info(f"Pinecone returned {count} document(s)")


def log_error(error: Exception):
    logger.exception(error)