from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QMessageBox
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WorkWidgets.MainWidget import MainWidget
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, message="sipPyTypeDict")
import os

class EntryWidget(QtWidgets.QWidget):
    #Initialize ========================================================
    def __init__(self, client, parent=None):
        super().__init__(parent)
        self.client = client
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QGridLayout(self)
 
        header_label = LabelComponent(20, "Student Management System")
        header_label.setStyleSheet("color:white; font-weight: bold;")

        name_content = LabelComponent(18, "Name: ")
        name_content.setStyleSheet("color:white;  font-weight: bold;")
        self.name_edit = LineEditComponent("Name")
        self.name_edit.mousePressEvent = self.clear_name


        ID_content = LabelComponent(18, "Staff ID: ")
        ID_content.setStyleSheet("color:white;  font-weight: bold;")
        self.ID_edit = LineEditComponent("ID")
        self.ID_edit.mousePressEvent = self.clear_ID
    

        self.enter_button = ButtonComponent("Enter")
        #self.enter_button.setStyleSheet("font-weight: bold; border:3px solid #9370DB; border-radius: 25px; padding: 10px 20px; color:white;")
        self.enter_button.clicked.connect(self.enter_action)

        self.close_button = ButtonComponent("Close")
        #self.close_button.setStyleSheet("font-weight: bold; border:3px solid #9370DB; border-radius: 25px; padding: 10px 20px; color:white;")
        self.close_button.clicked.connect(self.close_action)

    #Placement for all component ================================================    
        for col in range(6):
            layout.setColumnStretch(col, 1)
        for row in range(6):
            layout.setRowStretch(row, 1)

        layout.addWidget(header_label, 1, 1, 1, 6)
        layout.addWidget(name_content, 2, 1, 1, 2)
        layout.addWidget(self.name_edit, 2, 2, 1, 4)
        layout.addWidget(ID_content, 4, 1, 1, 3)
        layout.addWidget(self.ID_edit, 4, 2, 1, 4)
        layout.addWidget(self.enter_button, 2, 4, 1, 1)
        layout.addWidget(self.close_button, 4, 4, 1, 1)

    #Component effect and function=================================================================
    def enter_action(self):
        ID_text = self.ID_edit.text()
        name_text = self.name_edit.text()

        if not ID_text or not name_text:
            QMessageBox.warning(self, "Input Error", "Both ID and Name fields must be filled.")
            return

        ID_is_nine_digits = ID_text.isdigit() and len(ID_text) == 9
        name_is_not_digits = not any(char.isdigit() for char in name_text)

        if not ID_is_nine_digits:
            QMessageBox.warning(self, "Invalid ID", "ID should be a student ID (9 digits).")
        elif not name_is_not_digits:
            QMessageBox.warning(self, "Invalid Name", "Name should be Chinese or English.")
        else:
            main_widget = MainWidget(self.client)
            self.parent().addWidget(main_widget)
            self.parent().setCurrentWidget(main_widget)

    def clear_name(self,event):
        self.name_edit.clear()

    def clear_ID(self,event):
        self.ID_edit.clear()

        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if(os.path.isfile("./Image/image2.jpg")):
            pixmap = QtGui.QPixmap("./Image/image2.jpg")
        else:
            pixmap = QtGui.QPixmap("./client/Image/image2.jpg")
        painter.drawPixmap(self.rect(), pixmap)

    def close_action(selft):
        QApplication.instance().quit()
