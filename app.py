from flask import Flask, Response
from seleniumbase import SB
import time
import os


app = Flask(__name__)


COOKIE_NAME = "__illit"

PAGE_1 = "https://5afterdark.mom/"
PAGE_2 = "https://5afterdark.mom/video/7e4de128-b10f-dc2b-0542-7590c441630e"



def wait_for_cookie(sb, cookie_name, timeout=8):

    start = time.time()

    while time.time() - start < timeout:

        for cookie in sb.driver.get_cookies():

            if cookie["name"] == cookie_name:
                return cookie["value"]

        sb.sleep(0.2)

    return None




def get_cookie():

    with SB(uc=True) as sb:


        print("Ouverture page 1")

        sb.uc_open_with_reconnect(
            PAGE_1,
            1
        )


        print("Ouverture page 2")

        sb.uc_open_with_reconnect(
            PAGE_2,
            1
        )


        cookie_value = wait_for_cookie(
            sb,
            COOKIE_NAME,
            timeout=8
        )


        if cookie_value:

            print(
                "COOKIE:",
                cookie_value
            )

            return cookie_value


        raise Exception(
            "Cookie __illit introuvable"
        )




@app.route("/")
def home():

    return """
    <!DOCTYPE html>

    <html>

    <head>

    <title>Cookie Runner</title>

    <style>

    body {
        font-family: Arial;
        text-align:center;
        margin-top:80px;
    }


    button {

        padding:15px 30px;
        font-size:18px;

    }

    </style>

    </head>


    <body>

    <h1>Cookie Runner</h1>


    <form action="/run">

    <button>
    Récupérer le cookie
    </button>

    </form>


    </body>

    </html>
    """




@app.route("/run")
def run():

    try:

        cookie = get_cookie()


        return f"""
        <h1>Cookie trouvé</h1>

        <textarea style="width:90%;height:120px">
{cookie}
        </textarea>
        """



    except Exception as e:

        return Response(
            "Erreur :\n" + str(e),
            status=500,
            mimetype="text/plain"
        )





if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )


    app.run(
        host="0.0.0.0",
        port=port
    )
