from common import *

def talk_to_client(client_socket):
    Thread(target = receive_message, args = (client_socket,)).start()
    send_message(client_socket)

def send_message(client_socket):
    while True:          
        server_message = str(input(""))
        client_socket.send(server_message.encode())

def receive_message(client_socket):
    exit_messages = ["bye", "exit", "finish", "close"] 

    while True:
        try:
            client_message = client_socket.recv(1024).decode()

            if (client_message.strip() in exit_messages or not client_message.strip()):
                client_socket.close()

            if (client_message):
                print(f"\033[1;31mClient: {client_message}\033[0m")
        except:
            print("\033[1;33m[INFO] Closing Server/Client!\033[m")
            os._exit(0)


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))

socket.listen()
print("\033[1;33m[INFO] Server waiting for connection...\033[m")

client_socket, address = socket.accept()
print(f"\033[1;33m[INFO] Connection from: {str(address)}\033[m")

talk_to_client(client_socket)
