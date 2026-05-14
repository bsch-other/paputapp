from selenium import webdriver
import logging
log = logging.getLogger(__name__)


def test_example(uvicorn_runner):
    driver = webdriver.Edge()
    log.info("Opening browser")
    driver.get("http://localhost:8001")
    log.info("Testing if title is correct")
    assert "Pet Library" in driver.title
    driver.quit()