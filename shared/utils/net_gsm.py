import requests
from requests.auth import HTTPBasicAuth
from shared.config import Config


class NETGSMUtils:
    BASE_URL = "https://api.netgsm.com.tr/sms/rest/v2/otp"

    @staticmethod
    def send_otp(phone: str, message: str) -> dict:
        response = requests.post(
            NETGSMUtils.BASE_URL,
            auth=HTTPBasicAuth(Config.NET_GSM_USER, Config.NET_GSM_PASSWORD),
            json={
                "msgheader": Config.NET_GSM_USER,
                "msg": message,
                "no": phone,
            },
        )
        data = response.json()
        if data.get("code") != "00":
            raise Exception(f"NetGSM OTP error: {data.get('description', 'unknown error')}")
        return data
