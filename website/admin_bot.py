from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sys
import json


# with open('config.json', "r") as file:
#     content = file.read()
#     config = json.loads(content)



def visit_with_cookies(page_to_load, session_cookie):
    print('visit_with_cookies called', flush=True)

    # service = Service(
    #     executable_path="/home/miki/Documents/learn/render-me-this-CTF/website/geckodriver", 
    #     service_log_path="/home/miki/Documents/learn/render-me-this-CTF/website/geckodriver.log"
    #     )
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options = options)
    try:
        browser.set_page_load_timeout(2)
        browser.get("http://127.0.0.1:5000")
        cookie_data = {
            'name' : 'session',
            'value': session_cookie
            }

        browser.add_cookie(cookie_data)

        browser.get(page_to_load)
        browser.quit()
    except Exception as e:
        print(e, flush=True)
        browser.quit()
        print('Came in the exception loop.', flush=True)

    print('visit_with_cookies function successfully executed', flush=True)


import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)




if __name__ == "__main__":

    try:
        with time_limit(2):
            visit_with_cookies(
        page_to_load="http://127.0.0.1:5000/reports",
        session_cookie='.eJwlzkkKAjEQAMC_5Oyh01vSfkaSXlDwNIMn8e8KUh-od7vVkee9XWs9z7y02yPate20ObukmszakOGykMy40ywfMpNAxddPTdrFY2xDkEG8w516mSKkTtcaCsIqpqbMPZesTehWK4KDR3VGVAFAWiLge3BE-0VeZx7_DbbPF9ybLw8.Z7dJog.yNond60Yr0AEMOMZbM_6R0Njycs'
        )
    except TimeoutException as e:
        print("Timed out!")
    