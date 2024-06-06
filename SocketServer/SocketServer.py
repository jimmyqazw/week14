from threading import Thread
import socket
import json

from action_list.AddStu import AddStu
from action_list.PrintAll import PrintAll
from action_list.ModifyStu import ModifyStu
from action_list.DelStu import DelStu
from action_list.Query import Query

host = "127.0.0.1"
port = 20001

action_list = {
    "add": AddStu,
    "show": PrintAll,
    "modify": ModifyStu,
    "del": DelStu,
    "query": Query
}

class SocketServer(Thread):
    def __init__(self):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The following setting is to avoid the server crash. So, the binded address can be reused
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

    def serve(self):
        self.start()

    def run(self):
        while True:
            try:
                connection, address = self.server_socket.accept()
                print("{} connected".format(address))
                self.new_connection(connection=connection,
                                    address=address)
            except:
                pass

    def new_connection(self, connection, address):
        Thread(target=self.receive_message_from_client,
               kwargs={
                   "connection": connection,
                   "address": address}, daemon=True).start()

    def receive_message_from_client(self, connection, address):
        keep_going = True
        while keep_going:
            try:
                message = connection.recv(1024).strip().decode()
            except Exception as e:
                print("Exeption happened {}, {}".format(e, address))
                keep_going = False
            else:
                if not message:
                    keep_going = False
                print(message)
                message = json.loads(message)
                print('    server received:{}'.format(message))
                command = message['command']
                parameters = message['parameters']

                reply_msg = action_list[command](parameters).execute()
                connection.send(json.dumps(reply_msg).encode())

        connection.close()
        print("{} close connection".format(address))