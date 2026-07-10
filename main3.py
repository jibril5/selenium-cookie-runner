from fastapi import FastAPI
from fastapi.responses import FileResponse
from seleniumbase import SB
from datetime import datetime, timedelta
import os


app = FastAPI()


cookie_cache = {
    "cookie": None,
    "generated_at": None
}


COOKIE_DURATION_MINUTES = 30


@app.get("/")
def home():
    return {
        "status": "online"
    }


@app.get("/screenshot")
def screenshot():

    if os.path.exists("/tmp/debug.png"):
        return FileResponse(
            "/tmp/debug.png",
            media_type="image/png"
        )

    return {
        "error": "aucune capture disponible"
    }


@app.get("/get-cookie")
def get_cookie():

    # Vérification du cache
    if cookie_cache["cookie"] and cookie_cache["generated_at"]:

        age = datetime.now() - cookie_cache["generated_at"]

        if age < timedelta(minutes=COOKIE_DURATION_MINUTES):

            return {
                "cookie": cookie_cache["cookie"],
                "generated_at": cookie_cache["generated_at"].strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "cached": True
            }


    print("=== DEMARRAGE SELENIUM ===")


    with SB(
        uc=True,
        headless=True
    ) as sb:


        url = (
            "https://5afterdark.mom/video/7e4de128-b10f-dc2b-0542-7590c441630e"
        )


        print("Ouverture :", url)


        sb.uc_open_with_reconnect(
            url,
            2
        )


        sb.driver.uc_activate_cdp_mode(url)


        # Attente du chargement/challenge
        sb.sleep(10)


        # Capture écran debug
        try:
            sb.driver.save_screenshot(
                "/tmp/debug.png"
            )

            print("Screenshot sauvegardé")

        except Exception as e:
            print(
                "Erreur screenshot :",
                e
            )


        print(
            "URL finale :",
            sb.driver.current_url
        )

        print(
            "TITLE :",
            sb.driver.title
        )


        # Liste des cookies
        cookies = sb.driver.get_cookies()


        print("===== COOKIES =====")

        for c in cookies:
            print(
                c["name"]
            )

        print("===================")



        for cookie in cookies:


            if cookie["name"] == "__illit":


                cookie_cache["cookie"] = cookie["value"]

                cookie_cache["generated_at"] = datetime.now()


                print(
                    "COOKIE TROUVE !"
                )


                return {

                    "cookie": cookie["value"],

                    "generated_at":
                        cookie_cache["generated_at"].strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),

                    "cached": False
                }



    print(
        "COOKIE NON TROUVE"
    )


    return {
        "error": "Cookie non trouvé"
    }
