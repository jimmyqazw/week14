from PyQt6 import QtWidgets
from PyQt6.QtGui import QIntValidator
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
import json
from AddStu import AddStu
from query import Query

class AddStuWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.setObjectName("add_stu_widget")
        self.client = client

        # 儲存當下學生的成績
        self.student_dict = {}

        self.add_stu = AddStu(client)
        self.query = Query(client)
        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(18, "Add Student")

        name_content = LabelComponent(16, "Name: ")
        self.name_edit = LineEditComponent("Name")
        self.name_edit.mousePressEvent = self.clear_name
        self.name_edit.textChanged.connect(self.enable_query_button)

        subject_content = LabelComponent(16, "Subject: ")
        self.subject_edit = LineEditComponent("Subject")
        self.subject_edit.setEnabled(False)
        self.subject_edit.mousePressEvent = self.clear_subject
        self.subject_edit.textChanged.connect(self.enable_add_button)
        score_content = LabelComponent(16, "Score: ")
        self.score_edit = LineEditComponent()
        self.score_edit.setEnabled(False)
        self.score_edit.textChanged.connect(self.enable_add_button)
        self.score_edit.setValidator(QIntValidator())

        self.print_content = LabelComponent(15, "")
        self.print_content.setStyleSheet("color: red;")

        self.query_button = ButtonComponent("Query")
        self.query_button.setEnabled(False)
        self.query_button.clicked.connect(lambda: self.query_action(self.print_content))

        self.add_button = ButtonComponent("Add")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(lambda: self.add_action(self.print_content))

        self.send_button = ButtonComponent("Send")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(lambda: self.send_action(self.print_content))

        for col in range(6):
            layout.setColumnStretch(col, 1)
        for row in range(6):
            layout.setRowStretch(row, 1)
        layout.addWidget(header_label, 0, 0, 1, 3)
        layout.addWidget(name_content, 1, 0)
        layout.addWidget(subject_content, 3, 0)
        layout.addWidget(score_content, 5, 0)
        layout.addWidget(self.name_edit, 1, 1, 1, 2)
        layout.addWidget(self.subject_edit, 3, 1, 1, 2)
        layout.addWidget(self.score_edit, 5, 1, 1, 2)
        layout.addWidget(self.print_content, 0, 4, 5, 2)
        layout.addWidget(self.query_button, 1, 3)
        layout.addWidget(self.add_button, 5, 3)
        layout.addWidget(self.send_button, 6, 4, 1, 2)
        self.setLayout(layout)

    def initialize(self):
        self.student_dict = {}
        self.name_edit.setText("Name")
        self.subject_edit.setText("Subject")
        self.score_edit.setText("")
        self.subject_edit.setEnabled(False)
        self.score_edit.setEnabled(False)
        self.query_button.setEnabled(False)
        self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)
        self.name_edit.setEnabled(True)

    def clear_message(self):
        self.print_content.setText("")

    def showEvent(self, event):
        self.initialize()
        super().showEvent(event)

    def clear_name(self, event):
        if self.name_edit.text() == "Name":
            self.name_edit.clear()

    def clear_subject(self, event):
        if self.subject_edit.text() == "Subject":
            self.subject_edit.clear()

    def query_action(self, event):
        self.scores = {}
        query_status = self.query.query_student_from_server(self.name_edit.text())

        if query_status.get('status') == 'Fail':
            self.print_content.setText(f"Please enter subjects for student '{self.name_edit.text()}'")
            self.subject_edit.setEnabled(True)
            self.score_edit.setEnabled(True)
            self.query_button.setEnabled(False)
            self.name_edit.setEnabled(False)
            self.student_dict = {'name': self.name_edit.text()}
        elif query_status.get('status') == 'OK':
            self.print_content.setText(f"The student '{self.name_edit.text()}' already exists.")

    def send_action(self, event):
        self.add_stu.add_student_to_server(self.student_dict)
        self.print_content.setText("The information " + json.dumps(self.student_dict) + " is sent.")
        self.initialize()

    def add_action(self, event):
        # 將科目和分數做成 dict
        self.scores[self.subject_edit.text()] = self.score_edit.text()
        # 將科目和分數的 dict 放入 student_dict
        self.student_dict['scores'] = self.scores
        string = "Student " + self.name_edit.text() + "'s \nsubject '" + self.subject_edit.text() + "' with\nscore '" + self.score_edit.text() + "' added"
        self.print_content.setText(string)
        self.send_button.setEnabled(True)

    def enable_query_button(self, event):
        self.query_button.setEnabled(bool(self.name_edit.text()))

    def enable_add_button(self, event):
        self.add_button.setEnabled(bool(self.subject_edit.text() and self.score_edit.text()))
