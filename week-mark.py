#!python3

from datetime import datetime, timedelta


"""week-mark.py

自FIRST_DATE起，连续创建WEEK_COUNT个全天日程事件，
日程的标题分别设置为“Week 1, 2, ...”。

"""


""" 在下方输入信息 """

FIRST_DATE = '2019/02/24'

WEEK_COUNT = 20

OUTPUT_FILENAME = 'week-mark.ics'

""" 信息输入完成 """


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
