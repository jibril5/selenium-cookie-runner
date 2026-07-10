from fastapi import FastAPI
from seleniumbase import SB

app = FastAPI()

@app.get("/get-cookie")
def get_cookie():
    with SB(uc=True, headless=False) as sb:
        url = "https://5afterdark.mom/video/7e4de128-b10f-dc2b-0542-7590c441630e"

        sb.uc_open_with_reconnect(url, 0.001)
        sb.driver.uc_activate_cdp_mode(url)

        sb.uc_gui_click_captcha()

        sb.driver.connect()

        for cookie in sb.driver.get_cookies():
            if cookie["name"] == "__illit":
                return {"cookie": cookie["value"]}
