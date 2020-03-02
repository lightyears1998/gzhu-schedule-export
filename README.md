# gzhu-schedule-export

这是一个将广州大学教务系统课程表导出为iCal格式文件（.ics）的小工具。iCal文件可由Google Calendar、MS Outlook等日历程序导入。

![效果预览](screenshot.png)

## 使用方式

请使用Python3.6或以上版本直接运行脚本，无需安装其他依赖。
脚本运行时会提示您输入账号、密码或验证码等信息，您也可直接修改脚本填入信息。

重要提示：为避免程序中潜在bug的影响，建议先将日程导入到临时日历，确认无误后再导入到主日历。

* **导出课程表为日历日程** 使用`schedule.py`。
* **创建Week 1 ~ Week N的标记** 使用`week-mark.py`。

## What's more

* @ZhenShaw的[广大课表项目](https://github.com/ZhenShaw/GZHU-ClassTable)
