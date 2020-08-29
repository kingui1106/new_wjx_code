from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError
import requests
from bs4 import BeautifulSoup
import re
import random
import time
import datetime
import fake_info
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''
作者：normanbb
链接：https://github.com/NormanBB/WJX_Autosubmit
来源：Github
'''

'''调查页面，获取相关参数'''
# 获取调查问卷的页面
class WenJuanXing:
    def __init__(self, url, win, times, thread):
        """
        :param url:要填写的问卷的url
        """
        self.url = url
        self.win = win
        self.times = times
        self.thread = thread
        self.now = False
        self.state = False

    def get_fill_content(self,url, user_agent):
        headers = {
        'user-agent': user_agent,
        "Connection": "close"
        }
        r1 = requests.get(url, headers=headers,verify=False)
        setCookie = r1.headers['Set-Cookie']
        CookieText = re.findall(r'acw_tc=.*?;', setCookie)[0] + re.findall(r'\.ASP.*?;', setCookie)[0] + re.findall(r'jac.*?;', setCookie)[0] + re.findall(r'SERVERID=.*;',setCookie)[0]
        return r1.text,CookieText

    # 从页面中获取curid,rn,jqnonce,starttime,同时构造ktimes用作提交调查问卷
    def get_submit_query(self,content):
        curid = re.search(r'\d{8}',content).group()
        rn = re.search(r'\d{9,10}\.\d{8}',content).group()
        jqnonce= re.search(r'.{8}-.{4}-.{4}-.{4}-.{12}',content).group()
        ktimes = random.randint(5, 18)
        starttime = (datetime.datetime.now()-datetime.timedelta(minutes=1)).strftime("%Y/%m/%d %H:%M:%S")
        return curid, rn, jqnonce, ktimes, starttime

    #通过ktimes,jqnonce构造jqsign
    def get_jqsign(self,ktimes, jqnonce):
            result = []
            b = ktimes % 10
            if b == 0:
                b = 1
            for char in list(jqnonce):
                f = ord(char) ^ b
                result.append(chr(f))
            return ''.join(result)


    '''获取随机答案'''

    # 获取调查问卷的题目
    def get_title_list(self,content):
        main_soup = BeautifulSoup(content, 'lxml')
        title_soup_list = main_soup.find_all(id=re.compile(r'div\d'))
        title_list = []
        for title_soup in title_soup_list:
            title_str = title_soup.find(class_='div_title_question').get_text().strip()
            choice_list = [choice.get_text() for choice in title_soup.find_all('label')]
            title_dict = {
                'title': title_str,
                'choice_list': choice_list,
                'is_choice': len(choice_list) != 0
            }
            title_list.append(title_dict)
        return title_list

    # 随机选择
    def random_choose(self,title_list):
        answer_list = []
        for title in title_list:
            if title['is_choice']:
                title['answer'] = random.randint(1, len(title['choice_list']))
            else:
                title['answer'] = ''
            answer_list.append(title['answer'])
        return answer_list

    #构造符合样式的提交数据
    def get_submit_data(self,title_list,answer_list):
        form_data = ''
        for num in range(len(title_list)):
            form_data += str(num+1) + '$' + str(answer_list[num]) + '}'
        return form_data[:-1]


    def Auto_WjX(self,ip_list):
        try:
            user_agent = UserAgent().random
        except FakeUserAgentError:
            user_agent = self.proxy.get_agent()
        #ip_list = proxy.choose_proxy(filename)
        ip = random.choice(ip_list)
        fill_content,cookies = self.get_fill_content(self.url,user_agent)#网页源代码，cookies
        title_list = self.get_title_list(fill_content) #所有题目
        '''获取相关参数'''
        curid, rn, jqnonce, ktimes,starttime = self.get_submit_query(fill_content)
        jqsign = self.get_jqsign(ktimes,jqnonce)
        time.sleep(random.randint(3, 10))
        time_stamp = '{}{}'.format(int(time.time()), random.randint(100, 200))  # 生成一个时间戳，最后三位为随机数
        #curid, time_stamp, starttime, ktimes, rn, jqnonce, jqsign
        FormData = {
                'submittype': '1',
                'curID': curid,
                't': time_stamp,
                'starttime': starttime,
                'rn': rn,
                'hlv': '1',
                'ktimes':ktimes,
                'jqnonce':jqnonce,
                'jqsign':jqsign,
            }
        url = 'https://www.wjx.cn/joinnew/processjq.ashx'
        headers = {
            "Host": "www.wjx.cn",
            "Connection": "close",
            "User-Agent": user_agent,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en, zh-CN;q=0.9, zh;q=0.8",
            "Referer": self.url,
            "Cookie": cookies,
        }
        #作随机选择
        random_data = self.random_choose(title_list)
        #构造符合样式的提交数据
        #自定义答案可以将选择与构造部分去除
        submit_data = self.get_submit_data(title_list,random_data)
        data = {'submitdata':str(submit_data)}
        #data = {'submitdata': '1$2}2$1}3$2}4$2}5$1}6$1}7$1}8$3}9$3}10$1}11$2}12$2}13$1'}
        # 发送请求
        try:
            r = requests.post(url=url, headers=headers, data=data, params=FormData, proxies={
                              "https":ip}, verify=False, timeout=10)
            #通过测试返回数据中表示成功与否的关键数据（’10‘or '22s'）在开头,所以只需要提取返回数据中前两位元素
            result = r.text[0:2]
            return result
        except(requests.exceptions.ProxyError,requests.exceptions.ConnectTimeout):
            self.win.textBrowser.append('未知错误'+ self.randommystr())
            ip_list.remove(ip)
        except requests.exceptions.ReadTimeout:
            pass

    def randommystr(self):
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        sa = []
        for i in range(8):
            sa.append(random.choice(seed))
        salt = ''.join(sa)
        return salt
    def main(self, times):
        PostNum = 0
        times=int(times)
        self.win.textBrowser.append('开始提交')
        ip_list = self.proxy.choose_proxy(filename)
        # i 为 提交次数
        # 若需达到某特定次数
        #while i < Postnum:
        for i in range(times):
            try:
                result= self.Auto_WjX(ip_list)
                if '10' in result:
                    self.win.textBrowser.append('提交成功' + self.randommystr())
                    PostNum += 1
                    time.sleep(5)  # 设置休眠时间，这里要设置足够长的休眠时间
                else:
                    self.win.textBrowser.append('提交失败' + self.randommystr())
            #捕获错误
            except(TypeError,IndexError,ValueError):
                self.win.textBrowser.append('未知错误'+ self.randommystr())
                continue
        #print('提交结束，已经提交%s份调查报告' % PostNum)  # 总结提交成功的数量，并打印
        self.win.textBrowser.append('提交结束，已经提交%s份调查报告' % PostNum)
        self.win.pushButton.setEnabled(True)
        self.thread.flag = False
        self.now = False

    def various_options(self):
        #根据参数匹配不同条件
        global filename
        filename = 'origin_log_temp'
        f = open(filename, mode='w')
        f.close()
        #if os.path.exists(filename):
        #    os.remove(filename)
        self.proxy = fake_info.proxy()
        self.proxy.get_proxy('pool')
        self.proxy.validate_proxy('origin_log')
    def start_up(self):
        if self.now:
           return
        self.now = True
        if not self.state:
            self.win.textBrowser.append("开始准备")
            startTime = time.time()
            self.various_options()
            endTime = time.time()
            self.win.textBrowser.append("准备完成，用时： %.2f s " % (endTime - startTime))
            self.state = True
        fill_url = self.url
        if 'm' in fill_url:
            self.url = fill_url.replace('m', 'jq')
        times = self.times
        self.main(times)
    


