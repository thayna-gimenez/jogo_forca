from forca import Forca
from fases import Fases
from jogo import JogoDaForca

# Inicia o jogo da forca
def main():
    jogo = JogoDaForca(Fases(), Forca())
    jogo.iniciar()


if __name__ == "__main__":
    main()
