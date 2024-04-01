import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout


class RecordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建文本框
        text_edit = QTextEdit(self)
        text_edit.setPlainText("这是一段文字。\n它将在文本框中换行显示。\n你可以根据需要添加更多的文本。")
        text_edit.setReadOnly(True)  # 如果不需要编辑文本，可以设置为只读

        # 创建垂直布局
        vbox = QVBoxLayout()
        vbox.addWidget(text_edit)

        # 设置窗口布局
        self.setLayout(vbox)

        # 设置窗口标题
        self.setWindowTitle('QTextEdit Example')

        # 调整窗口大小以适应文本框
        self.resize(400, 300)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RecordWindow()
    sys.exit(app.exec_())