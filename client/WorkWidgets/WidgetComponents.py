from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QPropertyAnimation

class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        font = QtGui.QFont("微軟正黑體", font_size, QtGui.QFont.Weight.Bold)
        self.setFont(font)
        self.setText(content)
        self.setStyleSheet("color: white;")

class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", placeholder="", length=10, width=200, font_size=16, numeric_only=False):
        super().__init__()
        self.setMaxLength(length)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setPlaceholderText(placeholder)
        if numeric_only:
            self.setValidator(QtGui.QIntValidator())
        self.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QLineEdit:hover {
                background-color: white;
            }
            QLineEdit:focus {
                border-color: blue;
            }
            QLineEdit:disabled {
                background-color: #808080;
                color: #d0d0d0;
            }
        """)

class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__(text)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setMinimumHeight(40)
        self._background_position = 100
        self.animation = QPropertyAnimation(self, b"backgroundPosition")
        self.animation.setDuration(300)
        self.animation.setStartValue(100)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
        self.pressed.connect(self.animateButton)
        self.setStyleSheet("""
            QPushButton {
                color: white;
                border: 2px solid #FFA510;
   
            }
            QPushButton:disabled {
                background-color: #505050; /* Dark gray for disabled state */
                border: 2px solid #505050;
                color: #A0A0A0; /* Lighter gray text for disabled state */
            }
        """)

    def animateButton(self):
        if self.animation.state() == QtCore.QAbstractAnimation.State.Stopped:
            self.animation.start()

    def setBackgroundPosition(self, value):
        self._background_position = value / 100.0
        # Ensure the value stays within the 0 to 1 range
        gradient_stop_start = max(0.0, min(1.0, self._background_position))
        gradient_stop_end = max(0.0, min(1.0, self._background_position + 0.1))
        
        self.styleSheet = f"""
            QPushButton {{
                color: white;
                border: 2px solid #FFA510;
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:{gradient_stop_start} #FFA510, stop:{gradient_stop_end} transparent);
            }}
            QPushButton:disabled {{
                background-color: #505050; /* Dark gray for disabled state */
                border: 2px solid #505050;
                color: #A0A0A0; /* Lighter gray text for disabled state */
            }}
        """
        self.setStyleSheet(self.styleSheet)

    def backgroundPosition(self):
        return int(self._background_position * 100)

    backgroundPosition = QtCore.pyqtProperty(int, fget=backgroundPosition, fset=setBackgroundPosition)


class ComboBoxComponent(QtWidgets.QComboBox):
    def __init__(self, font_size=16):
        super().__init__()
        font = QtGui.QFont("微軟正黑體", font_size)
        font.setBold(True)
        self.setFont(font)
        self.setStyleSheet("""
            QComboBox {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QComboBox:hover {
                background-color: white;
            }
            QComboBox:disabled {
                background-color: #808080;
                color: #d0d0d0;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
        """)
