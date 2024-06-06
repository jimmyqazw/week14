from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent

import json

class ModifyScoreWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setObjectName("Modify_score_widget")

        # 初始化 selected_subject
        self.selected_subject = ""

        # 設置整體佈局
        main_layout = QtWidgets.QVBoxLayout()
        layout = QtWidgets.QGridLayout()
        main_layout.addLayout(layout)
        self.setLayout(main_layout)

        # 設置標籤和輸入框
        subject_label = LabelComponent(16, "Subject: ")
        subject_label.setStyleSheet("color: yellow;")
        score_label = LabelComponent(16, "Score: ")
        score_label.setStyleSheet("color: yellow;")

        fixed_width = 200  # 設置固定寬度

        self.subject_input = QtWidgets.QComboBox()
        self.subject_input.currentIndexChanged.connect(self.subject_selection_changed)
        self.subject_input.setFixedWidth(fixed_width)

        self.score_input = LineEditComponent("Score")
        self.score_input.setFixedWidth(fixed_width)
        self.score_input.setText("Score")  # 初始化提示文字
        self.score_input.mousePressEvent = lambda event: self.clear_editor_content(self.score_input, event)
        self.score_input.textChanged.connect(self.check_input_fields)

        # 添加數字輸入驗證器
        self.validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]*"))
        self.score_input.setValidator(self.validator)

        self.send_button = ButtonComponent("Modify")
        self.send_button.setEnabled(False)  # 初始禁用按鈕
        self.send_button.setStyleSheet("""
             QPushButton {
                background-color: #ADD8E6; /* 淺藍色 */
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:disabled {
                background-color: #A9A9A9;
                color: white;
            }
            QPushButton:hover:!disabled {
                background-color: #87CEEB; /* 深藍色 */
            }
        """)
        self.send_button.clicked.connect(self.modify_action)

        # 添加到佈局中
        layout.addWidget(subject_label, 2, 0, 1, 1)
        layout.addWidget(self.subject_input, 2, 1, 1, 3)
        layout.addWidget(score_label, 4, 0, 1, 1)
        layout.addWidget(self.score_input, 4, 1, 1, 3)
        layout.addWidget(self.send_button, 6, 0, 1, 3)

        # 信息框
        info_group_box = QtWidgets.QGroupBox("Information")
        info_layout = QtWidgets.QVBoxLayout()
        self.info_display_label = QtWidgets.QLabel()
        self.info_display_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.info_display_label.setStyleSheet("color: green; font-size: 20px;")  # 調整字體顏色和大小
        self.info_display_label.setWordWrap(True)  # 自動換行
        info_layout.addWidget(self.info_display_label)
        info_group_box.setLayout(info_layout)

        layout.addWidget(info_group_box, 0, 4, 7, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 4)
        layout.setColumnStretch(4, 6)  # 增加第5列以容納信息框

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)
        layout.setRowStretch(5, 1)
        layout.setRowStretch(6, 1)

        # 初始化信息框
        self.clear_info_display()

    def update_selected_student(self, student_name):
        self.subject_input.blockSignals(True)
        self.subject_input.clear()
        self.student_dict = {'name': student_name}
        self.client.send_command("query", self.student_dict)
        raw_data = self.client.wait_response()
        raw_data = json.loads(raw_data)
        self.student_dict['scores'] = raw_data.get('scores')
        self.scores = raw_data.get('scores', {})
        for subject in self.scores:
            self.subject_input.addItem(subject)

        if self.subject_input.count() > 0:
            self.subject_input.setCurrentIndex(0)
            self.subject_selection_changed()
        self.subject_input.blockSignals(False)

        # 清空信息框
        self.clear_info_display()

    def subject_selection_changed(self):
        self.selected_subject = self.subject_input.currentText()
        self.check_input_fields()  # 更新按钮状态

    def clear_editor_content(self, editor, event):
        editor.clear()
        self.clear_info_display()
        QtWidgets.QLineEdit.mousePressEvent(editor, event)  # 调用原始点击事件处理

    def check_input_fields(self):
        score_text = self.score_input.text().strip()
        if self.selected_subject and score_text and score_text != "Score":
            self.send_button.setEnabled(True)
        else:
            self.send_button.setEnabled(False)

    def modify_action(self):
        score = int(self.score_input.text())
        if score > 100:
            # 在信息框中顯示錯誤信息
            info_text = "score need <= 100\nplease try again"
            self.info_display_label.setText(info_text)
            self.info_display_label.setStyleSheet("color: red; font-size: 20px;")
        else:
            self.student_dict['scores'][self.selected_subject] = self.score_input.text()
            print(self.student_dict)
            # 有這學生所有科目分數後，傳給server
            self.client.send_command("modify", self.student_dict)
            self.client.wait_response()
            # 在信息框中顯示修改信息
            info_text = f"Modified score for subject '{self.selected_subject}' to '{self.score_input.text()}'"
            self.info_display_label.setText(info_text)
            self.info_display_label.setStyleSheet("color: yellow; font-size: 20px;")

            # 清空輸入框並禁用Modify按鈕
            self.score_input.setText("Score")
            self.send_button.setEnabled(False)

    def clear_info_display(self):
        self.info_display_label.setText("")
        self.info_display_label.setStyleSheet("color: green; font-size: 20px;")
