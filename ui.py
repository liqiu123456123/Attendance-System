import sys
from PyQt5.Qt import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, \
    QLabel, QMessageBox, QTextEdit,QApplication, QWidget, QPushButton, QVBoxLayout, QDialog, QLineEdit, QDialogButtonBox,QTimeEdit

from util import camera
from util import public_tools as tool
from service import hr_service as hr

ADMIN_LOGIN = False  # 管理员登录状态




class TimeSetter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个垂直布局
        layout = QVBoxLayout()
        layout_1 = QHBoxLayout()
        layout_2 = QHBoxLayout()
        # 创建一个标签
        label = QLabel('上班时间：')
        label_1 = QLabel('下班时间：')

        # 创建一个时间编辑控件
        time_edit = QTimeEdit()
        time_edit.setDisplayFormat('HH:mm')  # 设置时间格式

        time_edit_1 = QTimeEdit()
        time_edit_1.setDisplayFormat('HH:mm')  # 设置时间格式


        # 将标签和时间编辑控件添加到布局中
        layout_1.addWidget(label)
        layout_1.addWidget(time_edit)

        layout_2.addWidget(label_1)
        layout_2.addWidget(time_edit_1)
        layout.addLayout(layout_1)
        layout.addLayout(layout_2)
        # 设置窗口的布局
        self.setLayout(layout)

        # 设置窗口的标题和大小
        self.setWindowTitle('上下班时间设置')
        self.setGeometry(300, 300, 250, 150)

class DayReportDialog(QDialog):
    def __init__(self, parent=None):
        super(DayReportDialog, self).__init__(parent)
        self.resize(300, 200)
        self.setWindowTitle('输入查询日期')

        # 创建标签
        self.label = QLabel('输入查询日期，格式为(2008-08-08)，输入0则查询今天', self)

        self.line_edit = QLineEdit(self)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)

        layout = QVBoxLayout()
        # 先添加标签，再添加文本框和按钮
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def text_value(self):
        return self.line_edit.text()

class PopupDialog(QDialog):
    def __init__(self, parent=None):
        super(PopupDialog, self).__init__(parent)
        self.resize(300, 200)
        self.setWindowTitle('输入新员工的姓名')
        self.line_edit = QLineEdit(self)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        layout = QVBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def text_value(self):
        return self.line_edit.text()

class RemoveDialog(QDialog):
    def __init__(self, parent=None):
        super(RemoveDialog, self).__init__(parent)
        self.resize(300, 200)
        self.setWindowTitle('输出要删除员工的编号')
        self.line_edit = QLineEdit(self)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        layout = QVBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def text_value(self):
        return self.line_edit.text()

class ButtonImage(QPushButton):
    def __init__(self, name_label, image_url):
        super().__init__()
        # 居中显示窗口

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

