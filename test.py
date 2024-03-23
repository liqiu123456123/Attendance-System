from service import hr_service as hr
from util import public_tools as tool

from util import io_tools as io
from entity import organizations as o
import datetime
import calendar
import random

# io.load_lock_record()  # 载入打卡记录
io.load_employee_info()

for emp in o.EMPLOYEES:
    print(emp.name)
    lock_list = []
    today = datetime.date.today()  # 得到今天的日期
    date = datetime.date(today.year, today.month - 1, 1)  # 获得上个月的第一天的日期
    monthRange = calendar.monthrange(date.year, date.month)[1]  # 该月最后一天的天数
    month_first_day = datetime.date(date.year, date.month, 1)  # 该月的第一天
    month_last_day = datetime.date(date.year, date.month, monthRange)  # 该月的最后一天

    index_day = month_first_day  # 从该月第一天开始
    while index_day <= month_last_day:  # 遍历整月
        a = datetime.datetime.strptime(
            str(index_day) + " 08:" + str(random.randint(10, 59)) + ":" + str(random.randint(10, 59)),
            "%Y-%m-%d %H:%M:%S")
        b = datetime.datetime.strptime(
            str(index_day) + " 17:" + str(random.randint(10, 59)) + ":" + str(random.randint(10, 59)),
            "%Y-%m-%d %H:%M:%S")
        lock_list.append(str(a))
        lock_list.append(str(b))
        index_day = index_day + datetime.timedelta(days=1)  # 日期递增
    o.LOCK_RECORD[emp.name] = lock_list

io.save_lock_record()
