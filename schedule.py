#!python3

import urllib.request, urllib.parse
import http.cookiejar
from getpass import getpass
import re
import datetime
import json


"""schedule.py

从广州大学教务系统中获取课程信息，并输出为ics文件，
以便将课程信息导入到支持ics的日历程序中。

"""


""" ⬇⬇⬇ 在下方输入信息 ⬇⬇⬇ """

USERNAME = input('请输入您的学号：')
PASSWORD = getpass(prompt='请输入您的密码：')
YEAR = int(input('请输入学年（学年取前4位数字，如2019-2020学年, 则取2019）：'))
SEMESTER = int(input('请输入学期(1/2), 1=上学期, 2=下学期：'))
DATE_OF_MONDAY_OF_FIRST_WEEK = input('请输入学期第一周的周一的日期（格式：2020/2/17）：')
OUTPUT_FILENAME = 'schedule.ics'  # 输出文件名的默认值
OUTPUT_FILENAME_EDIT = input(f'请填写输出文件名（默认{OUTPUT_FILENAME}）：')

# 当用户填写的输出文件名非空时，使用用户填写的输出文件名
if OUTPUT_FILENAME_EDIT != "":
    OUTPUT_FILENAME = OUTPUT_FILENAME_EDIT + '.ics'

""" ⬆⬆⬆ 信息输入完成 ⬆⬆⬆ """


# 检查信息是否完整
while len(USERNAME) != 10:
	USERNAME = input('您输入的学号有误，请重新输入您的10位数字学号:  ')
while (len(str(YEAR)) != 4):
    YEAR = int(input('您输入的学年有误，请重新输入4位数的学年:  '))
while (SEMESTER != 1 and SEMESTER != 2):
    SEMESTER = int(input('您输入的学期有误，请重新输入学期(1/2):  '))


# 确认已经输入的信息
print('您的学号为' + USERNAME)
print('抓取' + str(YEAR) + '-' + str(YEAR+1) + '学年' + ['上学期', '下学期'][SEMESTER == 2] + '的课程表')
print('第一周的周一设定为' + DATE_OF_MONDAY_OF_FIRST_WEEK)
print('输出文件名为' + OUTPUT_FILENAME)
input('请按回车键确认上述信息：')


# 打印一行空行
print('')


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

    # 下载验证码并提示用户输入
    captcha_url = 'https://cas.gzhu.edu.cn/cas_server/captcha.jsp'
    with opener.open(captcha_url) as captcha:
        with open('captcha.jpg', mode='wb') as captcha_file:
            captcha_file.write(captcha.read())
    data['captcha'] = input("请查看当前目录下的captcha.jpg，并输入验证码：")


# 登陆统一认证系统
with opener.open(cas_url, urllib.parse.urlencode(data).encode(charset)) as response:
    payload = response.read().decode(charset)

    if '验证码不正确' in payload:
        print('验证码输入错误。')
        exit(0)
    if '账号或密码错误' in payload:
        print('用户名或密码错误。')
        exit(0)


# 登陆教务系统
jwxt_login_url = 'http://jwxt.gzhu.edu.cn/sso/lyiotlogin'
opener.open(jwxt_login_url)


# 打开个人信息查询页面
info_url = 'http://jwxt.gzhu.edu.cn/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default'
with opener.open(info_url) as response:
    payload = response.read().decode(charset)

    # 查询姓名
    match = re.search(r'<label[\s\S]*?姓名[\s\S]*?<p.*?>(?P<name>.*?)</p>', payload)
    if match:
        print('欢迎，' + match.group('name'))


# 构建查询数据
schedule_url = 'http://jwxt.gzhu.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508'
data = {
    'xnm': YEAR,
    'xqm': (3, 12)[SEMESTER == 2]
}


# 查询课表
with opener.open(schedule_url, urllib.parse.urlencode(data).encode(charset)) as response:
    payload = response.read().decode(charset)
    schedule = json.loads(payload)  # 载入Json形式的课表
    courses = schedule['kbList']  # 获取课程列表
    print('查询到' + str(len(courses)) + '个课程：')


