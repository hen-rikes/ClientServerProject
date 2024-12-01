from common import *

class Post:
    def __init__(self, id, content):
        self.id = id
        self.content = content

feed_limit = 24
feed_current_id = 0
feed = []

def create_post(content : str):
    global feed_current_id

    if (feed_current_id >= feed_limit):
        return "Could not create a post, max limit reached!"

    post = Post(feed_current_id, content)
    feed.append(post)

    feed_current_id += 1
    return "Post created!"

def edit_post(id, content):
    for p in feed:
        if (p.id == id):
            p.content = content
            return "Post edited!"
    return "Could not find that post!"

def show_feed():
    if feed: return "\n".join([f"\033[1;33mID: {p.id} - {p.content}\033[m" for p in feed])
    return "Feed is empty!"

def remove_post(id):
    for p in feed:
        if (p.id == id):
            feed.remove(p)
            return "Post removed!"
    return "Could not remove post!"

def receive_message(client_socket):
    while True:
        try:
            client_message = client_socket.recv(1024).decode()
            if not client_message: break

            command = client_message.split(' ', 1)
            #print(f"command[0]: {command[0]}, command[1].split(' ', 1): {command[1].split(' ', 1)}, content: {content}")
            if command[0] == 'CREATE':
                content = command[1].strip()
                answer = create_post(content)
            elif command[0] == 'EDIT':
                id, content = command[1].split(' ', 1)
                answer = edit_post(int(id), content)
            elif command[0] == 'EXCLUDE':
                id = command[1]
                answer = remove_post(int(id))
            elif command[0] == 'SHOW':
                answer = show_feed()
            elif command[0] == 'EXIT':
                answer = "Server terminated!"
                break
            else:
                answer = "Invalid command."

            client_socket.send(answer.encode())
        except Exception as e:
            client_socket.send(f"Could note receive socket messages: {str(e)}")
            break

    client_socket.close()
    print("\033[1;33m[INFO] Connection with the client was terminated!\033[m")

def server_watch(server_socket):
    global is_server_active

    exit_ops = ["exit", "sair", "close", "finish"]

    while is_server_active:
        command = str(input(""))
        if (command.strip() in exit_ops):
            is_server_active = False
            print("Closing server...")

    server_socket.close()
    os._exit(0)

is_server_active = True

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))

socket.listen(2)
print("\033[1;33m[INFO] 'exit', 'sair', 'close' or 'finish' to kill the server...\033[m")
print("\033[1;33m[INFO] Server waiting for connection...\033[m")

Thread(target=server_watch, args=(socket,)).start()

while is_server_active:
    client_socket, address = socket.accept()
    print(f"\033[1;33m[INFO] Connection with the client estabilished! Address: {str(address)}\033[m")

    Thread(target = receive_message, args = (client_socket,)).start()
