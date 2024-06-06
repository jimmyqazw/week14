from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent

from PyQt6.QtCore import pyqtSignal, pyqtSlot


class BackgroundWidget(QtWidgets.QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap(self.image_path)
        painter.drawPixmap(self.rect(), pixmap)


class MainWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.setObjectName("main_widget")

        layout = QtWidgets.QVBoxLayout()
        header_label = LabelComponent(24, "Student Management System")
        header_label.setStyleSheet("color: red;")
        function_widget = FunctionWidget(client)
        self.menu_widget = MenuWidget(function_widget, client)
        function_widget.set_menu_widget(self.menu_widget)

        layout.addWidget(header_label)
        layout.addWidget(function_widget)
        layout.addSpacing(10)  # 添加固定空间，将按钮推到底部
        layout.addWidget(self.menu_widget)

        self.setLayout(layout)

        # 设置背景图片
        self.background_widget = BackgroundWidget("WorkWidgets/22.jpg", self)  # 替换为图片的实际路径
        self.background_widget.setLayout(layout)
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.background_widget)
        self.setLayout(main_layout)


class MenuWidget(QtWidgets.QWidget):
    def __init__(self, function_widget, client):
        super().__init__()
        self.setObjectName("menu_widget")
        self.function_widget = function_widget
        self.client = client

        layout = QtWidgets.QHBoxLayout()
        self.show_button = self.create_button("Show all", "#FFA500", "#FF8C00")
        self.add_button = self.create_button("Add student", "#4CAF50", "#45a049")
        self.del_button = self.create_button("Del student", "#FF0000", "#FF3333")
        self.modify_button = self.create_button("Modify student", "#ADD8E6", "#87CEEB")

        self.show_button.clicked.connect(lambda: self.function_widget.update_widget("show"))
        self.add_button.clicked.connect(lambda: self.function_widget.update_widget("add"))
        self.del_button.clicked.connect(self.confirm_delete)
        self.modify_button.clicked.connect(self.modify)

        self.del_button.setEnabled(False)
        self.modify_button.setEnabled(False)

        layout.addWidget(self.show_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.del_button)
        layout.addWidget(self.modify_button)

        layout.setContentsMargins(0, 0, 0, 0)  # 移除边距，使按钮贴紧底部
        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget#menu_widget {
                border: none;
            }
            QPushButton {
                border: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """)

    def create_button(self, text, color, hover_color):
        button = ButtonComponent(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color}; 
                color: white;
                padding: 10px;
                font-size: 16px;
                border: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }}
            QPushButton:disabled {{
                background-color: #A9A9A9;
                color: white;
            }}
            QPushButton:hover:!disabled {{
                background-color: {hover_color};
            }}
        """)
        return button

    def confirm_delete(self):
        selected_students = self.function_widget.get_selected_students()
        if selected_students:
            reply = QtWidgets.QMessageBox.question(
                self, 'Delete Confirmation',
                'Are you sure you want to delete the selected students?',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No
            )
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                self.client.send_command("del", selected_students)
                self.client.wait_response()
                self.function_widget.update_widget("show")  # 更新 show 的介面
                self.del_button.setEnabled(False)
                self.modify_button.setEnabled(False)

    def modify(self):
        selected_students = self.function_widget.get_selected_students()
        if selected_students:
            self.function_widget.set_selected_students(selected_students)
            self.function_widget.update_widget("modify")
            self.del_button.setEnabled(False)
            self.modify_button.setEnabled(False)

    def update_buttons(self, enable):
        self.del_button.setEnabled(enable)
        self.modify_button.setEnabled(enable)
        self.add_button.setEnabled(not enable)  # 当有选中学生时禁用添加按钮

    def initialize_buttons(self):
        self.add_button.setEnabled(True)
        self.del_button.setEnabled(False)
        self.modify_button.setEnabled(False)


class FunctionWidget(QtWidgets.QStackedWidget):
    students_selected = pyqtSignal(list)

    def __init__(self, client):
        super().__init__()
        self.show_widget = ShowStuWidget(client)
        self.add_widget = AddStuWidget(client)
        self.modify_widget = ModifyStuWidget(client)
        self.widget_dict = {
            "show": self.addWidget(self.show_widget),
            "add": self.addWidget(self.add_widget),
            "modify": self.addWidget(self.modify_widget)
        }
        self.menu_widget = None  # 初始化 menu_widget 属性
        self.current_selected_students = []
        self.update_widget("show")

        self.show_widget.students_selected.connect(self.update_selected_students)

    def set_menu_widget(self, menu_widget):
        self.menu_widget = menu_widget

    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        if name == "modify":
            current_widget.set_selected_students(self.current_selected_students)
        if name == "show" and self.menu_widget:
            self.menu_widget.initialize_buttons()

        current_widget.load()

    def get_selected_students(self):
        return self.current_selected_students

    def set_selected_students(self, students):
        self.current_selected_students = students

    @pyqtSlot(list)
    def update_selected_students(self, students):
        self.current_selected_students = students
        self.students_selected.emit(students)  # 发射信号通知菜单更新按钮状态
        if self.menu_widget:
            self.menu_widget.update_buttons(len(students) > 0)