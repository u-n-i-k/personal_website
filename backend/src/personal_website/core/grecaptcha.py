import requests
from pydantic import SecretStr

from personal_website.core.config import Config


def get_grecaptcha_secret_token() -> SecretStr:
    return Config.instance.fastapi.grecaptcha_secret_token  # type: ignore


def check_grecaptcha_token(
    token: str,
    secret_token: SecretStr,
    user_ip: str | None,
    grecaptcha_check_url: str = "https://www.google.com/recaptcha/api/siteverify",
) -> None:
    success = True
    try:
        data = {"secret": secret_token.get_secret_value(), "response": token}
        if user_ip:
            data["remoteip"] = user_ip
        resp = requests.post(url=grecaptcha_check_url, data=data)
        resp.raise_for_status()
        if not resp.json()["success"]:
            success = False
    except Exception:
        raise RuntimeError("unknown error occured while checking grecaptcha token")
    if not success:
        raise ValueError("invalid grecaptcha token")
