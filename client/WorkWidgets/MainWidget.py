from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.ModifyWidget import ModifyWidget
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent
from PrintAll import PrintAll
from PyQt6.QtCore import Qt

class MainWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.setObjectName("main_widget")
        self.client = client


        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(24, "Student Management System")  # 標題標籤
        self.function_widget = FunctionWidget(client)
        self.menu_widget = MenuWidget(self.function_widget.update_widget, self.show_students)
   
      
        
        # 添加標題標籤、菜單和功能窗口到佈局
        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(self.menu_widget, 1, 0, 1, 1)
        layout.addWidget(self.function_widget, 1, 1, 1, 1)

        # 設置佈局的列和行拉伸比例
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 6)

        self.setLayout(layout)

    def show_students(self):
        # 獲取所有學生的資料並顯示在ShowStuWidget中
        print_all = PrintAll(self.client)
        reply_msg_dict = print_all.execute()
        self.function_widget.update_widget("show")
        self.function_widget.show_widget.display_students(reply_msg_dict)

class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback, show_students_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback
        self.show_students_callback = show_students_callback

        layout = QtWidgets.QVBoxLayout()
        add_button = ButtonComponent("Add student")
        del_button = ButtonComponent("Delete student")
        modify_button = ButtonComponent("Modify student")  # 確保這個按鈕存在
        show_button = ButtonComponent("Show all")

        add_button.clicked.connect(lambda: self.update_widget_callback("add"))
        del_button.clicked.connect(lambda: self.update_widget_callback("del"))
        modify_button.clicked.connect(lambda: self.update_widget_callback("modify"))  # 新增此行
        show_button.clicked.connect(lambda: self.show_students_callback())

        # 將按鈕添加到佈局中
        layout.addWidget(add_button, stretch=1)
        layout.addWidget(del_button, stretch=1)
        layout.addWidget(modify_button, stretch=1)  # 新增此行
        layout.addWidget(show_button, stretch=1)

        self.setLayout(layout)

class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.add_widget = AddStuWidget(client)
        self.show_widget = ShowStuWidget(client)
        self.del_widget = DelStuWidget(client)
        self.modify_widget = ModifyWidget(client)  # 新增這一行

        # 在字典中註冊所有窗口
        self.widget_dict = {
            "add": self.addWidget(self.add_widget),
            "show": self.addWidget(self.show_widget),
            "del": self.addWidget(self.del_widget),
            "modify": self.addWidget(self.modify_widget)  # 新增這一行
        }
        self.update_widget("add")

    def update_widget(self, name):
        # 更新顯示的窗口
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        # 如果當前窗口有initialize方法，則調用它
        if hasattr(current_widget, 'initialize'):
            current_widget.initialize()
            current_widget.clear_message()
        # 如果當前窗口有load方法，則調用它
        if hasattr(current_widget, 'load'):
            current_widget.load()
