import cliente
from PyQt5 import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit

cliente = cliente.cliente()

class Ui_BatePapo(object):
    def setupUi(self, BatePapo):
        BatePapo.setObjectName("BatePapo")
        BatePapo.resize(630, 409)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\icons/icons8-message-preview-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BatePapo.setWindowIcon(icon)
        self.todas_mensagens = QtWidgets.QTextBrowser(BatePapo)
        self.todas_mensagens.setGeometry(QtCore.QRect(160, 10, 461, 331))
        self.todas_mensagens.setObjectName("todas_mensagens")
        self.enviar_mensagem = QtWidgets.QPushButton(BatePapo)
        self.enviar_mensagem.setGeometry(QtCore.QRect(550, 350, 71, 23))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(".\\icons/icons8-email-send-96.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.enviar_mensagem.setIcon(icon1)
        self.enviar_mensagem.setObjectName("enviar_mensagem")
        self.enviar_arquivo = QtWidgets.QPushButton(BatePapo)
        self.enviar_arquivo.setGeometry(QtCore.QRect(550, 380, 71, 23))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(".\\icons/icons8-add-file-96.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.enviar_arquivo.setIcon(icon2)
        self.enviar_arquivo.setObjectName("enviar_arquivo")
        self.cliente_mensagem = QtWidgets.QTextEdit(BatePapo)
        self.cliente_mensagem.setGeometry(QtCore.QRect(160, 350, 381, 51))
        self.cliente_mensagem.setObjectName("cliente_mensagem")
        self.lista_usuarios = QtWidgets.QListWidget(BatePapo)
        self.lista_usuarios.setGeometry(QtCore.QRect(10, 10, 141, 391))
        self.lista_usuarios.setObjectName("lista_usuarios")

        def receberSinal(comando, valor):
            # Adiciona nova mensagem na caixa de mensagens gerais 
            if comando == "novaMensagem":
                self.todas_mensagens.append(valor)
                
            # Adiciona clientes impedindo a duplicação
            if comando == "novoCliente":
                itens = self.lista_usuarios.findItems(valor, QtCore.Qt.MatchExactly)
                if itens == []:
                    self.lista_usuarios.addItem(valor)
                
        # Evento enviar mensagem
        self.enviar_mensagem.clicked.connect(self.enviaMensagem)

        # Sinal
        cliente.sinal.connect(receberSinal)

        # Abre o input para o cliente escolher o nome de usuário
        self.getNomeCliente()

        self.retranslateUi(BatePapo)
        QtCore.QMetaObject.connectSlotsByName(BatePapo)
        
    def getNomeCliente(self):
        nomeCliente, ok = QtWidgets.QInputDialog.getText(None, "Bate Papo","Nome de usuário:", QtWidgets.QLineEdit.Normal, "")  
        aceito = cliente.novoCliente(nomeCliente)
        if aceito == False:
            self.getNomeCliente()
        
    def enviaMensagem(self):
        # Enviar Mensagem
        cliente.enviaMensagem(self.cliente_mensagem.toPlainText())
        # Apaga a caixa de texto
        self.cliente_mensagem.setText("")

    def retranslateUi(self, BatePapo):
        _translate = QtCore.QCoreApplication.translate
        BatePapo.setWindowTitle(_translate("BatePapo", "Bate Papo"))
        self.enviar_mensagem.setText(_translate("BatePapo", "Enviar"))
        self.enviar_arquivo.setText(_translate("BatePapo", "Arquivo"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BatePapo = QtWidgets.QDialog()
    ui = Ui_BatePapo()
    ui.setupUi(BatePapo)
    BatePapo.show()
    sys.exit(app.exec_())
