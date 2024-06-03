from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QPropertyAnimation

class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.setFont(QtGui.QFont("Microsoft JhengHei", pointSize=font_size, weight=500))
        self.setText(content)
      
class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", placeholder="", length=10, width=200, font_size=16, numeric_only=False):
        super().__init__()
        self.setMaxLength(length)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setStyleSheet("color:purple;")
        self.setPlaceholderText(placeholder)
        if numeric_only:
            self.setValidator(QtGui.QIntValidator())
       
class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("Microsoft JhengHei", font_size))
        self.default_style = ("font-weight: bold; border:3px solid #9370DB; border-radius: 25px; "
                              "padding: 10px 20px; color:#9f0fff; background-color: #ffffff;")
        self.disabled_style = ("font-weight: bold; border:3px solid #9370DB; border-radius: 25px; "
                               "padding: 10px 20px; color:#9f0fff; background-color: #d3d3d3;")
        self.setStyleSheet(self.default_style)
        
        # Set up the animation
        self.animation = QtCore.QPropertyAnimation(self, b"bg_color")
        self.animation.setDuration(300)

    def enterEvent(self, event):
        if self.isEnabled():
            self.animation.setStartValue(QtGui.QColor("#ffffff"))
            self.animation.setEndValue(QtGui.QColor("#1E90FF"))  # Change to desired hover color
            self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.isEnabled():
            self.animation.setStartValue(QtGui.QColor("#1E90FF"))  # Change to the hover color
            self.animation.setEndValue(QtGui.QColor("#ffffff"))
            self.animation.start()
        super().leaveEvent(event)

    def set_bg_color(self, color):
        if self.isEnabled():
            self.setStyleSheet(self.default_style.split("background-color:")[0] + f"background-color: {color.name()};")

    def get_bg_color(self):
        # This is a placeholder function. It should return the current background color of the button.
        return QtGui.QColor("#ffffff")

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        if enabled:
            self.setStyleSheet(self.default_style)
        else:
            self.setStyleSheet(self.disabled_style)

    bg_color = QtCore.pyqtProperty(QtGui.QColor, fget=get_bg_color, fset=set_bg_color)

class ComboBoxComponent(QtWidgets.QComboBox):
    def __init__(self, text,font_size=16):
        super().__init__()
        self.setStyleSheet("""
            QComboBox {
                border-radius: 10px;  
                padding: 5px;  
                font-family: Microsoft JhengHei;  
                font-size: 18px;  
                color: purple;  
            }
        """)
        

