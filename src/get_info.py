import httpx
from fake_useragent import UserAgent

from config import settings
from utils import logger

import re

ua = UserAgent()


class GetmArg:
    def __init__(self, course_id, clazz_id, chapter_id, enc, cookies):
        self.course_id = course_id
        self.clazz_id = clazz_id
        self.chapter_id = chapter_id
        self.enc = enc
        self.cookies = cookies

    @property
    def random_headers(self):
        return {
            "Host": "mooc1.mooc.whu.edu.cn",
            "Referer": "mooc1.mooc.whu.edu.cn",
            "User-Agent": ua.random
        }

    def get_cpi(self):
        params = {
            "courseId": self.course_id,
            "chapterId": self.chapter_id,
            "clazzid": self.clazz_id,
            "enc": self.enc
        }
        r = httpx.get(
            settings.course_url, params=params, headers=self.random_headers, cookies=self.cookies
        )
        logger.debug(f"status: {r.status_code}")
        # logger.debug(f"text: {r.text}")
        if r.status_code == 200:
            cpi = re.search("&cpi=(.+?)&", r.text).group(1)
            logger.debug(f"cpi={cpi}")
            return cpi
        else:
            raise NotImplementedError

    def get_param_str(self):
        cpi = self.get_cpi()
        params = {
            "courseId": self.course_id,
            "clazzid": self.clazz_id,
            "chapterId": self.chapter_id,
            "cpi": cpi,
            # 验证码？
            "verificationcode": ""
        }
        r = httpx.get(
            settings.student_ajax_url, params=params, headers=self.random_headers, cookies=self.cookies
        )
        logger.debug(f"status: {r.status_code}")
        # logger.debug(f"text: {r.text}")
        if r.status_code == 200:
            param_str = re.search("/knowledge/cards(.+?)\\\"", r.text).group(1)
            logger.debug(f"param_str={param_str}")
            return param_str
        else:
            raise NotImplementedError

    def get_mArg(self):
        param_str = self.get_param_str()
        r = httpx.get(
            f"{settings.info_url}{param_str}", headers=self.random_headers, cookies=self.cookies
        )
        logger.debug(f"status: {r.status_code}")
        # logger.debug(f"text: {r.text}")
        if r.status_code == 200:
            mArg = re.search("mArg = ({.+?});", r.text, re.S).group(1)
            logger.debug(f"mArg={mArg}")
            return mArg
        else:
            raise NotImplementedError


if __name__ == '__main__':
    pass