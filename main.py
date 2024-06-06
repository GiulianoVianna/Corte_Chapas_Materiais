from PyQt5.QtWidgets import (
    QApplication, QWidget, QGraphicsScene, QGraphicsView, 
    QGraphicsRectItem, QGraphicsTextItem, QLineEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
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
        self.setWindowIcon(QIcon('logo.ico'))

        # Layout vertical para organizar widgets
        layoutPrincipal = QVBoxLayout()
        self.criarCamposDeEntrada(layoutPrincipal)
        self.cena = QGraphicsScene()
        self.visao = QGraphicsView(self.cena, self)
        layoutPrincipal.addWidget(self.visao)
        self.setLayout(layoutPrincipal)
        self.setWindowState(Qt.WindowMaximized)
        self.show()

    # Método para criar campos de entrada e botão
    def criarCamposDeEntrada(self, layoutPrincipal):
        layoutEntrada = QHBoxLayout()

        # Criando campos de texto
        self.adicionarCampoDeTexto(layoutEntrada, 'Comprimento da Chapa', 'comprimentoChapa')
        self.adicionarCampoDeTexto(layoutEntrada, 'Largura da Chapa', 'larguraChapa')
        self.adicionarCampoDeTexto(layoutEntrada, 'Comprimento da Placa', 'comprimentoPlaca')
        self.adicionarCampoDeTexto(layoutEntrada, 'Largura da Placa', 'larguraPlaca')

        # Criando e configurando botão
        botaoCalcular = QPushButton('Calcular')
        botaoCalcular.clicked.connect(self.calcular)
        botaoCalcular.setFont(QFont("Arial", 13))
        layoutEntrada.addWidget(botaoCalcular)
        layoutPrincipal.addLayout(layoutEntrada)

    # Método para adicionar campos de texto
    def adicionarCampoDeTexto(self, layout, placeholder, nomeVariavel):
        campoDeTexto = QLineEdit()
        campoDeTexto.setPlaceholderText(placeholder)
        campoDeTexto.setFont(QFont("Arial", 13)) 
        layout.addWidget(campoDeTexto)
        setattr(self, nomeVariavel, campoDeTexto)

    # Método para realizar cálculos e desenhar na cena
    def calcular(self):
        try:
            comprimento_chapa = float(self.comprimentoChapa.text().replace(',', '.'))
            largura_chapa = float(self.larguraChapa.text().replace(',', '.'))
            comprimento_placa = float(self.comprimentoPlaca.text().replace(',', '.'))
            largura_placa = float(self.larguraPlaca.text().replace(',', '.'))
        except ValueError:
            print("Por favor, insira valores válidos")
            return

        self.cena.clear()

        # Aumentando as dimensões em 2.5 vezes para melhor visualização
        fator_aumento = 2.5
        comprimento_chapa *= fator_aumento
        largura_chapa *= fator_aumento
        comprimento_placa *= fator_aumento
        largura_placa *= fator_aumento

        # Calculando dimensões úteis
        margem = 1 * fator_aumento
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
        for i in range(int(margem // 2), int(comprimento_util), int(comprimento_placa)):
            for j in range(0, int(largura_util), int(largura_placa)):
                if i + comprimento_placa <= comprimento_chapa and j + largura_placa <= largura_chapa:
                    self.adicionarRetangulo(i, j, comprimento_placa, largura_placa, Qt.blue)

        # Adicionando texto com informações
        y_offset = 10
        self.adicionarTexto(f"Dimensões da Chapa: {str(format(comprimento_chapa / fator_aumento, '.2f')).replace('.', ',')}x{str(format(largura_chapa / fator_aumento, '.2f')).replace('.', ',')} cm", comprimento_chapa + 10, y_offset)

        y_offset += 40  # Ajuste a posição y para a próxima linha de texto
        self.adicionarTexto(f"Dimensões Úteis: {str(format(comprimento_util / fator_aumento, '.2f')).replace('.', ',')}x{str(format(largura_util / fator_aumento, '.2f')).replace('.', ',')} cm", comprimento_chapa + 10, y_offset)

        y_offset += 40  # Ajuste a posição y para a próxima linha de texto
        self.adicionarTexto(f"Quantidade de Placas: {qtd_placas} un - {str(format(comprimento_placa / fator_aumento, '.2f')).replace('.', ',')}x{str(format(largura_placa / fator_aumento, '.2f')).replace('.', ',')} cm", comprimento_chapa + 10, y_offset)



    # Método para adicionar retângulo na cena
    def adicionarRetangulo(self, x, y, comprimento, largura, cor):
        retangulo = QGraphicsRectItem(x, y, comprimento, largura)
        retangulo.setPen(cor)
        self.cena.addItem(retangulo)

    # Método para adicionar texto na cena
    def adicionarTexto(self, texto, x, y):
        texto_item = QGraphicsTextItem(texto)
        texto_item.setFont(QFont("Arial", 13))
        texto_item.setPos(x, y)
        self.cena.addItem(texto_item)

# Inicializando aplicação
if __name__ == "__main__":
    aplicacao = QApplication([])
    janela = Janela()
    sys.exit(aplicacao.exec_())
