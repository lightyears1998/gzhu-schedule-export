#!python3

import re
from datetime import datetime, timedelta


"""week-mark.py

自FIRST_DATE起，连续创建WEEK_COUNT个全天日程事件，
日程的标题分别设置为“Week 1, 2, ...”。

"""


""" ⬇⬇⬇ 在下方输入信息 ⬇⬇⬇ """

# 第一次创建日程的日期
FIRST_DATE = input("创建标记的起始日期（格式：2020/3/1）：").strip() or '2020/3/1'

# 每隔七天创建日程的个数
WEEK_COUNT = int(input('需要创建多少个星期标记？（默认：20）：') or '20')

OUTPUT_FILENAME = 'week-mark.ics'

""" ⬆⬆⬆ 信息输入完成 ⬆⬆⬆ """

# 检查信息是否完整
if not re.match('\d{4}/\d{1,2}/\d{1,2}', FIRST_DATE):
	print('您输入的日期格式似乎有误？请您检查后重新输入。')
	exit()
if WEEK_COUNT <= 0:
    print("创建星期标记的数量似乎有误？请您检查后重新输入。")

# 确认已经输入的信息
print('将自' + FIRST_DATE + '始每隔1周创建Week X全天日程，共计创建' + str(WEEK_COUNT) + '次')
print('输出文件名为' + OUTPUT_FILENAME)
input('请按回车键确认上述信息：')


# 打开输出文件
file = open(OUTPUT_FILENAME, 'w', encoding='utf-8')

# 写入起始信息
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


# 计算开始日期
first_date = datetime.strptime(FIRST_DATE, '%Y/%m/%d')


# 创建WEEK_COUNT个日程
for i in range(WEEK_COUNT):
    now_date = first_date + timedelta(weeks=i)

    file.write('BEGIN:VEVENT\n')  # 日程开始标记
    file.write('SUMMARY:' + 'Week ' + str(i+1) + '\n')  # 日程标题
    file.write('DTSTART;VALUE=DATE:' + now_date.strftime('%Y%m%d') + '\n')  # 日程开始日期
    file.write(
        'DTEND;VALUE=DATE:' + (now_date + timedelta(days=1)).strftime('%Y%m%d') + '\n')  # 日程结束日期，全天事件的结束日期在开始日期的后一天
    file.write('END:VEVENT\n')  # 日程结束标记

# 写入结束信息并关闭文件
file.write("END:VCALENDAR\n")
file.close()

print('完成')
