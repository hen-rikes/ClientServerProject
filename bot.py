from common import *

def criar_postagem(cliente_socket, message):
    conteudo = f"{message}"
    cliente_socket.send(f"CREATE {conteudo}".encode())
    resposta = cliente_socket.recv(1024).decode()
    print(resposta)

#connetion
def talk_to_server(socket):
  Thread(target = send_message, args = (socket,)).start()

def send_message(socket):
    nomes = ["Carlos", "Henrique", "Arthur", "Fernando", "Kri3g"]
    for _ in range(0, 10):
        criar_postagem(socket, f"BogusAmogus in the focus: {nomes[rand(0, len(nomes)-1)]}")

    socket.close()

socket = socket.socket()
socket.connect((HOST, PORT))

talk_to_server(socket)
