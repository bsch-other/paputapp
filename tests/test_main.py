from selenium import webdriver
import logging

log = logging.getLogger(__name__)

def test_example(uvicorn_runner):
    log.info("Opening browser")
    driver = webdriver.Firefox()
    driver.get("http://localhost:8001")
    log.info("Testing if title is correct")
    assert "Pet Library" in driver.title
    driver.quit()