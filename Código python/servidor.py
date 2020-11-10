import socket
import select
import time

# Tamanho do cabeçalho
HEADER_LENGTH = 10

# IP e Porta
IP = "127.0.0.1"
PORT = 1234

# Criação de soquete
servidorSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidorSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Seta o IP e Porta que o servidor vai "ouvir"
servidorSocket.bind((IP, PORT))

# Coloca o servidor para "ouvir"
servidorSocket.listen()

# Lista de sockets
listaSockets = [servidorSocket]

# Listas de clientes, dicionário e lista comum
clientes = {}
clientesLista = []

print(f"Aguardando conexões em {IP}:{PORT}...")

def tratamentoMensagem(cliente):
    try:
        # Recebe o "cabeçalho" contendo o comprimento da mensagem, seu tamanho é definido e constante
        cabecalhoMensagem = cliente.recv(HEADER_LENGTH)

        # Se não houver mensagem o cliente fechou a aplicação
        if not len(cabecalhoMensagem):
            return False

        # Converte o cabeçalho em valor interno
        tamanhoMensagem = int(cabecalhoMensagem.decode("utf-8").strip())

        # Retorna um objeto de cabeçalho de mensagem e dados de mensagem
        return {"header": cabecalhoMensagem, "data": cliente.recv(tamanhoMensagem)}

    # Casos de interrupção bruta, como um CTRL + C
    except:
        return False

while True:
    sockets, _, exception = select.select(listaSockets, [], listaSockets)

    # Itera sobre sockets notificados
    for socket in sockets:

        # Se o soquete notificado for um soquete de servidor - nova conexão, aceite-o
        if socket == servidorSocket:

            # Aceita nova conexão
            cliente, client_address = servidorSocket.accept()

            # O cliente deve enviar seu nome imediatamente
            novoCliente = tratamentoMensagem(cliente)

            # If False - o cliente desconectou antes de enviar seu nome
            if novoCliente is False:
                continue

            # Adicionar soquete aceito à lista
            listaSockets.append(cliente)
            
            # Se o cliente já existe ele não será adicionado
            
            clientes[cliente] = novoCliente
            clientesLista.append(novoCliente)
            print("Novo cliente conectado {}:{}, nome: {}".format(*client_address, novoCliente["data"].decode("utf-8")))

            # Delay para evitar erros na atualização da tela
            time.sleep(0.1)

            # Envia os clientes conectados a chegada do novo
            for cliente in clientes:
                for socket in clientesLista:
                    cliente.send(socket['header'] + socket['data'] + socket['header'] + socket['data'])

        # Caso contrário, o soquete existente está enviando uma mensagem
        else:

            # Receber mensagem
            message = tratamentoMensagem(socket)

            # Se False, o cliente se desconectou
            if message is False:
                print("Cliente desconectado: {}".format(clientes[socket]["data"].decode("utf-8")))

                # Remova da lista para socket.socket ()
                listaSockets.remove(socket)

                # Remova da nossa lista de clientes
                del clientes[socket]

                continue

            # Obter cliente por soquete notificado, assim saberemos quem enviou a mensagem
            novoCliente = clientes[socket]

            print(f"Mensagem de {novoCliente['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            # Iterar sobre clientes conectados e transmitir mensagem
            for cliente in clientes:
                cliente.send(novoCliente['header'] + novoCliente['data'] + message['header'] + message['data'])