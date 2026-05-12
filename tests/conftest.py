import threading
import logging
from pathlib import Path

import pytest
import uvicorn
import time
import sys

uvlog = logging.getLogger("uvicorn")

sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture(scope="session")
def uvicorn_runner():
    uvlog.info("Server started")

    def app():
        uvicorn.run("src.main:app", port=8001, log_level="info")
        print("application was started")

    t = threading.Thread(target=app, daemon=True)
    t.start()
    time.sleep(1)

    yield