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


    def drawRuler(self):
        # 设置标尺的单位长度和数量
        unit_length = 20
        num_units = 30
        long_tick_interval = 5  # 长刻度的间隔（每隔几个单位长度）

        # 创建画笔
        pen = QPen(Qt.black, 1)

        # 创建主标尺线
        main_line = QGraphicsLineItem(0, 0, 800, 0)
        main_line.setPen(pen)
        self.scene.addItem(main_line)

        # 在场景中添加标尺刻度线
        for i in range(num_units + 1):  # +1 是为了包括最后一个单位
            if i % long_tick_interval == 0:
                # 长刻度线
                long_tick = QGraphicsLineItem(0, i * unit_length, 10, i * unit_length)
                long_tick.setPen(pen)
                self.scene.addItem(long_tick)
                # 添加数字标签
                text_item = QGraphicsTextItem(str(i * unit_length))  # 创建文本项
                text_item.setFont(QFont("Arial", 8))
                text_item.setPos(20, i * unit_length)  # 设置文本项的位置
                self.scene.addItem(text_item)
            else:
                # 小刻度线
                short_tick = QGraphicsLineItem(0, i * unit_length, 5, i * unit_length)
                short_tick.setPen(pen)
                self.scene.addItem(short_tick)

    def setup_ui(self):
        """
        Set up the main window layout and components.
        """
        self.setWindowTitle("图片信息查看器")
        self.resize(1200, 900)

        self.central_widget = QWidget(self)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Title bar with open, save, and undo buttons
        self.title_bar = QFrame(self.central_widget)
        self.title_bar.setFrameShape(QFrame.StyledPanel)
        self.title_bar.setFrameShadow(QFrame.Raised)
        self.title_layout = QHBoxLayout(self.title_bar)

        self.btn_open = QToolButton(self.title_bar)
        self.btn_save = QToolButton(self.title_bar)
        self.btn_undo = QToolButton(self.title_bar)

        self.title_layout.addWidget(self.btn_open)
        self.title_layout.addWidget(self.btn_save)
        self.title_layout.addWidget(self.btn_undo)

        # Control bar with confirm and cancel buttons
        self.control_bar = QFrame(self.title_bar)
        self.control_layout = QHBoxLayout(self.control_bar)
        self.btn_confirm = QToolButton(self.control_bar)
        self.btn_cancel = QToolButton(self.control_bar)

        self.control_layout.addWidget(self.btn_confirm)
        self.control_layout.addWidget(self.btn_cancel)
        self.title_layout.addWidget(self.control_bar)

        # Add a spacer item to the title layout
        self.title_layout.addItem(QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Image frame with an ImageLabel widget to display images
        self.img_frame = QFrame(self.central_widget)
        self.img_frame.setFrameShape(QFrame.StyledPanel)
        self.img_frame.setFrameShadow(QFrame.Raised)
        self.img_layout = QVBoxLayout(self.img_frame)
        self.img_display = ImageLabel(self.img_frame)
        self.img_info = QFrame(self.img_frame)

        self.hist_win = QFrame()

        self.hist_win_layout = QHBoxLayout()
        self.hist_win.setLayout(self.hist_win_layout)
        self.img_hist_win = HistWidget()
        self.hist_win_layout.addWidget(self.img_display)
        self.hist_win_layout.addWidget(self.img_hist_win)

        self.img_info.setFixedHeight(50)
        self.img_info_layout = QHBoxLayout()
        self.img_info.setLayout(self.img_info_layout)
        self.w_label = QLabel('宽度: xxx 像素')
        self.h_label = QLabel('高度: xxx 像素')
        self.c_label = QLabel('通道数: x ')
        # 创建标签来显示信息
        labels = [
            self.w_label,
            self.h_label,
            self.c_label,
        ]

        # 设置字体样式、大小和颜色
        font = QFont()
        font.setFamily('Arial')  # 设置字体类型，例如 'Arial'
        font.setPointSize(12)  # 设置字体大小，例如 12

        # 应用字体和颜色到每个标签
        for label in labels:
            label.setFont(font)  # 设置字体
            label.setStyleSheet("color: rgb(35, 184, 80);")  # 设置颜色，也可以使用QLabel的setPalette方法

        # 添加标签到布局中
        for label in labels:
            self.img_info_layout.addWidget(label)

        self.img_layout.addWidget(self.hist_win)
        self.img_layout.addWidget(self.img_info)
        self.central_layout.addWidget(self.title_bar)
        self.central_layout.addWidget(self.img_frame)

        # Set button text, icons, styles, and layout styles
        self.set_buttons_text_icons()
        self.set_buttons_styles()
        self.set_layout_styles()

    def set_initial_states(self):
        """
        Set initial states for UI components.
        """
        self.control_bar.setVisible(False)

    def set_buttons_text_icons(self):
        """
        Set button texts, icons, and style for open and save buttons.
        """
        self.btn_open.setText("打开")
        self.btn_open.setIcon(QIcon("./icon/open.png"))
        self.btn_open.setIconSize(QSize(36, 36))
        self.btn_open.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.btn_open.clicked.connect(self.open_img)

        self.btn_save.setText("保存")
        self.btn_save.setIcon(QIcon("./icon/save.png"))
        self.btn_save.setIconSize(QSize(36, 36))
        self.btn_save.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.btn_save.clicked.connect(self.save_img)

    def set_buttons_styles(self):
        """
        Set styles for all buttons and the control bar.
        """
        transparent_button_style = "background: rgba(0, 0, 0, 0); color: rgb(255, 255, 255);"
        gray_button_style = "background: rgb(80, 80, 80); color: rgb(255, 255, 255);"

        buttons = [self.btn_open, self.btn_save, self.btn_undo, self.btn_confirm, self.btn_cancel]
        for btn in buttons:
            btn.setStyleSheet(transparent_button_style)

        self.control_bar.setStyleSheet(gray_button_style)

    def set_layout_styles(self):
        """
        Set styles for central layout and title bar.
        """
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        self.title_bar.setMinimumSize(QSize(0, 55))
        self.title_bar.setMaximumSize(QSize(188888, 55))

        self.control_bar.setMinimumSize(QSize(0, 45))
        self.control_bar.setMaximumSize(QSize(120, 45))

        self.img_frame.setMinimumSize(QSize(100, 0))

        font = QtGui.QFont()
        font.setPointSize(8)
        self.setFont(font)
        self.btn_open.setFont(font)
        self.btn_save.setFont(font)

        self.central_widget.setStyleSheet("background: rgb(252, 255, 255);")
        self.title_bar.setStyleSheet("background: rgb(146, 6, 213);")

    def open_img(self):
        """
        Open an image file using a file dialog and display it.
        """
        img_name, img_type = QFileDialog.getOpenFileName(
            self, "打开图片", "", "*.jpg;*.png;*.jpeg"
        )
        if img_name == "" or img_name is None:
            self.show_warning_message_box("未选择图片")
            return
        self.img_path = img_name
        img = cv2.imread(img_name)
        self.show_image(img)
        self.current_img = img
        self.last_img = self.current_img
        self.original_img = copy.deepcopy(self.current_img)
        self.original_img_path = img_name

    def show_image(self, img, is_grayscale=False):
        """
        Display an image in the ImageLabel widget.

        Args:
            img (numpy.ndarray): The image to display (in BGR or grayscale format).
            is_grayscale (bool, optional): Whether the image is grayscale. Defaults to False.
        """
        if len(img.shape) == 3:  # Color image
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

        height, width, channels = img.shape
        bytes_per_line = channels * width

        if len(img.shape) == 2:  # Grayscale image
            format = QImage.Format_Grayscale8
            bytes_per_line *= 1  # Treat grayscale image as having one channel
        else:  # RGB image
            format = QImage.Format_RGB888

        qimage = QImage(img.data, width, height, bytes_per_line, format)
        pixmap = QPixmap.fromImage(qimage)
        if pixmap.width() > 600 or pixmap.height() > 600:
            pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img_display.setPixmap(pixmap)
        self.img_hist_win=HistWidget(self.img_path)
        self.hist_win_layout.addWidget(self.img_hist_win)
        self.img_display.repaint()
        height, width = img.shape[:2]
        # 获取图片的通道数
        channels = img.shape[2] if len(img.shape) > 2 else 1
        self.w_label.setText(f"宽度: {width} 像素")
        self.h_label.setText(f"高度: {height} 像素")
        self.c_label.setText(f"通道数: {channels}")

    def crop_image(self, src_img, x_start, x_end, y_start, y_end):
        """
        Crop an image.

        Args:
            src_img (numpy.ndarray): The source image to crop.
            x_start (int): Starting x-coordinate of the crop region.
            x_end (int): Ending x-coordinate of the crop region.
            y_start (int): Starting y-coordinate of the crop region.
            y_end (int): Ending y-coordinate of the crop region.

        Returns:
            numpy.ndarray: The cropped image.
        """
        return src_img[y_start:y_end, x_start:x_end]

    def show_warning_message_box(self, msg):
        """
        Show a warning message box with the given message.

        Args:
            msg (str): The message to display.
        """
        QMessageBox.warning(self, "警告", msg, QMessageBox.Ok)

    def show_info_message_box(self, msg):
        """
        Show an information message box with the given message.

        Args:
            msg (str): The message to display.
        """
        QMessageBox.information(self, "提示", msg, QMessageBox.Ok)

    def save_img(self):
        """
        Save the current image to a file using a file dialog.
        """
        if self.current_img is None:
            self.show_warning_message_box("未选择图片")
            return

        ext_name = self.original_img_path[self.original_img_path.rindex("."):]
        img_path, img_type = QFileDialog.getSaveFileName(
            self, "保存图片", self.original_img_path, f"*{ext_name}"
        )
        cv2.imwrite(img_path, self.current_img)

        def doAction(self):
            if self.timer.isActive():
                self.timer.stop()
                self.btn.setText('开始')
            else:
                self.timer.start(100)  # 设置定时器每隔100ms触发一次
                self.btn.setText('停止')

        def updateProgress(self):
            value = self.pbar.value() + 1
            self.pbar.setValue(value)

            if value == 100:
                self.timer.stop()
                self.btn.setText('开始')


    def save_wordcloud_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "保存词云图", "",
                                                  "PNG Files (*.png);;JPG Files (*.jpg);;All Files (*)",
                                                  options=options)
        if fileName:
            self.fig.savefig(fileName, dpi=100, bbox_inches='tight')
            print(f"词云图已保存为 {fileName}")
    def update_wordcloud(self):
        # 使用jieba进行分词
        word_list = jieba.cut(self.text, cut_all=False)
        words = " ".join(word_list)
        # 设置matplotlib使用支持中文的字体
        # 创建WordCloud对象并生成词云图
        print(self.color_code)
        wordcloud = WordCloud(width=800, height=800, background_color=self.color_code if self.color_code is not None else "white", stopwords=None,font_path='msyh.ttc',).generate(
            words)

        # 清除之前的图像并绘制新的词云图
        self.axes.clear()
        self.axes.imshow(wordcloud, interpolation='bilinear')
        self.axes.axis("off")
        self.canvas.draw()

    def openTextFile(self):
        """打开文件选择对话框，选择文本文件"""
        self.file_path, _ = QFileDialog.getOpenFileName(self, "选择文本文件", "", "Text Files (*.txt)")
        if self.file_path:  # 确保文件路径不为空
            with open(self.file_path, 'r', encoding='utf-8') as file:  # 读取文本文件内容
                self.text = file.read()
                # 自动更新词云图
        else:
            print("未选择文件")

    def openStopWordsFile(self):
        """打开文件选择对话框，选择停用词文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择停用词文件", "", "Text Files (*.txt)")
        # 这里添加处理文件路径的逻辑
        with open(file_path, 'r', encoding='utf-8') as f:
            stopwords = set(f.read().splitlines())
        print(stopwords)

    def selectBackgroundColor(self):
        """打开颜色选择器，选择背景颜色"""
        color = QColorDialog.getColor()
        if color.isValid():
            # 更新按钮文本为颜色代码
            self.color_code = color.name()
            button = self.findChild(QPushButton, "选择背景颜色")
            button.setText(self.color_code)
            # 更新按钮文本颜色
            button.setStyleSheet(f"color: {self.color_code};")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = ProgressBarDemo()
    demo.show()
    sys.exit(app.exec_())