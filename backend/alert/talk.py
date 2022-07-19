from json import dumps
from httpx import post
from inspect import cleandoc


class KakaoTalk:
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    def __headers(self, token):
        return {
            # "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
        }

    @classmethod
    def send(cls, token: str) -> int:
        """text는 최대 200자"""
        text = cleandoc(
            """
            """
        )
        data = {
            "template_object": dumps(
                {
                    "object_type": "text",
                    "text": text,
                    "link": {
                        "web_url": "https://f.kakao.com",
                        "mobile_web_url": "https://developers.kakao.com",
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
        text = cleandoc(
            """
            [환율 알리미]
            안녕하세요 환율 알리미 입니다
            여러 환율에 알림을 설정해 받아보실 수 있습니다😊
            """
        )
        data = {
            "template_object": dumps(
                {
                    "object_type": "text",
                    "text": text,
                    "link": {
                        "web_url": "https://finance.1ife.kr/USD",
                        "mobile_web_url": "https://finance.1ife.kr/USD",
                    },
                    "buttons": [
                        {
                            "title": "일본 환율 보기",
                            "link": {
                                "web_url": "https://finance.1ife.kr/JPY",
                                "mobile_web_url": "https://finance.1ife.kr/JPY",
                            },
                        }
                    ],
                }
            )
        }
        res = post(cls.url, headers=cls.__headers(cls, token), data=data)
        print(res.json())
        return res.status_code
