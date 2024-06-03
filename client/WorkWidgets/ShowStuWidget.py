from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, ButtonComponent
import json

class ShowStuWidget(QtWidgets.QWidget):
    #Initialize ========================================================
    def __init__(self, client):
        super().__init__()
        self.setObjectName("show_stu_widget")
        self.client = client
        layout = QtWidgets.QVBoxLayout()
        header_label = LabelComponent(20, "Show Student")
        header_label.setStyleSheet("color:darkblue; font-weight: bold;")
        self.content_label = LabelComponent(16,"")
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setWidget(self.content_label)

    #Placement for all component ================================================  
        layout.addWidget(header_label, stretch=1)
        layout.addWidget(self.scroll_area, stretch=9)
        self.setLayout(layout)
    
    #Component effect and function================================================
    def load(self):
        self.client.send_command("show", {})
        data = self.client.wait_response()
        data = json.loads(data)
        if data.get('status') == 'OK': 
            text = "<pre>========== Student List ==========\n</pre>"       
            for key, value in data['parameters'].items():
                text += "<pre>Name:{}</pre>".format(value['name'])
                for subject, score in value['scores'].items():
                    if score < 60:
                        text += "<pre>  Subject:{}, Score:<span style='color: red;'>{}</span></pre>\n".format(subject, score)
                    else:
                        text += "<pre>  Subject:{}, Score:{}</pre>\n".format(subject, score)
            self.content_label.setStyleSheet("font-family: Microsoft JhengHei; font-weight:bold;")           
            self.content_label.setText(text)


  
 
     
        



    
