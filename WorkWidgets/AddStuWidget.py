from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
import json


class AddStuWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        # 儲存當下學生的成績
        self.student_dict = {}
        self.client = client
        self.setObjectName("add_stu_widget")

        # 設置整體佈局
        main_layout = QtWidgets.QVBoxLayout()
        layout = QtWidgets.QGridLayout()
        main_layout.addLayout(layout)
        self.setLayout(main_layout)

        # 設置標籤和輸入框
        header_label = LabelComponent(20, "Add Student")
        header_label.setStyleSheet("color: yellow;")
        name_label = LabelComponent(16, "Name: ")
        name_label.setStyleSheet("color: yellow;")
        subject_label = LabelComponent(16, "Subject: ")
        subject_label.setStyleSheet("color: yellow;")
        score_label = LabelComponent(16, "Score: ")
        score_label.setStyleSheet("color: yellow;")

        fixed_width = 200  # 設置固定寬度

        self.name_editor_label = LineEditComponent("Name")
        self.name_editor_label.setFixedWidth(fixed_width)
        self.name_editor_label.mousePressEvent = lambda event: self.clear_editor_content(self.name_editor_label, event)
        self.name_editor_label.textChanged.connect(self.check_input)

        self.subject_editor_label = LineEditComponent("Subject")
        self.subject_editor_label.setFixedWidth(fixed_width)
        self.subject_editor_label.setEnabled(False)
        self.subject_editor_label.mousePressEvent = lambda event: self.clear_editor_content(self.subject_editor_label, event)
        self.subject_editor_label.textChanged.connect(self.check_add)

        self.score_editor_label = LineEditComponent("Score")
        self.score_editor_label.setFixedWidth(fixed_width)
        self.score_editor_label.setEnabled(False)
        self.score_editor_label.mousePressEvent = lambda event: self.clear_editor_content(self.score_editor_label, event)
        self.score_editor_label.textChanged.connect(self.check_add)

        # 设置输入验证器，只允许数字
        self.validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]*"))
        self.score_editor_label.setValidator(self.validator)

        self.query_button = ButtonComponent("Query")
        self.query_button.setEnabled(False)
        self.query_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border-radius: 5px; 
                padding: 5px;
            }
            QPushButton:disabled {
                background-color: #A9A9A9;
                color: white;
            }
            QPushButton:hover:!disabled {
                background-color: #45a049;
            }
        """)
        self.query_button.clicked.connect(self.query_action)

        self.add_button = ButtonComponent("Add")
        self.add_button.setEnabled(False)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border-radius: 5px; 
                padding: 5px;
            }
            QPushButton:disabled {
                background-color: #A9A9A9;
                color: white;
            }
            QPushButton:hover:!disabled {
                background-color: #45a049;
            }
        """)
        self.add_button.clicked.connect(self.add_action)

        self.send_button = ButtonComponent("Send")
        self.send_button.setEnabled(False)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border-radius: 5px; 
                padding: 5px;
            }
            QPushButton:disabled {
                background-color: #A9A9A9;
                color: white;
            }
            QPushButton:hover:!disabled {
                background-color: #45a049;
            }
        """)
        self.send_button.clicked.connect(self.send_action)

        # 添加到佈局中
        layout.addWidget(header_label, 0, 0, 1, 3)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(self.name_editor_label, 1, 1, 1, 1)
        layout.addWidget(self.query_button, 1, 2, 1, 1)
        layout.addWidget(subject_label, 2, 0, 1, 1)
        layout.addWidget(self.subject_editor_label, 2, 1, 1, 1)
        layout.addWidget(score_label, 3, 0, 1, 1)
        layout.addWidget(self.score_editor_label, 3, 1, 1, 1)
        layout.addWidget(self.add_button, 3, 2, 1, 1)
        layout.addWidget(self.send_button, 5, 0, 1, 3)

        # 信息框
        info_group_box = QtWidgets.QGroupBox("Information")
        info_layout = QtWidgets.QVBoxLayout()
        self.info_display_label = QtWidgets.QLabel()
        self.info_display_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.info_display_label.setStyleSheet("color: yellow; font-size: 20px;")  # 調整字體顏色和大小
        self.info_display_label.setWordWrap(True)  # 自動換行
        info_layout.addWidget(self.info_display_label)
        info_group_box.setLayout(info_layout)

        layout.addWidget(info_group_box, 0, 3, 6, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 4)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)
        layout.setRowStretch(5, 1)


    def clear_editor_content(self, editor, event):
        editor.clear()

    def check_input(self, event):  # 控制 query_button
        if self.name_editor_label.text():  # 如果输入框有内容
            self.query_button.setEnabled(True)  # 启用按钮
        else:
            self.query_button.setEnabled(False)  # 否则禁用按钮

    def check_add(self, event):  # 控制 add_button
        if self.subject_editor_label.text() and self.score_editor_label.text():
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def query_action(self):
        self.scores = {}
        # query傳給server
        self.student_dict = {'name': self.name_editor_label.text()}
        self.client.send_command("query", self.student_dict)
        # 回傳結果告知name是否存在
        raw_data = self.client.wait_response()
        raw_data = json.loads(raw_data)

        # text:name是否存在
        if raw_data.get('status') == 'Fail':  # 不存在，資料會回傳到DB
            info_text = f"Please enter subject for student '{self.name_editor_label.text()}'"
            self.info_display_label.setStyleSheet("color: yellow; font-size: 20px;")
            # button control
            self.name_editor_label.setEnabled(False)
            self.query_button.setEnabled(False)
            self.subject_editor_label.setEnabled(True)
            self.score_editor_label.setEnabled(True)
        else:  # 存在，資料不會回傳到DB
            info_text = (f"The name '{self.name_editor_label.text()}' is already exists. \n\n"
                         f"please try again. \n\n"
                         f"If you want to modify, please use modify.")
            self.info_display_label.setStyleSheet("color: red; font-size: 20px;")

        self.info_display_label.setText(info_text)

    def add_action(self):
        if int(self.score_editor_label.text()) <= 100:
            # 將科目和分數做成dict
            self.scores[self.subject_editor_label.text()] = self.score_editor_label.text()
            # 將科目和分數的dict，放入student_dict
            self.student_dict['scores'] = self.scores
            # information detail
            info_text = f"Student {self.name_editor_label.text()}'s subject '{self.subject_editor_label.text()}' with score '{self.score_editor_label.text()}' added"
            self.info_display_label.setText(info_text)
            self.info_display_label.setStyleSheet("color: yellow; font-size: 20px;")
            # 有新增加科目和分數，才打開send按鈕
            self.send_button.setEnabled(True)
        else:
            info_text = f"score need <= 100 \nplease try again"
            self.info_display_label.setText(info_text)
            self.info_display_label.setStyleSheet("color: red; font-size: 20px;")

    def send_action(self):
        # 有這學生所有科目分數後，傳給server
        self.client.send_command("add", self.student_dict)
        # server回傳學生是否存在
        raw_data = self.client.wait_response()
        # 判斷學生是否已存在
        raw_data = json.loads(raw_data)
        if raw_data.get('status') == 'OK':
            info_text = f"Add {self.student_dict} successfully"  # 不存在
        else:
            info_text = f"Add {self.student_dict} fail"  # 已存在

        self.info_display_label.setText(info_text)

        # 重新放入輸入框提示，告訴使用者該放入甚麼訊息
        self.name_editor_label.setText("Name")
        self.subject_editor_label.setText("Subject")
        self.score_editor_label.setText("")
        # setPlaceholderText是背景文字，點下去不會不見
        # setText是實體文字，點下去會不見

        # 按鈕和輸入框關閉
        self.name_editor_label.setEnabled(True)
        self.query_button.setEnabled(False)
        self.subject_editor_label.setEnabled(False)
        self.score_editor_label.setEnabled(False)
        self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)

    def load(self):
        self.name_editor_label.setText("Name")
        self.subject_editor_label.setText("Subject")
        self.score_editor_label.setText("")
        self.info_display_label.setText("")

        # 按钮和输入框的初始状态
        self.name_editor_label.setEnabled(True)
        self.query_button.setEnabled(False)
        self.subject_editor_label.setEnabled(False)
        self.score_editor_label.setEnabled(False)
        self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)
