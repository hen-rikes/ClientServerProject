from common import *

def exibir_menu():
    print("\nEscolha uma opção:")
    print("1. Criar postagem")
    print("2. Editar postagem")
    print("3. Excluir postagem")
    print("4. Listar postagens")
    print("5. Sair")

def criar_postagem(cliente_socket):
    conteudo = input("Digite o conteúdo da postagem: ")
    cliente_socket.send(f"CREATE {conteudo}".encode())
    resposta = cliente_socket.recv(1024)
    print(resposta)

def editar_postagem(cliente_socket):
    id_postagem = input("Digite o ID da postagem a ser editada: ")
    conteudo = input("Digite o novo conteúdo da postagem: ")
    cliente_socket.send(f"EDIT {id_postagem} {conteudo}".encode())
    resposta = cliente_socket.recv(1024).decode()
    print(resposta)

def excluir_postagem(cliente_socket):
    id_postagem = input("Digite o ID da postagem a ser excluída: ")
    cliente_socket.send(f"EXCLUDE {id_postagem}".encode())
    resposta = cliente_socket.recv(1024).decode()
    print(resposta)

def listar_postagens(cliente_socket):
    cliente_socket.send("SHOW".encode())
    resposta = cliente_socket.recv(1024).decode()
    print(resposta)


socket = socket.socket()
socket.connect((HOST, PORT))

def receive_message(socket):
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção (1-5): ")

        if opcao == '1':
            criar_postagem(socket)
        elif opcao == '2':
            editar_postagem(socket)
        elif opcao == '3':
            excluir_postagem(socket)
        elif opcao == '4':
            listar_postagens(socket)
        elif opcao == '5':
            print("Saindo...")
            socket.send("EXIT".encode())
            break
        else:
            print("Opção inválida!")

    socket.close()

Thread(target = receive_message, args = (socket,)).start()

