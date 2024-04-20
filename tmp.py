import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTimeEdit,QHBoxLayout


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimeSetter()
    ex.show()
    sys.exit(app.exec_())