from SocketServer import SocketServer
from DB.DBConnection import DBConnection
from DB.DBInitializer import DBInitializer

def main():
    server = SocketServer()
    server.daemon = True
    server.serve()
    DBConnection.db_file_path = "example.db"
    DBInitializer().execute()

    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break

    server.server_socket.close()
    print("leaving ....... ")

main()