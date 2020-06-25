from pydantic import BaseSettings, HttpUrl


class Settings:
    # 课程 url
    course_url: HttpUrl = "http://mooc1.mooc.whu.edu.cn/mycourse/studentstudy"
    # 信息 url，用于获取 mArg
    info_url: HttpUrl = "http://mooc1.mooc.whu.edu.cn/knowledge/cards"
    # 课程 url，用于获取请求 info_url 的参数
    student_ajax_url: HttpUrl = "http://mooc1.mooc.whu.edu.cn/mycourse/studentstudyAjax"

    host_url: HttpUrl = "mooc1.mooc.whu.edu.cn"
    referer_url: HttpUrl = "mooc1.mooc.whu.edu.cn"

    base_url: HttpUrl = "http://mooc1.mooc.whu.edu.cn"


settings = Settings()
