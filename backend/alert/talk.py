from json import dumps
from httpx import post

from django.template.loader import render_to_string


class KakaoTalk:
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    def __headers(self, token):
        return {
            # "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
        }

    @classmethod
    def send(cls, token: str, currency: str, price: int, url_path: str) -> int:
        # text는 최대 200자
        data = {
            "template_object": dumps(
                {
                    "object_type": "text",
                    "text": render_to_string(
                        "kakao/alert.txt", {"currency": currency, "price": price}
                    ),
                    "link": {
                        "web_url": f"https://finance.1ife.kr/{url_path.upper()}",
                        "mobile_web_url": f"https://finance.1ife.kr/{url_path.upper()}",
                    },
                    "button_title": "바로 확인",
                }
            )
        }
        res = post(cls.url, headers=cls.__headers(cls, token), data=data)
        return res.status_code

    @classmethod
    def welcome(cls, token: str) -> int:
        """text는 최대 200자"""
        data = {
            "template_object": dumps(
                {
                    "object_type": "text",
                    "text": render_to_string("kakao/welcome.txt"),
                    "link": {
                        "web_url": "https://finance.1ife.kr",
                        "mobile_web_url": "https://finance.1ife.kr",
                    },
                    "buttons": [
                        {
                            "title": "환율 알리미 바로가기",
                            "link": {
                                "web_url": "https://finance.1ife.kr",
                                "mobile_web_url": "https://finance.1ife.kr",
                            },
                        }
                    ],
                }
            )
        }
        res = post(cls.url, headers=cls.__headers(cls, token), data=data)
        return res.status_code


