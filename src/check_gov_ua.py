import requests
from time import sleep

class RecaptchaError(Exception):
    """Cannot get recaptcha token from a given url
    """
    def __init__(self, url):
        super().__init__(f'Cannot get recaptcha token from a given url: {url}')
        self.url = url

class CheckGovUa:
    """Wrapper for state statement check service (https://check.gov.ua)
    Provide functionality:
        - get recaptcha token (allows to perform a single request)
        - request the download link by a given receipt ID
    """

    CHECK_GOV_UA_HANDLER_URL = 'https://check.gov.ua/api/handler'
    CHECK_GOV_UA_URL = 'https://check.gov.ua'

    def __init__(self, webdriver_instance):
        self.driver = webdriver_instance

    def get_recaptcha_token(self):
        self.driver.get(CheckGovUa.CHECK_GOV_UA_URL)
        for i in range(10):
            recaptchaToken = self.driver.execute_script('return window.conf.recaptchaToken')
            if recaptchaToken is not None:
                return recaptchaToken
            sleep(0.3)
        raise RecaptchaError(url)

    def request_download_link(self, company, receipt_id, recaptcha_token):
        headers = {
            "Accept": "*/*",
            "Content-Type": "text/plain; charset=utf-8",
            "Origin": "https://check.gov.ua",
            "Accept-Language": "en-GB,en;q=0.9",
            "Host": "check.gov.ua",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
            "Referer": "https://check.gov.ua/",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        data = {
            "c": "check",
            "company": company,
            "check": receipt_id,
            "recaptcha": recaptcha_token,
            "browser": {
                "name": "safari",
                "version": "15.4",
                "platform": "desktop",
                "os": "osx",
                "osVer": "10.15.7",
                "language": "uk",
                "adblockState": False
            }
        }
        response = requests.post(CheckGovUa.CHECK_GOV_UA_HANDLER_URL, headers=headers, json=data)
        return response.json()["link"]
