import socket 
import json
import sys
from WorkWidgets.MainWidget import MainWidget
from WorkWidgets.EntryWidget import EntryWidget
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
import os

class SocketClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client_socket.connect((host, port))
 
    def send_command(self, command, student_dict):
        send_data = {'command': command, 'parameters': student_dict}
        self.client_socket.send(json.dumps(send_data).encode())
        print("    The client sent data => {}".format(send_data))

    def wait_response(self):
        data = self.client_socket.recv(BUFFER_SIZE)
        result = data.decode()
        print("    The client received data => {}".format(result))

        return result

class MainApplication(QtWidgets.QMainWindow):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)
        self.entry_widget = EntryWidget(client)
        self.stack.addWidget(self.entry_widget)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 20001
    BUFFER_SIZE = 1940
    app = QtWidgets.QApplication(sys.argv)
    client = SocketClient() 
    main_window = MainApplication(client)
    main_window.setFixedSize(700, 400)
    if os.path.isfile('./Image/icon.jpg'):
        main_window.setWindowIcon(QIcon('./Image/icon.jpg'))
    else:
        main_window.setWindowIcon(QIcon('./client/Image/icon.jpg'))
    main_window.setWindowTitle("NTUT Student Management System")
    main_window.show()
    sys.exit(app.exec())    
    