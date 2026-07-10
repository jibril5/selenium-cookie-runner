from fastapi import FastAPI
from seleniumbase import SB
from datetime import datetime, timedelta

app = FastAPI()

# Cache global
cookie_cache = {
    "cookie": None,
    "generated_at": None
}

COOKIE_DURATION_MINUTES = 30


@app.get("/get-cookie")
def get_cookie():

    # Vérification du cookie existant
    if cookie_cache["cookie"] and cookie_cache["generated_at"]:

        age = datetime.now() - cookie_cache["generated_at"]

        if age < timedelta(minutes=COOKIE_DURATION_MINUTES):
            return {
                "cookie": cookie_cache["cookie"],
                "generated_at": cookie_cache["generated_at"].strftime("%Y-%m-%d %H:%M:%S"),
                "cached": True
            }


    # Aucun cookie valide → génération d'un nouveau
    with SB(uc=True, headless=True) as sb:

        url = "https://5afterdark.mom/video/7e4de128-b10f-dc2b-0542-7590c441630e"

        sb.uc_open_with_reconnect(url, 0.1)
        sb.driver.uc_activate_cdp_mode(url)

        sb.driver.connect()

        for cookie in sb.driver.get_cookies():

            if cookie["name"] == "__illit":

                # Sauvegarde en cache
                cookie_cache["cookie"] = cookie["value"]
                cookie_cache["generated_at"] = datetime.now()

                return {
                    "cookie": cookie["value"],
                    "generated_at": cookie_cache["generated_at"].strftime("%Y-%m-%d %H:%M:%S"),
                    "cached": False
                }

    return {"error": "Cookie non trouvé"}
