"""implementation of client class"""

from requests import Request, Session
from requests.utils import cookiejar_from_dict

from fake_useragent import UserAgent

from utils import logger
from config import settings

from typing import Dict, Union, Optional

ua = UserAgent()


class BaseUserClient:

    def __init__(self, headers: Optional[Dict] = None):
        self.client = Session()
        self._add_headers_to_session(self.client, headers)

    @classmethod
    def _get_headers(cls) -> Dict:
        """获取 headers"""
        return {
            "User-Agent": cls._get_ua(),
            "Host": settings.host_url,
            "Referer": settings.referer_url
        }

    @staticmethod
    def _get_ua() -> str:
        """获取 User-Agent"""
        # todo
        # 保证在一段时间内请求头一样
        return ua.random

    @classmethod
    def _add_headers_to_session(cls, s: Session, headers=None):
        if not headers:
            headers = cls._get_headers()
        s.headers.update(headers)

    def get(self, url, **kwargs):
        return self.client.get(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.client.post(url, data=data, json=json, **kwargs)


class CookieUserClient(BaseUserClient):
    def __init__(self, cookies: Union[str, Dict[str, str]], headers: Optional[Dict] = None):
        super(CookieUserClient, self).__init__(headers)

        cookies = self._process_cookies(cookies)
        self._add_cookies_to_session(self.client, cookies)

    @staticmethod
    def _process_cookies(cookies: Union[str, Dict[str, str]]) -> Dict[str, str]:
        if isinstance(cookies, Dict):
            return cookies
        elif isinstance(cookies, str):
            return dict([item.split("=", 1) for item in cookies.split(";")])
        else:
            logger.error(f"cookies type not supported!")
            raise ValueError

    @classmethod
    def _add_cookies_to_session(cls, s: Session, cookies: Dict[str, str]):
        cookiejar = cookiejar_from_dict(cookies)
        s.cookies.update(cookiejar)


if __name__ == '__main__':
    test_cookies = "test=123456789"

    user = CookieUserClient(test_cookies)
    r = user.get("https://httpbin.org/cookies")
    print(r.text)
    r = user.get("https://httpbin.org/headers")
    print(r.text)
