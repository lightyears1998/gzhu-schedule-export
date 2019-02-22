from datetime import datetime, timedelta


OUTPUT_FILENAME = 'week-mark.ics'

WEEK_COUNT = 20

FIRST_DATE = '2019/02/24'

file = open(OUTPUT_FILENAME, 'w')

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


first_date = datetime.strptime(FIRST_DATE, '%Y/%m/%d')

for i in range(WEEK_COUNT):
    now_date = first_date + timedelta(weeks=i)

    file.write('BEGIN:VEVENT\n')
    file.write('SUMMARY:' + 'Week ' + str(i+1) + '\n')
    file.write('DTSTART;VALUE=DATE:' + now_date.strftime('%Y%m%d') + '\n')
    file.write('DTEND;VALUE=DATE:' + (now_date + timedelta(days=1)).strftime('%Y%m%d') + '\n')
    file.write('END:VEVENT\n')

file.write("END:VCALENDAR\n")

# DTSTART;VALUE=DATE:20180916
# DTEND;VALUE=DATE:20180917
