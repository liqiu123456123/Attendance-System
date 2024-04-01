import sys
from PyQt5.Qt import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, \
    QPushButton, QLabel, QMessageBox,QTextEdit

from util import camera
from util import public_tools as tool
from service import hr_service as hr

ADMIN_LOGIN = False  # 管理员登录状态


class ButtonImage(QPushButton):
    def __init__(self, name_label, image_url):
        super().__init__()
        self.initUI(name_label, image_url)

    def initUI(self, name_label, image_url):
        self.resize(300, 300)
        hr.load_emp_data()  # 数据初始化
        # 使用内部布局
        self.layout = QVBoxLayout(self)
        # 设置标签居中
        alignment = Qt.AlignHCenter | Qt.AlignVCenter
        # 创建并设置名称标签
        self.name_label = QLabel(name_label)
        self.name_label.setAlignment(alignment)
        # 创建并设置图片标签
        self.image_label = QLabel()
        pixmap = QPixmap(image_url)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(alignment)
        # 将标签添加到布局中
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.name_label)

class RecordWindow(QWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.initUI()

    def initUI(self):
        # 创建文本框
        text_edit = QTextEdit(self)
        text_edit.setPlainText(self.text)
        text_edit.setReadOnly(True)  # 如果不需要编辑文本，可以设置为只读
        # 创建垂直布局
        vbox = QVBoxLayout()
        vbox.addWidget(text_edit)
        # 设置窗口布局
        self.setLayout(vbox)
        # 设置窗口标题
        self.setWindowTitle('QTextEdit')
        # 调整窗口大小以适应文本框
        self.resize(400, 300)
class CheckRecordsWin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CheckRecordsWin')
        self.resize(400, 300)
        # 创建垂直布局
        layout = QHBoxLayout()
        # 创建两个ButtonImage实例
        button_image1 = ButtonImage('员工列表', 'icon/员工列表.png')
        button_image2 = ButtonImage('打卡记录', 'icon/打卡记录.png')
        # 将ButtonImage实例添加到布局中
        button_image1.setFixedSize(300, 300)
        button_image2.setFixedSize(300, 300)
        layout.addWidget(button_image1)
        layout.addWidget(button_image2)
        button_image1.clicked.connect(self.get_employee)
        button_image2.clicked.connect(self.get_record)
        # 设置主窗口的布局
        self.setLayout(layout)


    def get_employee(self):
        print_str = hr.get_employee_report()# 打印员工信息报表
        print_str = '\n'.join(print_str)
        self.text_win = RecordWindow(print_str)
        self.text_win.show()


    def get_record(self):
        report = hr.get_record_all()
        print(report)

class MainWin(QWidget):
    def __init__(self):
        super(MainWin, self).__init__()
        self.resize(900, 600)
        self.h_layout = QHBoxLayout(self)  # 直接设置给self，避免额外的变量
        self.h_layout.setContentsMargins(100, 0, 100, 0)
        # 按钮的标签和图标路径
        buttons_labels = ["人脸打卡", "员工管理", "查看报表", "查看记录", "退出"]
        buttons_icons = ['icon/人脸打卡.png', 'icon/员工管理.png', 'icon/查看报表.png', 'icon/查看记录.png',
                         'icon/退出.png']

        # 创建按钮并添加到布局中
        for label, icon in zip(buttons_labels, buttons_icons):
            button = ButtonImage(label, icon)
            button.setFixedSize(300, 300)
            button.clicked.connect(lambda checked, msg=label: self.button_clicked(msg))  # 使用lambda表达式传递不同的消息
            self.h_layout.addWidget(button)

    def show_message_box(self, message):
        """
        显示一个带有指定消息的提示窗口。

        参数:
            message (str): 要在提示窗口中显示的消息文本。
        """
        # 创建一个QMessageBox对象
        msg_box = QMessageBox()
        # 设置消息框的类型为Information
        msg_box.setIcon(QMessageBox.Information)
        # 设置标题和消息文本
        msg_box.setWindowTitle('提示')
        msg_box.setText(message)

        # 显示消息框并等待用户响应
        msg_box.exec_()

    def face_clock(self):
        name = camera.clock_in()  # 开启摄像头，返回打卡员工名称
        if name is not None:  # 如果员工名称有效
            hr.add_lock_record(name)  # 保存打卡记录
            self.show_message_box(name + " 打卡成功！")

    def button_clicked(self, msg):
        # 通用的事件处理方法
        if msg == "人脸打卡":
            self.face_clock()
        # 处理人脸打卡的逻辑
        elif msg == "员工管理":
            pass
        elif msg == "查看报表":
            print(222222222222222)
        elif msg == "查看记录":
            self.check_record = CheckRecordsWin()
            self.check_record.show()
        elif msg == "退出":
            print(222222222222222)
    # 处理员工管理的逻辑


if __name__ == "__main__":
    app = QApplication(sys.argv)
    LW = MainWin()
    LW.show()
    sys.exit(app.exec_())
