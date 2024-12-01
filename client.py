from common import *

def talk_to_server(socket):
  Thread(target = receive_message, args = (socket,)).start()
  send_message(socket)

def receive_message(socket):
    exit_messages = ["bye", "exit", "finish", "close"] 

    while True:
        try:
            server_message = socket.recv(1024).decode()
            if (server_message.strip() in exit_messages or not server_message.strip()):
                socket.close()

            if (server_message):
                print(f"\033[1;32mServer: {server_message}\033[m")
        except:
            print("\033[1;33m[INFO] Connection was closed!\033[m")
            os._exit(0)

def send_message(socket):
    while True:
        client_message = str(input(""))
        socket.send(client_message.encode())


socket = socket.socket()
socket.connect((HOST, PORT))

talk_to_server(socket)
