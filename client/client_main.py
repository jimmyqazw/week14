import socket 
import json
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtGui import QIcon, QPixmap
import os
import sys

from WorkWidgets.MainWidget import MainWidget

class SocketClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 20001))

    def send_command(self, command, student_dict):
        send_data = {'command': command, 'parameters': student_dict}
        self.client_socket.send(json.dumps(send_data).encode())
        print("The client sent data => {}".format(send_data))

    def wait_response(self):
        data = self.client_socket.recv(1940)
        result = data.decode()
        print("The client received data => {}".format(result))
        return result

class CustomMainWidget(MainWidget):
    def __init__(self, client):
        super().__init__(client)
        self.init_background()

    def init_background(self):
 
        self.background_label = QLabel(self)

        if os.path.isfile('./WorkWidgets/image.jpg'):
            pixmap = QPixmap('./WorkWidgets/image.jpg')
        else:
            pixmap = QPixmap('./client/WorkWidgets/image.jpg')

        
        self.background_label.setPixmap(pixmap)
        self.background_label.resize(700, 450)  
        self.background_label.lower()  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = SocketClient()

    main_window = CustomMainWidget(client)
    main_window.setFixedSize(700, 450)
    main_window.setWindowTitle("Student Score Edit")


    if os.path.isfile('./WorkWidgets/icon.ico'):
        main_window.setWindowIcon(QIcon('./WorkWidgets/icon.ico'))
    else:
        main_window.setWindowIcon(QIcon('./client/WorkWidgets/icon.ico'))
    main_window.show()
    sys.exit(app.exec())
