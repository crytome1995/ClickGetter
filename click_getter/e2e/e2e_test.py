import os
import requests
from config import config
import os

os.environ["AWS_DEFAULT_REGION"] = config.default_region
url = os.getenv("E2E_HOST")


def test_click_endpoint():
    r = requests.get(url + "/click")
    status = r.status_code
    assert status == 200
