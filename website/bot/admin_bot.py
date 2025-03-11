from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sys
import json
import requests


def visit_with_cookies(page_to_load, session_cookie):
    print('visit_with_cookies called', flush=True)
    # service = Service(
    #     executable_path="/home/miki/Documents/learn/render-me-this-CTF/website/geckodriver", 
    #     service_log_path="/home/miki/Documents/learn/render-me-this-CTF/website/geckodriver.log"
    #     )
    print(page_to_load)
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


def get_session_cookie(ip_and_port, username, password):
    res = requests.post(
        url=f"http://{ip_and_port}/login",
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

def visit_with_cookies_time_limit(max_time_seconds, url, session_cookie):
    try:
        with time_limit(max_time_seconds):
            visit_with_cookies(
        page_to_load=url,
        session_cookie=session_cookie
        )
    except TimeoutException as e:
        print("Timed out!")



if __name__ == "__main__":

    # try:
    #     with time_limit(2):
    #         visit_with_cookies(
    #     page_to_load="http://127.0.0.1:5000/report/1",
    #     session_cookie='.eJwljjEOAjEMwP6SmaFp2qS5z6A0TQQS052YEH-nEqO92B-45xnXA4601xU3uD8XHJCu0a1rUatGk9hIylpCNTynrhZoVAJ71NQhLkTD0KeH8NTKXh3NJMmHNJYe0pUDpTcs1TYXVpxVcbgrJ2O4s-eO8BZNYI-8rzj_NwjfHxtBL50.Z7yOkQ.rJCDXfHQcTOdj_BXFawdRWkth34'
    #     )
    # except TimeoutException as e:
    #     print("Timed out!")
    print(login("127.0.0.1:5000", "admin", "admin"))
    