#!python3

import urllib.request, urllib.parse
import http.cookiejar
import re

# 输入学号和密码
USERNAME = 'username' or input('学号')
PASSWORD = 'password' or input('密码')


# 准备网络组件
cookie_jar = http.cookiejar.CookieJar()
cookie_handler = urllib.request.HTTPCookieProcessor(cookie_jar)
opener = urllib.request.build_opener(cookie_handler)


# 打开广州大学统一认证系统
cas_url = 'https://cas.gzhu.edu.cn/cas_server/login'
with opener.open(cas_url) as response:
    # 取得网页编码
    charset = re.search(r'charset=(.*)', response.getheader('Content-Type')).group(1)

    # 解析网页获得表单数据以便后续模拟登陆
    data: dict = {}  # 在登陆的POST请求中提交的数据
    body = response.read().decode(charset)
    form = re.search(r'<form id="fm1"[\s\S]*?>(?P<content>[\s\S]*)</form>', body).group('content')  # 定位登陆表单

    # 组合登陆数据
    for line in form.split('\n'):
        match = re.match(r'\s*<input.*name="(?P<name>.*?)".*value="(?P<value>.*?)".*/>', line)
        if match and 'type="reset"' not in line:
            data[match.group('name')] = match.group('value')
    data['username'], data['password'] = USERNAME, PASSWORD


# 尝试登陆
with opener.open(cas_url, urllib.parse.urlencode(data).encode(charset)) as response:
    body = response.read().decode('utf-8')
    print(body)
    if '账号或密码错误' in body:
        print('学号或密码错误')
        exit(0)


exit(0)

login_url = 'https://cas.gzhu.edu.cn/cas_server/login'
login_data = urllib.parse.urlencode({
    'username': USERNAME,
    'password': PASSWORD,
    'captcha': '',
    'warn': 'true',
    'lt': 'LT-630570-5esaZtcSufJzr9hrYcaxbh9zbazhbn-cas01.example.org',
    'execution': 'e4s1',
    '_eventId': 'submit',
    'submit': '登陆'
}).encode('utf-8')
login_request = urllib.request.Request(login_url, login_data)

opener.open(login_url)
print(login_data)

for item in cookie_jar:
    print(item)

with opener.open(login_request) as response:
    print(response.getcode())
    if '账号' in response.read().decode('utf-8'):
        print('ok')

for item in cookie_jar:
    print(item)
