from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QFont, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.WidgetComponents import LabelComponent, ComboBoxComponent, ButtonComponent
import os

class MainWidget(QtWidgets.QWidget):
    # Initialize ========================================================
    def __init__(self, client):
        super().__init__()
        self.setObjectName("main_widget")
        self.client = client
        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(20, "Student Management System")
        header_label.setStyleSheet("color:darkblue; font-weight: bold;")
        self.function_widget = FunctionWidget(client)
        self.menu_widget = MenuWidget(self.function_widget.update_widget)

        # Placement of menu area /function area/title =========================
        for col in range(6):
            layout.setColumnStretch(col, 1)
        for row in range(6):
            layout.setRowStretch(row, 1)

        layout.addWidget(header_label, 0, 0, 1, 6)
        layout.addWidget(self.menu_widget, 1, 0, 2, 1)
        layout.addWidget(self.function_widget, 1, 1, 5, 5)
        self.setLayout(layout)

    # Add background into GUI ================================================================
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if(os.path.isfile("./Image/image.jpg")):
            pixmap = QtGui.QPixmap("./Image/image.jpg")
        else:
            pixmap = QtGui.QPixmap("./client/Image/image.jpg")
        painter.drawPixmap(self.rect(), pixmap)

# MenuWidget definition=======================================================
class MenuWidget(QtWidgets.QWidget):
    # Initialize ========================================================
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback
        layout = QtWidgets.QVBoxLayout()
        self.function_combobox = ComboBoxComponent("Select function")
        self.function_combobox.addItem("Add student", "add")
        self.function_combobox.addItem("Show student", "show")
        self.function_combobox.addItem("Modify student", "modify")
        self.function_combobox.addItem("Delete student", "del")
        # Connect the combobox selection change to update the widget
        self.function_combobox.currentIndexChanged.connect(self.on_combobox_changed)
        layout.addWidget(self.function_combobox, stretch=1)
        self.setLayout(layout)

    def on_combobox_changed(self):
        selected_function = self.function_combobox.currentData()
        self.update_widget_callback(selected_function)



# FunctionWidget definition===================================================
class FunctionWidget(QtWidgets.QStackedWidget):
    # Initialize ========================================================
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.add_widget = AddStuWidget(client)
        self.show_widget = ShowStuWidget(client)
        self.modify_widget = ModifyStuWidget(client)
        self.delete_widget = DelStuWidget(client)
        self.widget_dict = {
            "add": self.addWidget(self.add_widget),
            "show": self.addWidget(self.show_widget),
            "modify": self.addWidget(self.modify_widget),
            "del": self.addWidget(self.delete_widget)
        }
        self.update_widget("add")

    # Based on index of ComboBox to update widget =========================
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        if hasattr(current_widget, 'initialize'):
            current_widget.initialize()
        if hasattr(current_widget, 'load'):
            current_widget.load()
