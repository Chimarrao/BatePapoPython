import socket
import select
import errno
import threading
import random
from PyQt5 import QtCore

# Tamanho do cabeçalho
HEADER_LENGTH = 10

# IP e Porta
IP = "127.0.0.1"
PORT = 1234

# Cria um socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao IP e Porta
clientSocket.connect((IP, PORT))

# Remove o bloqueio para while True
clientSocket.setblocking(1)

class cliente(QtCore.QThread):
    sinal = QtCore.pyqtSignal(object, str)

    def __init__(self):
        QtCore.QThread.__init__(self)

        def receberMensagens():
            try:
                while True:
                    # Recebe o cabeçalho
                    cliente = clientSocket.recv(HEADER_LENGTH)

                    # Se o servidor for encerrado
                    if not len(cliente):
                        print("Conexão encerrada pelo servidor")

                    # Converter cabeçalho em valor interno
                    tamanhoUsuario = int(cliente.decode('utf-8').strip())

                    # Receber e decodificar nome de usuário
                    usuario = clientSocket.recv(tamanhoUsuario).decode('utf-8')

                    # Recebe o cabeçalho da mensagem
                    cabecalhoMensagem = clientSocket.recv(HEADER_LENGTH)

                    # Recebe a mensagem
                    tamanhoMensagem = int(cabecalhoMensagem.decode('utf-8').strip())
                    mensagem = clientSocket.recv(tamanhoMensagem).decode('utf-8')

                    # Filtra o conteúdo recebido
                    if mensagem == usuario:
                        self.sinal.emit("novoCliente", f'{usuario}')
                    else:
                        self.sinal.emit("novaMensagem", f'{usuario} > {mensagem}')

            except IOError as e:
                print(e)
                pass

            except Exception as e:
                print(e)
                pass

        # Thread responsável pela recepção das mensagens
        receber = threading.Thread(target=receberMensagens)
        receber.start()
        
    def novoCliente(self, nomeCliente):
        self.nomeCliente = nomeCliente
        # Codifique a mensagem em bytes 
        usuario = nomeCliente.encode('utf-8')
        # Preparamos o cabeçalho convertendo em bytes
        cliente = f"{len(usuario):<{HEADER_LENGTH}}".encode('utf-8')
        
        # Envia a mensagem
        clientSocket.send(cliente + usuario)

    def enviaMensagem(self, mensagem):
        self.mensagem = mensagem

        if self.mensagem and self.mensagem != "":
            # Codifique a mensagem em bytes 
            self.mensagem = self.mensagem.encode('utf-8')
            # Preparamos o cabeçalho convertendo em bytes
            cabecalhoMensagem = f"{len(self.mensagem):<{HEADER_LENGTH}}".encode('utf-8')
            # Envia a mensagem
            clientSocket.send(cabecalhoMensagem + self.mensagem)
