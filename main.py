import random
import os


# Recebe o caminho do arquivo de palavras e escolhe uma palavra aleatória
class Palavra:
    def __init__(self, path=None):
        if path is None:
            self.path = None
        else:
            self.path = path if path.endswith(".txt") else path + ".txt"

    def escolher_palavra(self):
        if not self.path:
            raise ValueError("Caminho do arquivo não informado.")

        with open(self.path, "r", encoding="utf-8") as arquivo:
            palavras = [linha.strip() for linha in arquivo if linha.strip()]

        return random.choice(palavras)

    def get_palavra(self):
        return self.escolher_palavra()


# Desenha a forca de acordo com o número de erros do jogador
class Forca:
    fases = [
        """
            --------
            |      |
            |      
            |    
            |      
            |     
            -
        """,
        """
            --------
            |      |
            |      O
            |    
            |      
            |     
            -
        """,
        """
            --------
            |      |
            |      O
            |      |
            |      
            |     
            -
        """,
        """
            --------
            |      |
            |      O
            |     /|
            |      
            |     
            -
        """,
        """
            --------
            |      |
            |      O
            |     /|\\
            |      
            |     
            -
        """,
        """
            --------
            |      |
            |      O
            |     /|\\
            |     / 
            |     
            -
        """,
        """
            --------
            |      |
            |      O
            |     /|\\
            |     / \\
            |
        """
    ]

    def desenhar_forca(self, n_erro):
        if 0 <= n_erro < len(self.fases):
            print(self.fases[n_erro])
        else:
            print(self.fases[-1])


# Aparece cada fase do jogo no terminal.
class Fases:
    nome_jogo = "Jogo da Forca"
    level = 1
    banco_de_palavras = "BancoPalavras"
    jogar = False
    arquivo_palavras = ""

    def __init__(self, palavra="", certas="", erradas=""):
        self.palavra = palavra
        self.certas = certas
        self.erradas = erradas

    def tela_inicial(self):
        print(f"\n{'='*30}\n{self.nome_jogo.center(30)}\n{'='*30}\n")
        nivel = input("Escolha o nível de dificuldade (1 - Fácil, 2 - Médio, 3 - Difícil): ")
        self.level = int(nivel)
        self.jogar = True
        return self.level

    def tela_final(self):
        print(f"\nA palavra certa: {self.palavra}")
        print(f"\nLetras certas: {self.certas[:len(self.certas)-2]}")
        print(f"Letras erradas: {self.erradas[:len(self.erradas)-2]}\n")

    def get_jogar(self):
        return self.jogar

    def get_level(self):
        return self.level

    def get_arquivo_palavras(self):
        if self.level == 1:
            return f"{self.banco_de_palavras}/facil"
        elif self.level == 2:
            return f"{self.banco_de_palavras}/medio"
        elif self.level == 3:
            return f"{self.banco_de_palavras}/dificil"
        raise ValueError("Nível inválido.")


# Função principal do jogo da forca usando as classes Palavra, Forca e Fases.
def JogoDaForca():
    while True:
        f = Fases()
        f.tela_inicial()

        palavra = Palavra(f.get_arquivo_palavras()).get_palavra()
        copia_palavra = ["_"] * len(palavra)
        certas = ""
        erradas = ""
        erros = 0
        forca = Forca()

        while erros < 6 and "_" in copia_palavra:
            print(f"\n{' '.join(copia_palavra)}\n")
            letra = input("Digite uma letra: ").lower()

            if letra in palavra:
                if letra not in certas:
                    certas += f"{letra}, "
                for i, char in enumerate(palavra):
                    if char == letra:
                        copia_palavra[i] = letra
            else:
                if letra not in erradas:
                    erradas += f"{letra}, "
                erros += 1

            forca.desenhar_forca(erros)

        f.palavra = palavra
        f.certas = certas
        f.erradas = erradas
        f.tela_final()

        if erros == 6:
            print("Você perdeu!")
        elif "_" not in copia_palavra:
            print("Você ganhou!")

        r = input("Deseja jogar novamente? (s/n): ").lower()
        if r != "s":
            break
        os.system("cls")


if __name__ == "__main__":
    JogoDaForca()

