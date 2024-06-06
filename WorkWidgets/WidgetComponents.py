from PyQt6 import QtWidgets, QtCore, QtGui


class LabelComponent(QtWidgets.QLabel): # 这个类继承自 QtWidgets.QLabel，用于创建一个可以显示文本的标签组件
    def __init__(self, font_size, content):
        # font_size 設置字體大小 ， content 文字內容
        super().__init__()

        self.setWordWrap(True) # 允许标签内的文本进行自动换行
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft) # 设置文本对齐方式为左对齐

        self.setFont(QtGui.QFont("Arial", pointSize=font_size, weight=500)) # 500表示字體粗度
        self.setText(content)

# name右邊的輸入框
class LineEditComponent(QtWidgets.QLineEdit): # 这个类继承自 QtWidgets.QLineEdit，用于创建一个单行文本输入框。
    def __init__(self, default_content="", length=10, width=200, font_size=16):
        # 输入框的默认文本，允许输入的最大字符长度，输入框的最大宽度，输入框文本的字体大小
        super().__init__()
        self.setMaxLength(length) # 设置输入框可以接受的最大字符数
        self.setText(default_content) # 设置输入框的默认文本
        self.setMinimumHeight(30) # 设置输入框的最小高度为 30 像素
        self.setMaximumWidth(width)# 设置输入框的最大宽度
        self.setFont(QtGui.QFont("Arial", font_size)) # 设置输入框的字体样式和大小

# 底下按鈕
class ButtonComponent(QtWidgets.QPushButton): # 这个类继承自 QtWidgets.QPushButton，用于创建一个按钮
    def __init__(self, text, font_size=16): # 按钮上显示的文本 按钮文本的字体大小
        super().__init__()
        self.setText(text) # 设置按钮上显示的文本
        self.setFont(QtGui.QFont("Arial", font_size)) # 设置按钮文本的字体样式和大小
