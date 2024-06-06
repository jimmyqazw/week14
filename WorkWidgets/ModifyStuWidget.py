# ModifyStuWidget.py

from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent
from .AddSubjectWidget import AddSubjectWidget
from .ModifyScoreWidget import ModifyScoreWidget

class ModifyStuWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.selected_students = []
        self.setObjectName("Modify_stu_widget")

        main_layout = QtWidgets.QVBoxLayout()
        top_layout = QtWidgets.QHBoxLayout()

        ### show student text ###
        header_label = LabelComponent(20, "Modify Student")
        header_label.setStyleSheet("color: yellow;")
        header_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)  # 至頂於最上面

        ### 下拉菜单 ###
        self.student_combo_box = QtWidgets.QComboBox()
        self.student_combo_box.setMinimumWidth(100)
        self.student_combo_box.currentIndexChanged.connect(self.student_selection_changed)

        ### add subject and modify score options with radio buttons ###
        self.option_group = QtWidgets.QButtonGroup(self)
        self.add_subject_radio = QtWidgets.QRadioButton("Add Subject")
        self.add_subject_radio.setStyleSheet("color: yellow;")
        self.modify_score_radio = QtWidgets.QRadioButton("Modify Score")
        self.modify_score_radio.setStyleSheet("color: yellow;")

        self.option_group.addButton(self.add_subject_radio)
        self.option_group.addButton(self.modify_score_radio)

        self.add_subject_radio.toggled.connect(self.show_add_subject_interface)
        self.modify_score_radio.toggled.connect(self.show_modify_score_interface)

        # Add widgets to the top layout with spacers
        top_layout.addWidget(header_label)
        top_layout.addSpacing(40)  # 添加间隔
        top_layout.addWidget(self.student_combo_box)
        top_layout.addSpacing(40)  # 添加间隔
        top_layout.addWidget(self.add_subject_radio)
        top_layout.addSpacing(40)  # 添加间隔
        top_layout.addWidget(self.modify_score_radio)
        top_layout.addStretch()

        # Add top layout to main layout
        main_layout.addLayout(top_layout)

        # Stacked widget to switch between different interfaces
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.add_subject_widget = AddSubjectWidget(client)
        self.modify_score_widget = ModifyScoreWidget(client)

        self.stacked_widget.addWidget(self.add_subject_widget)
        self.stacked_widget.addWidget(self.modify_score_widget)

        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        # 设置默认选项为Modify Score
        self.modify_score_radio.setChecked(True)
        self.show_modify_score_interface(True)

    def load(self):  # 使用初始化，讓每次資料都能更新
        pass

    def set_selected_students(self, students):
        self.selected_students = students
        self.update_student_combo_box()
        self.load()
        # 选择第一个学生以触发 student_selection_changed
        if self.student_combo_box.count() > 0:
            self.student_combo_box.setCurrentIndex(0)

    def update_student_combo_box(self):
        self.student_combo_box.clear()
        self.student_combo_box.addItems(self.selected_students)

    def get_current_selected_student(self):
        return self.student_combo_box.currentText()

    def show_add_subject_interface(self, checked):
        if checked:
            self.stacked_widget.setCurrentWidget(self.add_subject_widget)
            self.add_subject_widget.subject_input.setText("Enter Subject")  # 重置输入框内容
            self.add_subject_widget.score_input.setText("Enter Score")  # 重置输入框内容
            self.student_combo_box.blockSignals(True)  # 暂时断开信号连接
            self.student_selection_changed()  # 更新選中的學生資料
            self.student_combo_box.blockSignals(False)  # 重新连接信号

    def show_modify_score_interface(self, checked):
        if checked:
            self.stacked_widget.setCurrentWidget(self.modify_score_widget)
            self.modify_score_widget.score_input.setText("Enter Score")  # 重置输入框内容
            self.student_combo_box.blockSignals(True)  # 暂时断开信号连接
            self.student_selection_changed()  # 更新選中的學生資料
            self.student_combo_box.blockSignals(False)  # 重新连接信号

    def student_selection_changed(self):
        current_student = self.get_current_selected_student()
        if self.modify_score_radio.isChecked():
            self.modify_score_widget.update_selected_student(current_student)
            self.modify_score_widget.score_input.setText("Score")  # 重置输入框内容
        elif self.add_subject_radio.isChecked():
            self.add_subject_widget.update_selected_student(current_student)
            self.add_subject_widget.subject_input.setText("Subject")  # 重置输入框内容
            self.add_subject_widget.score_input.setText("Score")  # 重置输入框内容
