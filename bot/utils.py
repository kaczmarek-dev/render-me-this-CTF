from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests


def visit_with_cookies(page_to_load, session_cookie, prefix):
    print('visit_with_cookies called', flush=True)
    # service = Service(
    #     executable_path="/home/miki/Documents/learn/render-me-this-CTF/website/geckodriver", 
    #     service_log_path="/home/miki/Documents/learn/render-me-this-CTF/website/geckodriver.log"
    #     )
    print(page_to_load)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--user-data-dir=/tmp/user-data")
    options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options = options)
    try:
        browser.set_page_load_timeout(2)
        browser.get(f"http://127.0.0.1:5000")
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


def get_session_cookie(ip_and_port, username, password, prefix):
    res = requests.post(
        url=f"http://{ip_and_port}{prefix}/login",
        data={
            "username": username,
            "password": password
        }
    )
    return res.cookies["session"]

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

def visit_with_cookies_time_limit(max_time_seconds, page_to_load, session_cookie, prefix):
    try:
        with time_limit(max_time_seconds):
            visit_with_cookies(
        page_to_load=page_to_load,
        session_cookie=session_cookie,
        prefix=prefix
        )
    except TimeoutException as e:
        print("Timed out!")
    