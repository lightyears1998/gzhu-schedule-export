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

# 服务器在成功登陆后检查User-Agent
# 发起无UA请求的IP会被短暂禁止连接
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]


# 访问统一认证系统
cas_url = 'https://cas.gzhu.edu.cn/cas_server/login'
with opener.open(cas_url) as response:
    # 取得网页编码
    charset = re.search(r'charset=(.*)', response.getheader('Content-Type')).group(1)

    # 解析网页获得表单数据以便后续模拟登陆
    data: dict = {}  # 在登陆的POST请求中提交的数据
    payload = response.read().decode(charset)
    form = re.search(r'<form id="fm1"[\s\S]*?>(?P<content>[\s\S]*)</form>', payload).group('content')  # 定位登陆表单

    # 组合登陆数据
    for line in form.split('\n'):
        match = re.match(r'\s*<input.*name="(?P<name>.*?)".*value="(?P<value>.*?)".*/>', line)
        if match and 'type="reset"' not in line:
            data[match.group('name')] = match.group('value')
    data['username'], data['password'] = USERNAME, PASSWORD


# 登陆统一认证系统
with opener.open(cas_url, urllib.parse.urlencode(data).encode(charset)) as response:
    payload = response.read().decode(charset)
    if '账号或密码错误' in payload:
        print('用户名或密码错误')
        exit(0)


# 登陆教务系统
jwxt_login_url = 'http://jwxt.gzhu.edu.cn/jwglxt/lyiotlogin'
opener.open(jwxt_login_url)


# 打开个人信息查询页面
info_url = 'http://jwxt.gzhu.edu.cn/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default'
with opener.open(info_url) as response:
    payload = response.read().decode(charset)

    # 查询姓名
    match = re.search(r'<label[\s\S]*?姓名[\s\S]*?<p.*?>(?P<name>.*?)</p>', payload)
    if match:
        print('欢迎，' + match.group('name'))

