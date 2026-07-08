from seleniumbase import SB
import time

def wait_for_cookie(sb, cookie_name, timeout=8):
    """Attend rapidement l'apparition d'un cookie"""
    start = time.time()

    while time.time() - start < timeout:
        for cookie in sb.driver.get_cookies():
            if cookie["name"] == cookie_name:
                return cookie["value"]

        sb.sleep(0.2)

    return None

with SB(uc=True) as sb:
    # Première page
    sb.uc_open_with_reconnect(
        "https://5afterdark.mom/",
        1
    )

    # Deuxième page directement
    sb.uc_open_with_reconnect(
        "https://5afterdark.mom/video/7e4de128-b10f-dc2b-0542-7590c441630e",
        1
    )

    # Attendre uniquement ce qui est nécessaire
    cookie_value = wait_for_cookie(
        sb,
        "__illit",
        timeout=8
    )

    if cookie_value:
        print(cookie_value)
    else:
        raise Exception("Cookie __illit introuvable")
