from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
import json

class DelStuWidget(QtWidgets.QWidget):
    #Initialize ========================================================
    def __init__(self, client):
        super().__init__()
        self.setObjectName("Del_stu_widget")
        self.student_dict = {}
        self.client = client
        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(20, "Delete Student")
        header_label.setStyleSheet("color:darkblue; font-weight: bold;")
        name_content = LabelComponent(16, "Name: ")
        name_content.setStyleSheet("color:#9f0fff; font-weight: bold;")
        self.name_edit = LineEditComponent("Name")
        self.name_edit.mousePressEvent = self.clear_name
        self.name_edit.textChanged.connect(self.enable_query_button)
        self.print_content = LabelComponent(14, "====Information Display====\n1.Enter the name.\n2.Query.\n3.Send.")
        self.print_content.setStyleSheet("""
            QLabel {
                border: 2px solid #9370DB;  /* 邊框顏色 */
                border-radius: 10px;  /* 邊框圓角半徑 */
                padding: 10px;
                color: darkblue;
            }""")
        self.query_button = ButtonComponent("Query")
        self.query_button.setEnabled(False)
        self.query_button.clicked.connect(self.query_action)
        self.send_button = ButtonComponent("Send")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.send_action)

    #Placement for all component ================================================    
        for col in range(6):
            layout.setColumnStretch(col, 1)
        for row in range(6):
            layout.setRowStretch(row, 1)

        layout.addWidget(header_label, 0, 0, 1, 3)
        layout.addWidget(name_content, 1, 0)
        layout.addWidget(self.name_edit, 1, 1, 1, 2)

        layout.addWidget(self.print_content, 2,0,4,4)
        layout.addWidget(self.query_button, 1, 3)
        layout.addWidget(self.send_button, 5,4,1,2) 
        self.setLayout(layout)

    #Component effect and function=================================================================
    def clear_name(self,event):
        self.name_edit.clear()

    def enable_query_button(self,event):
        if self.name_edit.text():
            self.query_button.setEnabled(True)    
    
    def query_action(self,event):
        self.scores = {}
        self.student_dict = {'name' : self.name_edit.text()}
        self.client.send_command("query", self.student_dict)
        data = self.client.wait_response()
        data = json.loads(data)
        if data.get('status') == 'Fail': 
            string = f"The student {self.name_edit.text()} is not found."
            self.send_button.setEnabled(False)
        else: 
            string = f"If you want to delete the information of {self.name_edit.text()} , please press the send button."
            self.send_button.setEnabled(True)

        self.print_content.setText(string)


    def send_action(self,event):
        self.client.send_command("del", self.student_dict)
        data = self.client.wait_response()
        data = json.loads(data)
        if data.get('status') == 'OK':
            string = f"Delete {self.name_edit.text()}'s information successfully."  

        self.print_content.setText(string)
        self.name_edit.setText("Name")
        self.query_button.setEnabled(False)
        self.send_button.setEnabled(False)
        self.name_edit.setEnabled(True)
      