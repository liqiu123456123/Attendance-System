import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDialog, QLineEdit, QDialogButtonBox


class PopupDialog(QDialog):
    def __init__(self, parent=None):
        super(PopupDialog, self).__init__(parent)
        self.setWindowTitle('输入对话框')
        self.line_edit = QLineEdit(self)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        layout = QVBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def text_value(self):
        return self.line_edit.text()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.start_button = QPushButton('开始', self)
        self.start_button.clicked.connect(self.show_popup)
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        self.setLayout(layout)
        self.setWindowTitle('主窗体')
        self.show()

    def show_popup(self):
        dialog = PopupDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            text_value = dialog.text_value()
            self.handle_text(text_value)

    def handle_text(self, text):
        print(f'接收到的文本: {text}')
        # 在这里处理接收到的文本，例如更新UI或执行其他操作。


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())