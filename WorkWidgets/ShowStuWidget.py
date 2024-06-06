from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from PyQt6.QtCore import pyqtSignal
import json
from PyQt6.QtCore import pyqtSignal, pyqtSlot


class ShowStuWidget(QtWidgets.QWidget):
    students_selected = pyqtSignal(list)

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setObjectName("show_stu_widget")
        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(20, "Show Student")
        header_label.setStyleSheet("color: yellow;")
        header_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(header_label)

        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderLabels(["", "Name", "Subject", "Score"])

        # 设置样式表，使表格美观
        self.tree_widget.setStyleSheet("""
            QHeaderView::section {
                background-color: yellow;
                padding: 4px;
                border: 1px solid lightgray;
            }
            QTreeWidget::item {
                border: 1px solid lightgray;
                padding: 5px;
            }
            QTreeWidget::item:selected {
                background-color: #a8d8ea;
                color: black;
            }

            QTreeWidget::item:selected:hover {
                background-color: #a8d8ea;
            }
            QTreeWidget::item:selected:!active {
                background-color: #e0f7fa;
            }
        """)

        # 设置标准图标
        style = QtWidgets.QApplication.style()
        self.tree_widget.setStyle(style)
        self.tree_widget.setIconSize(QtCore.QSize(16, 16))
        self.tree_widget.setAnimated(True)
        self.tree_widget.setExpandsOnDoubleClick(False)

        layout.addWidget(self.tree_widget)
        self.setLayout(layout)

    def load(self):
        raw_data = self.client_print()
        self.populate_tree(raw_data)

    def client_print(self):
        self.client.send_command("show", student_dict={})
        raw_data = self.client.wait_response()
        raw_data = json.loads(raw_data)
        return raw_data

    def populate_tree(self, student_dict):
        self.tree_widget.clear()
        for name, info in student_dict['parameters'].items():
            student_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
            checkbox = QtWidgets.QCheckBox()
            checkbox.stateChanged.connect(self.some_method_that_updates_selection)
            self.tree_widget.setItemWidget(student_item, 0, checkbox)
            student_item.setText(1, name)
            for subject, score in info['scores'].items():
                subject_item = QtWidgets.QTreeWidgetItem(student_item)
                subject_item.setText(2, subject)
                subject_item.setText(3, str(score))
                # 检查分数，如果低于60，设置为红色
                if score < 60:
                    subject_item.setForeground(3, QtGui.QBrush(QtCore.Qt.GlobalColor.red))

        self.tree_widget.expandAll()

    def get_selected_students(self):
        selected_students = []
        root = self.tree_widget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            student_item = root.child(i)
            checkbox = self.tree_widget.itemWidget(student_item, 0)
            if checkbox.isChecked():
                selected_students.append(student_item.text(1))
        return selected_students

    @pyqtSlot()
    def some_method_that_updates_selection(self):
        selected_students = self.get_selected_students()
        self.students_selected.emit(selected_students)

