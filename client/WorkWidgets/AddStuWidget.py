from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from PyQt6.QtWidgets import  QMessageBox
import json

class AddStuWidget(QtWidgets.QWidget):
    # Initialize ========================================================
    def __init__(self, client):
        super().__init__()
        self.setObjectName("add_stu_widget")
        self.student_dict = {}
        self.client = client
        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(20, "Add Student")
        header_label.setStyleSheet("color:darkblue; font-weight: bold;")

        name_content = LabelComponent(16, "Name: ")
        name_content.setStyleSheet("color:#9f0fff;  font-weight: bold;")
        self.name_edit = LineEditComponent("Name")
        self.name_edit.mousePressEvent = self.clear_name
        self.name_edit.textChanged.connect(self.enable_query_button)

        subject_content = LabelComponent(16, "Subject: ")
        subject_content.setStyleSheet("color:#9f0fff; font-weight: bold;")
        self.subject_edit = LineEditComponent("Subject")
        self.subject_edit.setEnabled(False)
        self.subject_edit.mousePressEvent = self.clear_subject

        score_content = LabelComponent(16, "Score: ")
        score_content.setStyleSheet("color:#9f0fff; font-weight: bold;")
        self.score_edit = LineEditComponent("Score")
        self.score_edit.setEnabled(False)
        self.score_edit.mousePressEvent = self.clear_score
        self.score_edit.textChanged.connect(self.enable_add_button)

        # Set input validator for score_edit to ensure only digits are entered
        self.score_edit.setValidator(QtGui.QIntValidator())

        self.print_content = LabelComponent(13, "====Information Display====\n1.Enter the Name and query.\n2.Enter subject and score.\n3.Add and send.")
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

        self.add_button = ButtonComponent("Add")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self.add_action)

        self.send_button = ButtonComponent("Send")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.send_action)

        # Placement for all component ================================================
        for col in range(6):
            layout.setColumnStretch(col, 1)
        for row in range(6):
            layout.setRowStretch(row, 1)

        layout.addWidget(header_label, 0, 0, 1, 3)
        layout.addWidget(name_content, 1, 0)
        layout.addWidget(subject_content, 2, 0)
        layout.addWidget(score_content, 3, 0)
        layout.addWidget(self.name_edit, 1, 1, 1, 2)
        layout.addWidget(self.subject_edit, 2, 1, 1, 2)
        layout.addWidget(self.score_edit, 3, 1, 1, 2)
        layout.addWidget(self.print_content, 4, 0, 2, 4)
        layout.addWidget(self.query_button, 1, 3)
        layout.addWidget(self.add_button, 3, 3)
        layout.addWidget(self.send_button, 5, 4, 1, 2)
        self.setLayout(layout)

    def load(self):
        pass

    # Component effect and function=================================================================
    def clear_name(self, event):
        self.name_edit.clear()

    def clear_subject(self, event):
        self.subject_edit.clear()

    def clear_score(self, event):
        self.score_edit.clear()

    def query_action(self, event):
        self.scores = {}
        self.student_dict = {'name': self.name_edit.text()}
        self.client.send_command("query", self.student_dict)
        data = self.client.wait_response()
        data = json.loads(data)
        if data.get('status') == 'Fail':
            string = f"Please enter subject for student '{self.name_edit.text()}'."
            self.query_button.setEnabled(False)
            self.subject_edit.setEnabled(True)
            self.score_edit.setEnabled(True)
        else:
            string = f"The name '{self.name_edit.text()}' already exists."

        self.print_content.setText(string)

    def send_action(self, event):
        self.client.send_command("add", self.student_dict)
        data = self.client.wait_response()
        data = json.loads(data)
        if data.get('status') == 'OK':
            string = f"Add {self.student_dict} successfully."
        else:
            string = f"Add {self.student_dict} fail."

        self.print_content.setText(string)
        self.name_edit.setText("Name")
        self.subject_edit.setText("Subject")
        self.score_edit.setText("Score")
        self.subject_edit.setEnabled(False)
        self.score_edit.setEnabled(False)
        self.query_button.setEnabled(False)
        self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)
        self.name_edit.setEnabled(True)

    def add_action(self, event):
        self.scores[self.subject_edit.text()] = self.score_edit.text()
        self.student_dict['scores'] = self.scores
        string = f"Student {self.name_edit.text()}'s subject '{self.subject_edit.text()}' with score '{self.score_edit.text()}' added."
        self.print_content.setText(string)
        self.send_button.setEnabled(True)

    def enable_query_button(self, event):
        if self.name_edit.text():
            self.query_button.setEnabled(True)

    def enable_add_button(self, event):
        if self.subject_edit.text() and self.score_edit.text() and self.score_edit.text().isdigit():
            self.add_button.setEnabled(True)