# 输出ics
opens_date = datetime.datetime.strptime(DATE_OF_MONDAY_OF_FIRST_WEEK, '%Y/%m/%d')
if opens_date.weekday() != 0:
    raise ValueError(DATE_OF_MONDAY_OF_FIRST_WEEK + '似乎不是周一，是否设置了正确的DATE_OF_MONDAY_OF_FIRST_WEEK？')


file = open(OUTPUT_FILENAME, 'w', encoding='utf-8')


# 写入起始的历法和时区等信息
file.write("""BEGIN:VCALENDAR
VERSION:2.0
METHOD:PUBLISH
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Asia/Shanghai
X-LIC-LOCATION:Asia/Shanghai
BEGIN:STANDARD
TZOFFSETFROM:+0800
TZOFFSETTO:+0800
TZNAME:CST
DTSTART:19700101T000000
END:STANDARD
END:VTIMEZONE
""")


# 每小节上课与下课时间
period = [
    ('0830', '0915'), ('0920', '1005'), ('1025', '1110'), ('1115', '1200'),
    ('1350', '1435'), ('1440', '1525'), ('1545', '1630'), ('1635', '1720'),
    ('1820', '1905'), ('1910', '1955'), ('2000', '2045')
]


# 写入课程信息
for course in courses:
    name = course['kcmc']  # 课程名
    teacher = course['xm']  # 教师
    location = course['cdmc']  # 上课教室
    weekday = int(course['xqj'])  # 星期几，1=星期一
    begin_period, end_period = [int(period) for period in course['jcor'].split('-')]  # 始末节数，1=第1节

    # 始末上课周数，此数据的样式有“1-16周”，“11周”，还有些课程分段上课，如“9周,14周”
    begin_and_end_weeks = course['zcd'].split(',')  # 将分段上课的课程分段处理

    print(f'处理：《{name}》')  # 向控制台输出课程名称

    for begin_and_end_week in begin_and_end_weeks:
        begin_and_end_week = begin_and_end_week.strip('周')  # 去掉结尾的“周”
        # 极少数课程指定单双周上课，如“5-15周(单)”。程序无法正确处理这种格式。
        if begin_and_end_week.endswith('(单)') or begin_and_end_week.endswith('(双)'):
            print(f'\n程序可能没有正确处理课程《{name}》的上课时间“{begin_and_end_week}”，请注意核对。')
            begin_and_end_week = begin_and_end_week.rstrip('周(单)')
            begin_and_end_week = begin_and_end_week.rstrip('周(双)')
        try:
            begin_week, end_week = begin_and_end_week.split('-')  # 处理“1-16周”形式的课程
        except ValueError:
            begin_week = end_week = begin_and_end_week
        begin_week, end_week = int(begin_week), int(end_week)

        start_date = opens_date + datetime.timedelta(weeks=begin_week-1, days=weekday-1)  # 计算课程的起始日期
        repeat_time = end_week - begin_week + 1  # 计算重复次数

        file.write('BEGIN:VEVENT\n')  # ics日程的开始标记
        file.write('SUMMARY:' + name + '\n')  # 课程标题
        file.write('DESCRIPTION:' + teacher + '\n')  # 课程描述
        file.write(  # 课程的开始时间
            'DTSTART;TZID=Asia/Shanghai:' + start_date.strftime('%Y%m%d') + 'T' + period[begin_period - 1][0] + '00\n')
        file.write(  # 课程的结束时间
            'DTEND;TZID=Asia/Shanghai:' + start_date.strftime('%Y%m%d') + 'T' + period[end_period - 1][1] + '00\n')
        file.write('RRULE:FREQ=WEEKLY;COUNT=' + str(repeat_time) + '\n')  # 课程的重复次数
        file.write('LOCATION:' + course['cdmc'] + '\n')  # 上课地点
        file.write('END:VEVENT\n')  # ics日程的结束标记


# 写入结束信息并关闭文件
file.write("END:VCALENDAR\n")
file.close()


print('\n完成')
