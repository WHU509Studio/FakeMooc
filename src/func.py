import re
import hashlib
import json
import time
from client import CookieUserClient


class User:

    def __init__(self, cookies):
        self.client = CookieUserClient(cookies=cookies)

    # 生成enc
    def _make_enc(self, time, clazzId, duration, clipTime, objectId, jobid, userid):
        if jobid == None:
            jobid = ''
        raw = '[{0}][{1}][{2}][{3}][{4}][{5}][{6}][{7}]'.format(clazzId, userid, jobid, objectId, time*1000, "d_yHJ!$pdA~5", duration*1000, clipTime)
        return hashlib.md5(raw.encode('utf-8')).hexdigest()

    # 生成视频状态序列
    def _make_sequence(self, clazzId, duration, clipTime, objectId, jobid, userid):
        playingTime = -60
        result = []
        while playingTime < duration:
            playingTime += 60
            if playingTime > duration:
                playingTime = duration
            enc = self._make_enc(playingTime, clazzId, duration, clipTime, objectId, jobid, userid)
            result.append((playingTime, enc))
        return result

    # 获取相关参数
    def _get_arg(self, url):
        # 从url中截取一部分参数
        chapterId = re.search(r'chapterId=(.*?)&', url).group(1)
        clazzId = re.search(r'clazzid=(.*?)&', url).group(1)
        courseId = re.search(r'courseId=(.*?)&', url).group(1)

        # 构造请求
        url = "http://mooc1.mooc.whu.edu.cn/knowledge/cards?clazzid=" + clazzId + "&courseid=" + courseId + "&knowledgeid=" + chapterId + "&num=0&ut=s&cpi=64752888&v=20160407-1"

        #从返回的页面中获取另一部分参数
        html = self.client.get(url).text
        arg_string = re.search("mArg = ({.+?});", html, re.S).group(1)
        arg = json.loads(arg_string)

        # 删除多余项
        del_list = []
        for i in range(len(arg['attachments'])):
            if len(arg['attachments'][i]) != 9:
                del_list.append(i)
        for i in del_list:
            del arg['attachments'][i]

        for item in arg['attachments']:
            sub_url = item['objectId']
            url = "http://mooc1.mooc.whu.edu.cn/ananas/status/" + sub_url
            html = self.client.get(url).text
            item['dtoken'] = re.search('"dtoken":"(.*?)"', html).group(1)

        return arg

    def play_video(self, url):
        # 获取相关参数
        arg = self._get_arg(url)
        clazzId = str(arg['defaults']['clazzId'])
        userid = arg['defaults']['userid']

        # 播放页面中所有视频
        for video in arg['attachments']:

            # 相关参数预处理
            duration = int(int(video['headOffset'])/1000)
            clipTime = '0_' + str(duration)
            objectId = video['objectId']
            otherInfo = video['otherInfo']
            jobid = video['jobid']
            dtoken = video['dtoken']
            sequence = self._make_sequence(clazzId, duration, clipTime, objectId, jobid, userid)
            duration = str(duration)
            standard_t = int(round(time.time() * 1000))

            # 将每一个状态序列依次发送到服务端
            for info in sequence:

                # 相关参数预处理
                playingTime = str(info[0])
                _t = str(standard_t + int(playingTime) * 1000)
                enc = info[1]

                # 拼接url
                url = "http://mooc1.mooc.whu.edu.cn/multimedia/log/a/64752888/" + dtoken + "?clazzId=" + clazzId + "&playingTime=" + playingTime +"&duration=" + duration + "&clipTime=" + clipTime + "&objectId=" + objectId + "&otherInfo=" + otherInfo + "&jobid=" + jobid + "&userid=" + userid + "&isdrag=0&view=pc&enc=" + enc + "&rt=0.9&dtype=Video&_t=" + _t

                # 发送请求并回执状态码
                print(self.client.get(url).status_code)


if __name__ == '__main__':
    url = input("Input the url here:\n")

    # 读取cookies
    f = open(r'cookies.txt', 'r')
    cookies = {}
    for line in f.read().split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value

    # 实例化User
    user = User(cookies)
    #播放视频
    user.play_video(url)