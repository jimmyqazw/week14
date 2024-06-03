import socket
from threading import Thread
import json
from sqlite.DBConnection import DBConnection
from sqlite.DBInitializer import DBInitializer
from command import AddStu, DelStu, ModifyStu, PrintAll, Query

class SocketServer(Thread):
    def __init__(self):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

    def serve(self):
        self.start()

    def run(self):
        while True:
            try:
                conn, addr = self.server_socket.accept()
                print("{} connected".format(addr))
                self.handle_client(conn, addr)
            except:
                pass

    def handle_client(self, conn, addr):
        Thread(target=self.process_client, kwargs={'conn': conn, 'addr': addr}, daemon=True).start()

    def process_client(self, conn, addr):
        commands = {"add": AddStu, "show": PrintAll, "modify": ModifyStu, "del": DelStu, "query": Query}
        active = True
        while active:
            try:
                msg = conn.recv(1024).strip().decode()
                if not msg:
                    print(f"No message received from {addr}, closing connection.")
                    active = False
                    continue
            except Exception as e:
                print(f"Exception occurred: {e}, {addr}")
                break

            try:
                print(msg)
                msg_json = json.loads(msg)
                print('    server received:{}'.format(msg_json))
                cmd = msg_json['command']
                args = msg_json['parameters']
                response = commands[cmd](args).execute()
                conn.send(json.dumps(response).encode())
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e} from {addr}, possibly client disconnected.")
                break

        conn.close()
        print(f"{addr} connection closed")

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 20001
    server = SocketServer()
    server.daemon = True
    server.serve()
    DBConnection.db_file_path = "example.db"
    DBInitializer().execute()

    while True:
        cmd = input()
        if cmd == "finish":
            break

    server.server_socket.close()
    print("leaving ....... ")