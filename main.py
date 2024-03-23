"""
主入口
"""

from util import camera
from util import public_tools as tool
from service import hr_service as hr

ADMIN_LOGIN = False  # 管理员登录状态


# 管理员登录
def login():
    while True:
        username = input("请输入管理员账号(输入0取消操作)：")
        if username == "0":  # 如果只输入0
            return  # 结束方法
        passowrd = input("请输入管理员密码：")
        print("账号密码", username.strip(), passowrd.strip())
        if hr.valid_user(username.strip(), passowrd.strip()):  # 校验账号密码
            global ADMIN_LOGIN  # 读取全局变量
            ADMIN_LOGIN = True  # 设置为管理员已登录状态
            print(username + "登录成功！请选择重新选择功能菜单")
            break
        else:
            print("账号或密码错误，请重新输入！")
            print("---------------------------")


# 员工管理
def employee_management():
    menu = """+-------------------------------------------------+
|                员工管理功能菜单                 |
+-------------------------------------------------+
  ①录入新员工  ②删除员工  ③返回上级菜单
---------------------------------------------------"""
    while True:
        print(menu)  # 打印菜单
        option = input("请输入菜单序号：")
        if option == "1":  # 如果选择“录入新员工”
            name = str(input("请输入新员工姓名(输入0取消操作)：")).strip()
            if name != "0":  # 只要输入的不是0
                code = hr.add_new_employee(name)  # 人事服务添加新员工，并获得该员工的特征码
                print("请面对摄像头，敲击三次回车键完成拍照！")
                camera.register(code)  # 打开摄像头为员工照相
                print("录入成功！")
                # return  # 退出员工管理功能菜单
        elif option == "2":  # 如果选择“删除员工”
            # show_employee_all()  # 展示员工列表
            print(hr.get_employee_report())  # 打印员工信息报表
            id = int(input("请输入要删除的员工编号(输入0取消操作)："))
            if id > 0:  # 只要输入的不是0
                if hr.check_id(id):  # 若此编号有对应员工
                    verification = tool.randomNumber(4)  # 生成随机4位验证码
                    inputVer = input("[" + str(verification) + "] 请输入验证码：")  # 让用户输入验证码
                    if str(verification) == str(inputVer).strip():  # 如果验证码正确
                        hr.remove_employee(id)  # 人事服务删除该员工
                        print(str(id) + "号员工已删除！")
                    else:  # 无效编号
                        print("验证码有误，操作取消")
                else:
                    print("无此员工，操作取消")
        elif option == "3":  # 如果选择“返回上级菜单”
            return  # 退出员工管理功能菜单
        else:
            print("输入的指令有误，请重新输入！")


# 查看记录
def check_record():
    menu = """+-------------------------------------------------+
|                 查看记录功能菜单                |
+-------------------------------------------------+
  ①查看员工列表  ②查看打卡记录  ③返回上级菜单
---------------------------------------------------"""
    while True:
        print(menu)  # 打印菜单
        option = input("请输入菜单序号：")
        if option == "1":  # 如果选择“查看员工列表”
            print(hr.get_employee_report())  # 打印员工信息报表
        elif option == "2":  # 如果选择“查看打卡记录”
            report = hr.get_record_all()
            print(report)
        elif option == "3":  # 如果选择“返回上级菜单”
            return  # 退出查看记录功能菜单
        else:
            print("输入的指令有误，请重新输入！")


# 报表设置
def report_config():
    menu = """+-------------------------------------------------+
|                报表设置功能菜单                 |
+-------------------------------------------------+
①作息时间设置  ②返回上级菜单
---------------------------------------------------"""
    while True:
        print(menu)  # 打印菜单
        option = input("请输入菜单序号：")
        if option == "1":  # 如果选择“作息时间设置”
            while True:
                work_time = input("请设置上班时间，格式为(08:00:00)：")
                if tool.valid_time(work_time):  # 如果时间格式正确
                    break  # 结束循环
                else:  # 如果时间格式不对
                    print("上班时间格式错误，请重新输入")
            while True:
                close_time = input("请设置下班时间，格式为(23:59:59)：")
                if tool.valid_time(close_time):  # 如果时间格式正确
                    break
                else:  # 如果时间格式不对
                    print("下班时间格式错误，请重新输入")
            hr.save_work_time(work_time, close_time)  # 保存用户设置的上班时间和下班时间
            print("设置完成，上班时间：" + work_time + ",下班时间为：" + close_time)
        elif option == "2":  # 如果选择“返回上级菜单”
            return  # 退出查看记录功能菜单
        else:
            print("输入的指令有误，请重新输入！")


