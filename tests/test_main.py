from selenium import webdriver
import logging

from webdriver_manager.chrome import ChromeDriverManager

log = logging.getLogger(__name__)

service = webdriver.ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def test_example(uvicorn_runner):
    log.info("Opening browser")
    driver.get("http://localhost:8001")
    log.info("Testing if title is correct")
    assert "Pet Library" in driver.title
    driver.quit()