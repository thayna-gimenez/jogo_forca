import os

from forca import Forca
from palavra import Palavra
from fases import Fases

# Coordena as regras e o fluxo de uma partida
class JogoDaForca:
    MAX_ERROS = 6

    def __init__(self, fases, forca):
        self.fases = fases
        self.forca = forca

    def iniciar(self):
        jogar_novamente = True

        while jogar_novamente:
            self.iniciar_partida()
            jogar_novamente = self.perguntar_nova_partida()

            if jogar_novamente:
                os.system("cls")

    def iniciar_partida(self):
        self.fases.mostrar_tela_inicial()
        palavra = Palavra(self.fases.obter_arquivo_palavras()).escolher()
        palavra_oculta = ["_"] * len(palavra)
        letras_certas = []
        letras_erradas = []
        numero_erros = 0

        while self.partida_em_andamento(palavra_oculta, numero_erros):
            print(f"\n{' '.join(palavra_oculta)}\n")
            letra = input("Digite uma letra: ").lower()
            numero_erros = self.processar_tentativa(
                letra,
                palavra,
                palavra_oculta,
                letras_certas,
                letras_erradas,
                numero_erros,
            )
            self.forca.desenhar(numero_erros)

        self.finalizar_partida(
            palavra, palavra_oculta, letras_certas, letras_erradas, numero_erros
        )

    def partida_em_andamento(self, palavra_oculta, numero_erros):
        return numero_erros < self.MAX_ERROS and "_" in palavra_oculta

    def processar_tentativa(
        self,
        letra,
        palavra,
        palavra_oculta,
        letras_certas,
        letras_erradas,
        numero_erros,
    ):
        if letra in palavra:
            self.revelar_letra(letra, palavra, palavra_oculta)
            if letra not in letras_certas:
                letras_certas.append(letra)
        else:
            if letra not in letras_erradas:
                letras_erradas.append(letra)
            numero_erros += 1

        return numero_erros

    def revelar_letra(self, letra, palavra, palavra_oculta):
        for indice, caractere in enumerate(palavra):
            if caractere == letra:
                palavra_oculta[indice] = letra

    def finalizar_partida(
        self,
        palavra,
        palavra_oculta,
        letras_certas,
        letras_erradas,
        numero_erros,
    ):
        self.fases.palavra = palavra
        self.fases.letras_certas = letras_certas
        self.fases.letras_erradas = letras_erradas
        self.fases.mostrar_tela_final()

        if numero_erros == self.MAX_ERROS:
            print("Você perdeu!")
        elif "_" not in palavra_oculta:
            print("Você ganhou!")

    def perguntar_nova_partida(self):
        resposta = input("Deseja jogar novamente? (s/n): ").lower()
        return resposta == "s"
