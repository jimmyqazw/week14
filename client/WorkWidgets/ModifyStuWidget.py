from PyQt6 import QtWidgets

from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from PyQt6.QtGui import QFont

from subprogram.ModifyStu import ModifyStu
from subprogram.Query import Query
from subprogram.AddStu import AddStu
from subprogram.PrintAll import PrintAll  # 用於從服務器獲取所有學生資料

class ModifyStuWidget(QtWidgets.QWidget):
    # Initialize ========================================================
    def __init__(self, client):
        super().__init__()
        self.setObjectName("modify_stu_widget")
        self.client = client
        self.add_stu = AddStu(client)
        self.modify_stu = ModifyStu(client)
        self.query = Query(client)
        self.print_all = PrintAll(client)  # 實例化 PrintAll 以便使用
        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(20, "Modify Student")
        header_label.setStyleSheet("color:darkblue; font-weight: bold;")
        name_content = LabelComponent(16, "Name: ")
        name_content.setStyleSheet("color:#9f0fff;  font-weight: bold;")
        self.name_combo = QtWidgets.QComboBox()
        font = QFont("微軟正黑體", 16)  # 調整字體大小
        self.name_combo.setFont(font)
        self.name_combo.setStyleSheet("color:#9f0fff;  font-weight: bold;")
        subject_content = LabelComponent(16, "Subject: ")
        subject_content.setStyleSheet("color:#9f0fff;  font-weight: bold;")
        self.subject_edit = LineEditComponent(placeholder="Subject", font_size=16)
        self.subject_edit.setFont(font)
        score_content = LabelComponent(16, "Score:")
        score_content.setStyleSheet("color:#9f0fff;  font-weight: bold;")
        self.new_score_edit = LineEditComponent(placeholder="Score", font_size=14, numeric_only=True)
        self.new_score_edit.textChanged.connect(self.toggle_send_button)  # 連接文字變化信號
        self.print_content = LabelComponent(13, "====Information Display====\n1.Choose one student.\n2.Enter existing subject or new subject.\n3.Enter new score.")
        self.print_content.setStyleSheet("""
            QLabel {
                border: 2px solid #9370DB;  /* 邊框顏色 */
                border-radius: 10px;  /* 邊框圓角半徑 */
                padding: 10px;
                color: darkblue;
            }""")
        self.send_button = ButtonComponent("Modify")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.send_action)

        # Placement for all component ================================================
        for col in range(6):
            layout.setColumnStretch(col, 1)
        for row in range(6):
            layout.setRowStretch(row, 1)
        # 添加元件到佈局
        layout.addWidget(header_label, 0, 0, 1, 3)
        layout.addWidget(name_content, 1, 0)
        layout.addWidget(self.name_combo, 1, 1, 1, 2)
        layout.addWidget(subject_content, 2, 0)
        layout.addWidget(self.subject_edit, 2, 1, 1, 2)
        layout.addWidget(score_content, 3, 0, 1, 1)
        layout.addWidget(self.new_score_edit, 3, 1, 1, 2)
        layout.addWidget(self.print_content, 4, 0, 3, 4)
        layout.addWidget(self.send_button, 6, 4, 1, 2)
        self.setLayout(layout)
        self.name_combo.currentIndexChanged.connect(self.update_subjects)

    # Component effect and function=================================================================
    def load_student_names(self):
        self.scores = {}
        reply_msg_dict = self.print_all.execute()
        if reply_msg_dict['status'] == "OK":
            self.name_combo.clear()
            for student_name, info in reply_msg_dict['parameters'].items():
                self.name_combo.addItem(student_name)
            if not self.name_combo.count():
                self.subject_edit.clear()
            self.check_combos()

    def check_combos(self):
        if not self.name_combo.currentText():
            self.subject_edit.clear()
            self.new_score_edit.setEnabled(False)
        else:
            self.new_score_edit.setEnabled(True)
    
    def update_subjects(self):
        student_name = self.name_combo.currentText()
        if student_name:
            reply_msg_dict = self.print_all.execute()  # 再次獲取所有學生數據
            self.subjects = []  # Clear existing subjects list
            student_info = reply_msg_dict['parameters'].get(student_name, {})
            for subject in student_info.get('scores', {}):  # 假設 scores 包含了所有科目和分数
                self.subjects.append(subject)  # Add subjects to the list
            self.check_combos()

    def send_action(self):
        student_name = self.name_combo.currentText()
        subject = self.subject_edit.text().strip()
        new_score = self.new_score_edit.text().strip()

        if subject and new_score:
            if subject in self.subjects:
                # Use ModifyStu to update existing subject
                self.modify_stu.modify_student_from_server(student_name, subject, new_score)
                self.print_content.setText(f"{student_name}'s subject {subject} has been modified.")
            else:
                # Use AddStu to add new subject
                self.student_dict = {
                    'name': student_name,
                    'scores': {subject: new_score}
                }
                self.add_stu.add_student_to_server(self.student_dict)
                self.print_content.setText(f"Add new subject '{subject}' with score '{new_score}' for {student_name}.")
        else:
            self.print_content.setText("Please enter a subject and a valid score.")

        self.subject_edit.clear()
        self.new_score_edit.clear()
        self.load_student_names()

    def showEvent(self, event):
        self.load_student_names()
        self.new_score_edit.setText("")
        self.name_combo.setCurrentText("")
        self.subject_edit.setText("")
        self.send_button.setEnabled(False)
        super().showEvent(event)

    def toggle_send_button(self):
        self.send_button.setEnabled(bool(self.new_score_edit.text().strip()))
