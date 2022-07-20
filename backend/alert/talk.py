from json import dumps
from httpx import post
from inspect import cleandoc

from django.template.loader import render_to_string


class KakaoTalk:
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    def __headers(self, token):
        return {
            # "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
        }

    @classmethod
    def text(cls, currency: str, price: int) -> str:
        # text는 최대 200자
        return cleandoc(
            """
            [환율 알리미]
            안녕하세요 환율 알리미 입니다
            {currency} {price:,}원🔔
            원하는 가격에 도달했어요
            """.format(
                currency=currency, price=price
            )
        )

    @classmethod
    def send(cls, token: str, text: str, url_path: str) -> int:
        # text는 최대 200자
        data = {
            "template_object": dumps(
                {
                    "object_type": "text",
                    "text": text,
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
        text = render_to_string("kakao/welcome.txt")
        # text = cleandoc(
        #     """
        #     [환율 알리미]
        #     안녕하세요 환율 알리미 입니다
        #     여러 환율에 알림을 설정해 받아보실 수 있습니다😊
        #     """
        # )
        data = {
            "template_object": dumps(
                {
                    "object_type": "text",
                    "text": text,
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
