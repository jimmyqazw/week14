from PyQt6 import QtWidgets

from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent,ComboBoxComponent
from PyQt6.QtGui import QFont

from Modify import ModifyStu
from query import Query
from AddStu import AddStu
from PrintAll import PrintAll  # 用於從服務器獲取所有學生資料

class ModifyWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.setObjectName("modify_stu_widget")
        self.client = client
        self.add_stu = AddStu(client)
        self.modify_stu = ModifyStu(client)
        self.query = Query(client)
        self.print_all = PrintAll(client)  # 實例化 PrintAll 以便使用
        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(18, "Modify Student")

        name_content = LabelComponent(16, "Name: ")
        self.name_combo = ComboBoxComponent(16)  # 使用 QComboBox
        font = QFont("微軟正黑體", 16)  # 調整字體大小

        self.name_combo.setFont(font)

        subject_content = LabelComponent(16, "Subject: ")
        self.subject_combo = ComboBoxComponent(16)
        self.subject_combo.setFont(font)


        new_score_content = LabelComponent(16, "New score:")
        self.new_score_edit = LineEditComponent(placeholder="score",font_size=14, numeric_only=True)  # 使用新的初始化参数


        self.new_score_edit.textChanged.connect(self.toggle_send_button)  # 連接文字變化信號
        self.new_subject_edit = LineEditComponent(default_content="", placeholder="subject", font_size=14)


        self.print_content = LabelComponent(15, "")
        self.print_content.setStyleSheet("color: red;")

        self.send_button = ButtonComponent("Modify")
        
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.send_action)

        # Placement for all components
        for col in range(6):
            layout.setColumnStretch(col, 1)
        for row in range(6):
            layout.setRowStretch(row, 1)
        # 添加元件到佈局
        layout.addWidget(header_label, 0, 0, 1, 3)
        layout.addWidget(name_content, 1, 0)
        layout.addWidget(self.name_combo, 1, 1, 1, 2)
        layout.addWidget(subject_content, 3, 0)
        layout.addWidget(self.subject_combo, 3, 1, 1, 2)
        layout.addWidget(new_score_content, 5, 0, 1, 2)
        layout.addWidget(self.new_score_edit, 5, 3, 1, 1)
        layout.addWidget(self.new_subject_edit, 5, 2, 1, 1)

        layout.addWidget(self.print_content, 0, 4, 4, 2)
        layout.addWidget(self.send_button, 6, 4, 1, 2)
        self.setLayout(layout)
        self.name_combo.currentIndexChanged.connect(self.update_subjects)
        self.subject_combo.currentTextChanged.connect(self.adjust_edit_fields)

    def load_student_names(self):
        self.scores = {}
        reply_msg_dict = self.print_all.execute()
        if reply_msg_dict['status'] == "OK":
            self.name_combo.clear()
            for student_name, info in reply_msg_dict['parameters'].items():
                self.name_combo.addItem(student_name)
            if not self.name_combo.count():
                self.subject_combo.clear()
            self.check_combos()
    def adjust_edit_fields(self):
        if self.subject_combo.currentText() == "add subject":
            self.new_subject_edit.show()
            self.layout().addWidget(self.new_score_edit, 5, 3, 1, 1)
        else:
            self.new_subject_edit.hide()
            self.layout().addWidget(self.new_score_edit, 5, 2, 1, 1)
    def check_combos(self):
        if not self.name_combo.currentText():
            self.subject_combo.clear()
            self.new_score_edit.setEnabled(False)
        else:
            self.new_score_edit.setEnabled(True)
    
        

    def update_subjects(self):
        student_name = self.name_combo.currentText()
        if student_name:
            reply_msg_dict = self.print_all.execute()  # 再次獲取所有學生數據
            self.subject_combo.clear()  # 清空現有科目
            student_info = reply_msg_dict['parameters'].get(student_name, {})
            for subject in student_info.get('scores', {}):  # 假設 scores 包含了所有科目和分数
                self.subject_combo.addItem(subject)  # 添加科目到下拉列表
            self.subject_combo.addItem("add subject")  # 在列表底部添加 "add subject" 选项
            self.check_combos()

    def send_action(self):
        student_name = self.name_combo.currentText()
        if self.subject_combo.currentText() == "add subject":
            # 当选中“add subject”时，创建新科目
            new_subject = self.new_subject_edit.text().strip()
            new_score = self.new_score_edit.text().strip()
            if new_subject and new_score:  # 确保新科目和新分数不为空
                self.student_dict = {
                    'name': student_name,
                    'scores': {new_subject: new_score}
                }
       
                self.add_stu.add_student_to_server(self.student_dict)  # 假设有方法处理添加学生
                self.print_content.setText(f"Added new subject '{new_subject}' with score '{new_score}' for {student_name}.")
            else:
                self.print_content.setText("Please fill both subject and score fields.")
        else:
            # 使用选择的科目和分数修改
            subject = self.subject_combo.currentText()
            new_score = self.new_score_edit.text()
            if subject and new_score:
                self.student_dict = {
                    'name': student_name,
                    'scores': {subject: new_score}
                }
                self.modify_stu.modify_student_from_server(student_name, subject, new_score)
                self.print_content.setText(f"{student_name}'s subject {subject} has been modified to score {new_score}.")
            else:
                self.print_content.setText("Please select a subject and enter a valid score.")

        self.new_subject_edit.clear()
        self.new_score_edit.clear()
        self.load_student_names()
            

    def showEvent(self, event):
        self.load_student_names()
        self.print_content.setText("")
        self.new_score_edit.setText("")
        self.name_combo.setCurrentText("")
        self.subject_combo.setCurrentText("")
        self.send_button.setEnabled(False)
        super().showEvent(event)

    def toggle_send_button(self):
        self.send_button.setEnabled(bool(self.new_score_edit.text().strip()))
