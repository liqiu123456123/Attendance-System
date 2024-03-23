from service import hr_service as hr
from entity import organizations as o
from service import recognize_service as rs
import os
import cv2
import numpy as np

PATH = os.getcwd() + "\\data\\"  # 数据文件夹根目录
PIC_PATH = PATH + "faces\\"  # 照片文件夹
DATA_FILE = PATH + "employee_data.txt"  # 员工信息文件
WORK_TIME = PATH + "work_time.txt"  # 上下班时间配置文件
USER_PASSWORD = PATH + "user_password.txt"  # 管理员账号密码文件
RECORD_FILE = PATH + "lock_record.txt"  # 打卡记录文件

IMG_WIDTH = 640  # 图像的统一宽度
IMG_HEIGHT = 480  # 图像的统一高度


# 自检，检查默认文件缺失
def checking_data_files():
    if not os.path.exists(PATH):
        os.mkdir(PATH)
        print("数据文件夹丢失，已重新创建：" + PATH)
    if not os.path.exists(PIC_PATH):
        os.mkdir(PIC_PATH)
        print("照片文件夹丢失，已重新创建：" + PIC_PATH)
    sample1 = PIC_PATH + "1000000000.png"  # 样本1文件路径
    if not os.path.exists(sample1):
        sample_img_1 = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), np.uint8)  # 创建一个空内容图像
        sample_img_1[:, :, 0] = 255  # 改为纯蓝图像
        cv2.imwrite(sample1, sample_img_1)  # 保存此图像
        print("默认样本1已补充")
    sample2 = PIC_PATH + "2000000000.png"  # 样本2文件路径
    if not os.path.exists(sample2):
        sample_img_2 = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), np.uint8)  # 创建一个空内容图像
        sample_img_2[:, :, 1] = 255  # 改为纯蓝图像
        cv2.imwrite(sample2, sample_img_2)  # 保存此图像
        print("默认样本2已补充")
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "a+")  # 附加读写方式打开文件，达到创建空文件目的
        print("员工信息文件丢失，已重新创建：" + DATA_FILE)
    if not os.path.exists(RECORD_FILE):
        open(RECORD_FILE, "a+")  # 附加读写方式打开文件，达到创建空文件目的
        print("打卡记录文件丢失，已重新创建：" + RECORD_FILE)
    if not os.path.exists(USER_PASSWORD):
        file = open(USER_PASSWORD, "a+", encoding="utf-8")  # 附加读写方式打开文件，达到创建空文件目的
        user = dict()
        user["mr"] = "mrsoft"
        file.write(str(user))  # 将默认管理员账号密码写入到文件中
        file.close()  # 关闭文件
        print("管理员账号密码文件丢失，已重新创建：" + RECORD_FILE)
    if not os.path.exists(WORK_TIME):
        file = open(WORK_TIME, "a+", encoding="utf-8")  # 附加读写方式打开文件，达到创建空文件目的
        file.write("09:00:00/17:00:00")  # 将默认时间写入到文件中
        file.close()  # 关闭文件
        print("上下班时间配置文件丢失，已重新创建：" + RECORD_FILE)


# 加载全部员工信息
def load_employee_info():
    max_id = 1  # 最大员工ID
    file = open(DATA_FILE, "r", encoding="utf-8")  # 打开文件，只读
    for line in file.readlines():  # 遍历文件中的行内容
        id, name, code = line.rstrip().split(",")  # 去除换行符，并分割字符串信息
        o.add(o.Employee(id, name, code))  # 组织结构中添加员工信息
        if int(id) > max_id:  # 如果发现某员工的id更大
            max_id = int(id)  # 修改最大ID
    o.MAX_ID = max_id  # 记录最大ID
    file.close()  # 关闭文件


# 加载员工图像
def load_employee_pic():
    photos = list()  # 样本图像列表
    lables = list()  # 标签列表
    pics = os.listdir(PIC_PATH)  # 读取所有照片
    if len(pics) != 0:  # 如果照片文件不是空的
        for file_name in pics:  # 遍历所有图像文件
            code = file_name[0:o.CODE_LEN]  # 截取文件名开头的特征码
            photos.append(cv2.imread(PIC_PATH + file_name, 0))  # 以灰度图像的方式读取样本
            lables.append(int(code))  # 样本的特征码作为训练标签
        rs.train(photos, lables)  # 识别器训练样本
    else:  # 不存在任何照片
        print("Error >> 员工照片文件丢失，请重新启动程序并录入员工信息！")


# 将员工信息持久化
def save_employee_all():
    file = open(DATA_FILE, "w", encoding="utf-8")  # 打开员工信息文件，只写，覆盖
    info = ""  # 待写入的字符串
    for emp in o.EMPLOYEES:  # 遍历所有员工信息
        # 拼接员工信息
        info += str(emp.id) + "," + str(emp.name) + "," + str(emp.code) + "\n"
    file.write(info)  # 将这些员工信息写入到文件中
    file.close()  # 关闭文件


# 删除指定员工的所有照片
def remove_pics(id):
    pics = os.listdir(PIC_PATH)  # 读取所有照片文件
    code = str(hr.get_code_with_id(id))  # 获取该员工的特征码
    for file_name in pics:  # 遍历文件
        if file_name.startswith(code):  # 如果文件名以特征码开头
            os.remove(PIC_PATH + file_name)  # 删除此文件
            print("删除照片：" + file_name)


# 加载所有打卡记录
def load_lock_record():
    file = open(RECORD_FILE, "r", encoding="utf-8")  # 打开打卡记录文件，只读
    text = file.read()  # 读取所有文本
    if len(text) > 0:  # 如果存在文本
        o.LOCK_RECORD = eval(text)  # 将文本转换成打卡记录字典
    file.close()  # 关闭文件


# 将打卡记录持久化
def save_lock_record():
    file = open(RECORD_FILE, "w", encoding="utf-8")  # 打开打卡记录文件，只写，覆盖
    info = str(o.LOCK_RECORD)  # 将打卡记录字典转换成字符串
    file.write(info)  # 将字符串内容写入到文件中
    file.close()  # 关闭文件


# 将上下班时间写到文件中
def save_work_time_config():
    file = open(WORK_TIME, "w", encoding="utf-8")  # 打开打卡记录文件，只写，覆盖
    times = str(o.WORK_TIME) + "/" + str(o.CLOSING_TIME)
    file.write(times)  # 将字符串内容写入到文件中
    file.close()  # 关闭文件


# 加载上下班时间数据
def load_work_time_config():
    file = open(WORK_TIME, "r", encoding="utf-8")  # 打开打卡记录文件，只读
    text = file.read().rstrip()  # 读取所有文本
    times = text.split("/")  # 分割字符串
    o.WORK_TIME = times[0]  # 第一个值是上班时间
    o.CLOSING_TIME = times[1]  # 第二个值是下班时间
    file.close()  # 关闭文件


# 加载管理员账号密码
def load_users():
    file = open(USER_PASSWORD, "r", encoding="utf-8")  # 打开打卡记录文件，只读
    text = file.read()  # 读取所有文本
    if len(text) > 0:  # 如果存在文本
        o.USERS = eval(text)  # 将文本转换成打卡记录字典
    file.close()  # 关闭文件


# 生成csv文件，采用Windows默认的gbk编码
def create_CSV(file_name, text):
    file = open(PATH + file_name + ".csv", "w", encoding="gbk")  # 打开文件，只写，覆盖
    file.write(text)  # 将文本写入文件中
    file.close()  # 关闭文件
    print("已生成文件，请注意查看：" + PATH + file_name + ".csv")
