from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, ButtonComponent

class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.setObjectName("show_stu_widget")
        self.client = client

        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(18, "Show Student")
        layout.addWidget(header_label, stretch=1)

        # 創建滾動區域
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # 為滾動區域創建一個 widget
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_widget)

        # 為滾動 widget 創建佈局
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_widget)

        layout.addWidget(self.scroll_area, stretch=9)
        self.setLayout(layout)
    
    def load(self):
        pass

    def display_students(self, reply_msg_dict):
        # 清除現有的數據
        for i in reversed(range(self.scroll_layout.count())): 
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None: 
                widget.deleteLater()

        # 添加新學生數據，設置特定的字體大小
        title_label = QtWidgets.QLabel("====student list====")
        title_label.setStyleSheet("font-size: 20px;")
        self.scroll_layout.addWidget(title_label)

        for name, info in reply_msg_dict['parameters'].items():
            student_label = QtWidgets.QLabel(f"Name: {name}")
            student_label.setStyleSheet("font-size: 20px;")
            self.scroll_layout.addWidget(student_label)
            
            for subject, score in info['scores'].items():
                subject_label = QtWidgets.QLabel(f"    Subject: {subject}, Score: {score}")
                subject_label.setStyleSheet("font-size: 18px;")
                self.scroll_layout.addWidget(subject_label)

            # 添加一個空行以分隔不同學生的信息
            next_raw = QtWidgets.QLabel("\n")
            self.scroll_layout.addWidget(next_raw)
