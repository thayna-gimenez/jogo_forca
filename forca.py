# Responsável por desenhar a forca conforme os erros do jogador
class Forca:
    FASES = [
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
        """,
    ]

    # Desenha a forca de acordo com o número de erros do jogador
    def desenhar(self, numero_erros):
        if numero_erros < len(self.FASES):
            print(self.FASES[numero_erros])
        else:
            print(self.FASES[-1])
