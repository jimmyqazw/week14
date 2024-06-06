from SocketClient.SocketClient import SocketClient
from WorkWidgets.MainWidget import MainWidget
from PyQt6.QtWidgets import QApplication
import sys

client = SocketClient()

app = QApplication([])
main_window = MainWidget(client)

main_window.setFixedSize(700, 400)
main_window.show()
# main_window.showFullScreen()

sys.exit(app.exec())

# client.client_socket.close()