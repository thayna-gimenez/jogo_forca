import random

# Responsável por carregar e escolher uma palavra do banco
class Palavra:
    def __init__(self, caminho):
        self.caminho = caminho if caminho.endswith(".txt") else caminho + ".txt"

    def escolher(self):
        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            palavras = [linha.strip() for linha in arquivo if linha.strip()]

        if not palavras:
            raise ValueError("O arquivo de palavras está vazio.")

        return random.choice(palavras)
