from PyQt6 import QtWidgets
from WorkWidgets.WidgetComponents import LabelComponent, ButtonComponent,ComboBoxComponent
from PyQt6.QtGui import QFont
from DelStu import DelStu
from query import Query
from PrintAll import PrintAll  # 用於從服務器獲取所有學生資料

class DelStuWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.setObjectName("del_stu_widget")
        self.client = client

        self.del_stu = DelStu(client)
        self.query = Query(client)
        self.print_all = PrintAll(client)  # 實例化 PrintAll 以便使用
        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(18, "Delete Student")

        name_content = LabelComponent(16, "Name: ")
        self.name_combo = ComboBoxComponent(16)  # 使用 QComboBox
        font = QFont("微軟正黑體", 16)  # 調整字體大小

        self.name_combo.setFont(font)

        self.print_content = LabelComponent(15, "")
        self.print_content.setStyleSheet("color: red;")

        self.send_button = ButtonComponent("Delete")

        self.send_button.clicked.connect(self.send_action)

        # Placement for all components
        for col in range(6):
            layout.setColumnStretch(col, 1)
        for row in range(6):
            layout.setRowStretch(row, 1)
        # 添加元件到佈局
        layout.addWidget(header_label, 0, 0, 1, 3)
        layout.addWidget(name_content, 2, 0)
        layout.addWidget(self.name_combo, 2, 1, 1, 2)
        layout.addWidget(self.print_content, 0, 4, 4, 2)
        layout.addWidget(self.send_button, 6, 4, 1, 2)
        self.setLayout(layout)

    def check_name_combo(self):
        """根據 combo box 狀態啟用或禁用發送按鈕。"""
        # 確保 name_combo 当前有选中的索引並且文本不為空
        self.send_button.setEnabled(self.name_combo.currentIndex() != -1 and bool(self.name_combo.currentText().strip()))

    def load_student_names(self):
        reply_msg_dict = self.print_all.execute()
        if reply_msg_dict['status'] == "OK":
            self.name_combo.clear()
            for student_name in reply_msg_dict['parameters'].keys():
                self.name_combo.addItem(student_name)
            # 加載名稱後，檢查是否應該啟用發送按鈕
            self.check_name_combo()

    def send_action(self):
        student_name = self.name_combo.currentText()
        self.del_stu.del_student_from_server(student_name)
        self.print_content.setText(f"The student for {student_name} has been deleted.")
        self.load_student_names()

    def showEvent(self, event):
        self.load_student_names()
        self.print_content.setText("")
        self.name_combo.setCurrentText("")
        super().showEvent(event)
