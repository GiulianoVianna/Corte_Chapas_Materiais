from PyQt5.QtWidgets import (
    QApplication, QWidget, QGraphicsScene, QGraphicsView, 
    QGraphicsRectItem, QGraphicsTextItem, QLineEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

# Definindo a classe Janela que herda de QWidget
class Janela(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarInterfaceUsuario()

    # Método para inicializar a UI
    def inicializarInterfaceUsuario(self):
        # Configurando dimensões e título da janela
        self.setGeometry(350, 200, 900, 600)
        self.setWindowTitle("Cálculo de Corte de Chapas")

        # Layout vertical para organizar widgets
        layoutPrincipal = QVBoxLayout()
        self.criarCamposDeEntrada(layoutPrincipal)
        self.cena = QGraphicsScene()
        self.visao = QGraphicsView(self.cena, self)
        layoutPrincipal.addWidget(self.visao)
        self.setLayout(layoutPrincipal)
        self.show()

    # Método para criar campos de entrada e botão
    def criarCamposDeEntrada(self, layoutPrincipal):
        # Layout horizontal para os campos de texto e botão
        layoutEntrada = QHBoxLayout()

        # Criando campos de texto
        self.adicionarCampoDeTexto(layoutEntrada, 'Comprimento da Chapa', 'comprimentoChapa')
        self.adicionarCampoDeTexto(layoutEntrada, 'Largura da Chapa', 'larguraChapa')
        self.adicionarCampoDeTexto(layoutEntrada, 'Comprimento da Placa', 'comprimentoPlaca')
        self.adicionarCampoDeTexto(layoutEntrada, 'Largura da Placa', 'larguraPlaca')

        # Criando e configurando botão
        botaoCalcular = QPushButton('Calcular')
        botaoCalcular.clicked.connect(self.calcular)
        layoutEntrada.addWidget(botaoCalcular)
        layoutPrincipal.addLayout(layoutEntrada)

    # Método para adicionar campos de texto
    def adicionarCampoDeTexto(self, layout, placeholder, nomeVariavel):
        campoDeTexto = QLineEdit()
        campoDeTexto.setPlaceholderText(placeholder)
        layout.addWidget(campoDeTexto)
        setattr(self, nomeVariavel, campoDeTexto)

    # Método para realizar cálculos e desenhar na cena
    def calcular(self):
        try:
            # Obtendo valores dos campos de texto
            comprimento_chapa = int(self.comprimentoChapa.text())
            largura_chapa = int(self.larguraChapa.text())
            comprimento_placa = int(self.comprimentoPlaca.text())
            largura_placa = int(self.larguraPlaca.text())
        except ValueError:
            print("Por favor, insira valores válidos")
            return

        # Limpando cena para novo desenho
        self.cena.clear()

        # Calculando dimensões úteis
        margem = 1
        comprimento_util = comprimento_chapa - margem
        largura_util = largura_chapa

        # Calculando quantidade de placas
        qtd_placas_1 = (comprimento_util // comprimento_placa) * (largura_util // largura_placa)
        qtd_placas_2 = (comprimento_util // largura_placa) * (largura_util // comprimento_placa)

        if qtd_placas_1 >= qtd_placas_2:
            qtd_placas = qtd_placas_1
        else:
            qtd_placas = qtd_placas_2
            comprimento_placa, largura_placa = largura_placa, comprimento_placa

        # Calculando sobras
        sobra_comprimento = comprimento_util % comprimento_placa
        sobra_largura = largura_util % largura_placa

        # Desenhando chapa e placas
        self.adicionarRetangulo(0, 0, comprimento_chapa, largura_chapa, Qt.black)
        for i in range(sobra_comprimento + margem // 2, comprimento_util, comprimento_placa):
            for j in range(sobra_largura, largura_util, largura_placa):
                self.adicionarRetangulo(i, j, comprimento_placa, largura_placa, Qt.blue)

        # Adicionando texto com informações
        self.adicionarTexto(f"Dimensões da Chapa: {comprimento_chapa}x{largura_chapa} cm", comprimento_chapa + 10, 10)
        self.adicionarTexto(f"Dimensões Úteis: {comprimento_util}x{largura_util} cm", comprimento_chapa + 10, 30)
        self.adicionarTexto(f"Quantidade de Placas: {qtd_placas} un - {comprimento_placa}x{largura_placa}cm", comprimento_chapa + 10, 50)

    # Método para adicionar retângulo na cena
    def adicionarRetangulo(self, x, y, comprimento, largura, cor):
        retangulo = QGraphicsRectItem(x, y, comprimento, largura)
        retangulo.setPen(cor)
        self.cena.addItem(retangulo)

    # Método para adicionar texto na cena
    def adicionarTexto(self, texto, x, y):
        texto_item = QGraphicsTextItem(texto)
        texto_item.setFont(QFont("Arial", 10))
        texto_item.setPos(x, y)
        self.cena.addItem(texto_item)

# Inicializando aplicação
if __name__ == "__main__":
    aplicacao = QApplication([])
    janela = Janela()
    sys.exit(aplicacao.exec_())
