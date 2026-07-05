from flask import Flask, Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os

app = Flask(__name__)

COOKIE_NAME = "__illit"
PAGE_1 = "https://5afterdark.mom/"
PAGE_2 = "https://5afterdark.mom/video/7e4de128-b10f-dc2b-0542-7590c441630e"


def get_cookie():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium"

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")

    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(PAGE_1)
        time.sleep(2)

        driver.get(PAGE_2)
        time.sleep(4)

        cookie_value = ""

        for cookie in driver.get_cookies():
            if cookie.get("name") == COOKIE_NAME:
                cookie_value = cookie.get("value", "")
                break

        with open("cookie.txt", "w", encoding="utf-8") as f:
            f.write(cookie_value)

        return cookie_value if cookie_value else "Cookie introuvable"

    finally:
        driver.quit()


@app.route("/")
def home():
    return """
    <h1>Cookie Runner</h1>
    <form action="/run" method="get">
        <button type="submit">Récupérer le cookie</button>
    </form>
    """


@app.route("/run")
def run():
    result = get_cookie()
    return Response(result, mimetype="text/plain")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
