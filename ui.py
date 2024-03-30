import sys
from PyQt5.Qt import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, \
    QPushButton, QLabel, QMessageBox


class ButtonImage(QPushButton):
    def __init__(self, name_label, image_url):
        super().__init__()
        self.resize(300, 300)
        h_box = QVBoxLayout()
        self.name_label = QLabel(name_label, self)
        self.name_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        pixmap = QPixmap(image_url)
        self.image_label.setPixmap(pixmap)
        h_box.addWidget(self.image_label)
        h_box.addWidget(self.name_label)
        self.setLayout(h_box)


class MainWin(QWidget):
    def __init__(self):
        super(MainWin, self).__init__()
        self.resize(400, 300)
        h_layout = QHBoxLayout()
        self.setLayout(h_layout)
        button1 = ButtonImage("人脸打卡", 'icon/人脸打卡.png')
        button2 = ButtonImage("员工管理", 'icon/员工管理.png')
        button3 = ButtonImage("查看报表", 'icon/查看报表.png')
        button4 = ButtonImage("查看记录", 'icon/查看记录.png')
        button5 = ButtonImage("退出", 'icon/退出.png')
        for item in (button1, button2, button3,button4, button5):
            item.setFixedSize(300, 300)
        button1.clicked.connect(self.button1_event)
        button2.clicked.connect(self.button2_event)
        button3.clicked.connect(self.button3_event)
        button4.clicked.connect(self.button4_event)
        button5.clicked.connect(self.button5_event)
        h_layout.addWidget(button1)
        h_layout.addWidget(button2)
        h_layout.addWidget(button3)
        h_layout.addWidget(button4)
        h_layout.addWidget(button5)

    def button1_event(self):
        msg_box = QMessageBox(QMessageBox.Information, '提示', '你点击了button1！')
        msg_box.exec_()

    def button2_event(self):
        msg_box = QMessageBox(QMessageBox.Information, '提示', '你点击了button2！')
        msg_box.exec_()

    def button3_event(self):
        msg_box = QMessageBox(QMessageBox.Information, '提示', '你点击了button3！')
        msg_box.exec_()

    def button4_event(self):
        msg_box = QMessageBox(QMessageBox.Information, '提示', '你点击了button2！')
        msg_box.exec_()

    def button5_event(self):
        msg_box = QMessageBox(QMessageBox.Information, '提示', '你点击了button3！')
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    LW = MainWin()
    LW.show()
    sys.exit(app.exec_())