# 考勤报表
def check_report():
    menu = """+-------------------------------------------------+
|                考勤报表功能菜单                 |
+-------------------------------------------------+
   ①日报  ②月报  ③报表设置  ④返回上级菜单
---------------------------------------------------"""
    while True:
        print(menu)  # 打印菜单
        option = input("请输入菜单序号：")
        if option == "1":  # 如果选择“日报”
            while True:
                date = input("输入查询日期，格式为(2008-08-08),输入0则查询今天：")
                if date == "0":  # 如果只输入0
                    hr.get_today_report()  # 打印今天的日报
                    break  # 打印完之后结束循环
                elif tool.valid_date(date):  # 如果输入的日期格式有效
                    hr.get_day_report(date)  # 打印指定日期的日报
                    break  # 打印完之后结束循环
                else:  # 如果输入的日期格式无效
                    print("日期格式有误，请重新输入！")
        elif option == "2":  # 如果选择“月报”
            while True:
                date = input("输入查询月份，格式为(2008-08),输入0则查询上个月：")
                if date == "0":  # 如果只输入0
                    hr.get_pre_month_report()  # 生成上个月的月报
                    break  # 生成完毕之后结束循环
                elif tool.valid_year_month(date):  # 如果输入的月份格式有效
                    hr.get_month_report(date)  # 生成指定月份的月报
                    break  # 生成完毕之后结束循环
                else:
                    print("日期格式有误，请重新输入！")
        elif option == "3":  # 如果选择“报表设置”
            report_config()  # 进入“报表设置”菜单
        elif option == "4":  # 如果选择“返回上级菜单”
            return  # 退出查看记录功能菜单
        else:
            print("输入的指令有误，请重新输入！")


# 人脸打卡
def face_clock():
    print("请正面对准摄像头进行打卡")
    name = camera.clock_in()  # 开启摄像头，返回打卡员工名称
    if name is not None:  # 如果员工名称有效
        hr.add_lock_record(name)  # 保存打卡记录
        print(name + " 打卡成功！")


# 启动方法
def start():
    finish = False  # 程序结束标志
    menu = """
+--------------------------------------------------+
|                   主功能菜单                     |
+--------------------------------------------------+
 ①打卡  ②查看记录  ③员工管理  ④考勤报表  ⑤退出
---------------------------------------------------"""
    while not finish:
        print(menu)  # 打印菜单
        option = input("请输入菜单序号：")
        if option == "1":  # 如果选择“打卡”
            face_clock()  # 启动人脸打卡
        elif option == "2":  # 如果选择“查看记录”
            if ADMIN_LOGIN:  # 如果管理员已登录
                check_record()  # 进入查看记录方法
            else:
                login()  # 先让管理员登录
        elif option == "3":  # 如果选择“员工管理”
            if ADMIN_LOGIN:
                employee_management()  # 进入员工管理方法
            else:
                login()
        elif option == "4":  # 如果选择“考勤报表”
            if ADMIN_LOGIN:
                check_report()  # 进入考勤报表方法
            else:
                login()
        elif option == "5":  # 如果选择“退出”
            finish = True  # 确认结束，循环停止
        else:
            print("输入的指令有误，请重新输入！")
    print("Bye Bye !")


hr.load_emp_data()  # 数据初始化
tital = """
***************************************************
*                MR智能视频打卡系统               *
***************************************************"""
print(tital)  # 打印标题
start()  # 启动程序
