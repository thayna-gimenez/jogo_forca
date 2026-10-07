# Controla as telas e as configurações da partida
class Fases:
    NOME_JOGO = "Jogo da Forca"
    BANCO_DE_PALAVRAS = "BancoPalavras"
    NIVEL_FACIL = 1
    NIVEL_MEDIO = 2
    NIVEL_DIFICIL = 3
    LARGURA_TITULO = 30

    def __init__(self):
        self.nivel = None
        self.palavra = ""
        self.letras_certas = []
        self.letras_erradas = []

    # Mostra a tela inicial do jogo e solicita ao jogador que escolha o nível de dificuldade
    def mostrar_tela_inicial(self):
        print(
            f"\n{'=' * self.LARGURA_TITULO}\n"
            f"{self.NOME_JOGO.center(self.LARGURA_TITULO)}\n"
            f"{'=' * self.LARGURA_TITULO}\n"
        )
        self.nivel = int(
            input("Escolha o nível de dificuldade (1 - Fácil, 2 - Médio, 3 - Difícil): ")
        )

    # Mostra a tela final do jogo, com a palavra correta e as letras acertadas e erradas
    def mostrar_tela_final(self):
        print(f"\nA palavra certa: {self.palavra}")
        print(f"Letras certas: {', '.join(self.letras_certas)}")
        print(f"Letras erradas: {', '.join(self.letras_erradas)}\n")

    # Obtém o arquivo de palavras correspondente ao nível escolhido pelo jogador
    def obter_arquivo_palavras(self):
        arquivos_por_nivel = {
            self.NIVEL_FACIL: f"{self.BANCO_DE_PALAVRAS}/facil",
            self.NIVEL_MEDIO: f"{self.BANCO_DE_PALAVRAS}/medio",
            self.NIVEL_DIFICIL: f"{self.BANCO_DE_PALAVRAS}/dificil",
        }

        if self.nivel not in arquivos_por_nivel:
            raise ValueError("Nível inválido.")

        return arquivos_por_nivel[self.nivel]