class RemoveRecordWindow(QWidget):
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
class RecordWindow(QWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.initUI()

    def initUI(self):
        # 创建文本框
        text_edit = QTextEdit(self)
        text_edit.setPlainText(self.text)
        # text_edit.setReadOnly(True)  # 如果不需要编辑文本，可以设置为只读
        # 创建垂直布局
        vbox = QVBoxLayout()
        vbox.addWidget(text_edit)
        # 设置窗口布局
        self.setLayout(vbox)
        # 设置窗口标题
        self.setWindowTitle('QTextEdit')
        # 调整窗口大小以适应文本框
        self.resize(400, 300)

class StaffWin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CheckRecordsWin')
        self.resize(400, 300)
        # 创建垂直布局
        layout = QHBoxLayout()
        # 创建两个ButtonImage实例
        button_image1 = ButtonImage('新增员工', 'icon/新增员工.png')
        button_image2 = ButtonImage('删除员工', 'icon/删除员工.png')
        # 将ButtonImage实例添加到布局中
        button_image1.setFixedSize(300, 300)
        button_image2.setFixedSize(300, 300)
        layout.addWidget(button_image1)
        layout.addWidget(button_image2)
        button_image1.clicked.connect(self.add_staff)
        button_image2.clicked.connect(self.remove_staff)
        # 设置主窗口的布局
        self.setLayout(layout)

    def add_staff(self):
        dialog = PopupDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            text_value = dialog.text_value()
            self.handle_text(text_value)
    def handle_text(self, text):
        self.add_name = text
        code = hr.add_new_employee(self.add_name)
        self.show_message_box("请面对摄像头，敲击三次回车键完成拍照！")
        camera.register(code)  # 打开摄像头为员工照相
    def remove_staff(self):
        dialog = RemoveDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            id_value = int(dialog.text_value())
            if id_value > 0:  # 只要输入的不是0
                if hr.check_id(id_value):  # 若此编号有对应员工
                    hr.remove_employee(id_value)  # 人事服务删除该员工
                    self.show_message_box(str(id_value) + "号员工已删除！")
                else:
                    self.show_message_box("无此员工，操作取消")


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
class ReportWin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CheckRecordsWin')
        self.resize(400, 300)
        # 创建垂直布局
        layout = QHBoxLayout()
        # 创建两个ButtonImage实例
        button_image1 = ButtonImage('日报', 'icon/日报.png')
        button_image2 = ButtonImage('月报', 'icon/月报.png')
        button_image3 = ButtonImage('报表设置', 'icon/报表设置.png')
        # 将ButtonImage实例添加到布局中
        button_image1.setFixedSize(300, 300)
        button_image2.setFixedSize(300, 300)
        button_image3.setFixedSize(300, 300)
        layout.addWidget(button_image1)
        layout.addWidget(button_image2)
        layout.addWidget(button_image3)
        button_image1.clicked.connect(self.get_day_report)
        button_image2.clicked.connect(self.get_month_report)
        button_image3.clicked.connect(self.report_set)
        # 设置主窗口的布局
        self.setLayout(layout)

    def get_day_report(self):
        dialog = DayReportDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            text_value = dialog.text_value()
            if text_value == "0":  # 如果只输入0
                day_report = hr.get_today_report()  # 打印今天的日报
                self.text_win = RecordWindow(day_report)
                self.text_win.show()
            elif tool.valid_date(text_value):  # 如果输入的日期格式有效
                hr.get_day_report(text_value)
            else:  # 如果输入的日期格式无效
                print("日期格式有误，请重新输入！")
            # 打印指定日期的日报
    def get_month_report(self):
        pass

    def report_set(self):
        self.report_set = TimeSetter()
        self.report_set.show()
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
        print_str = hr.get_employee_report()  # 打印员工信息报表
        print_str = '\n'.join(print_str)
        self.text_win = RecordWindow(print_str)
        self.text_win.show()

    def get_record(self):
        print_str = hr.get_record_all()
        print_str = '\n'.join(print_str)
        self.text_win = RecordWindow(print_str)
        self.text_win.show()


class MainWin(QWidget):
    def __init__(self):
        super(MainWin, self).__init__()

        # 创建一个 QIcon 对象，加载图标文件
        icon = QIcon("icon.ico")

        # 使用 setWindowIcon() 方法设置窗体图标
        self.setWindowIcon(icon)
        self.resize(900, 600)
        self.move(100,300)
        self.setWindowTitle("基于Python的人脸识别考勤系统")
        self.h_layout = QHBoxLayout(self)  # 直接设置给self，避免额外的变量
        self.h_layout.setContentsMargins(100, 0, 100, 0)
        # 按钮的标签和图标路径
        buttons_labels = ["人脸打卡", "员工管理", "考勤报表", "查看记录", "退出"]
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
            self.staff = StaffWin()
            self.staff.show()
        elif msg == "考勤报表":
            self.report_win = ReportWin()
            self.report_win.show()
        elif msg == "查看记录":
            self.check_record = CheckRecordsWin()
            self.check_record.show()
        elif msg == "退出":
            self.close()

    # 处理员工管理的逻辑


if __name__ == "__main__":
    app = QApplication(sys.argv)
    LW = MainWin()
    LW.show()
    sys.exit(app.exec_())
