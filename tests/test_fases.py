
import pytest
from fases import Fases


# 1. Testes do construtor

def test_inicializar_fases():
    fases = Fases()

    assert fases.nivel is None
    assert fases.palavra == ""
    assert fases.letras_certas == []
    assert fases.letras_erradas == []


# 2. Testes de mostrar_tela_inicial

def test_mostrar_tela_inicial_com_nivel_facil(capsys, monkeypatch):
    fases = Fases()
    prompts = []

    def entrada_falsa(prompt):
        prompts.append(prompt)
        return "1"

    monkeypatch.setattr("builtins.input", entrada_falsa)

    fases.mostrar_tela_inicial()

    saida = capsys.readouterr().out

    assert fases.nivel == 1
    assert "Jogo da Forca" in saida
    assert saida.count("=" * fases.LARGURA_TITULO) == 2
    assert prompts == [
     "Escolha o nível de dificuldade (1 - Fácil, 2 - Médio, 3 - Difícil): "
    ]

def test_mostrar_tela_inicial_com_nivel_medio(monkeypatch):
    fases = Fases()

    monkeypatch.setattr("builtins.input", lambda _: "2")

    fases.mostrar_tela_inicial()

    assert fases.nivel == 2


def test_mostrar_tela_inicial_com_nivel_dificil(monkeypatch):
    fases = Fases()

    monkeypatch.setattr("builtins.input", lambda _: "3")

    fases.mostrar_tela_inicial()

    assert fases.nivel == 3


def test_mostrar_tela_inicial_com_entrada_nao_numerica(monkeypatch):
    fases = Fases()

    monkeypatch.setattr("builtins.input", lambda _: "abc")

    with pytest.raises(ValueError):
        fases.mostrar_tela_inicial()


# 3. Testes de mostrar_tela_final

def test_mostrar_tela_final(capsys):
    fases = Fases()

    fases.palavra = "casa"
    fases.letras_certas = ["c", "a", "s"]
    fases.letras_erradas = ["x", "y"]

    fases.mostrar_tela_final()

    saida = capsys.readouterr().out

    assert "A palavra certa: casa" in saida
    assert "Letras certas: c, a, s" in saida
    assert "Letras erradas: x, y" in saida


def test_mostrar_tela_final_sem_letras_certas_ou_erradas(capsys):
    fases = Fases()

    fases.palavra = "sol"
    fases.letras_certas = []
    fases.letras_erradas = []

    fases.mostrar_tela_final()

    saida = capsys.readouterr().out

    assert "A palavra certa: sol" in saida
    assert "Letras certas:" in saida
    assert "Letras erradas:" in saida


# 4. Testes de obter_arquivo_palavras

def test_obter_arquivo_palavras_nivel_facil():
    fases = Fases()
    fases.nivel = 1

    assert fases.obter_arquivo_palavras() == "BancoPalavras/facil"


def test_obter_arquivo_palavras_nivel_medio():
    fases = Fases()
    fases.nivel = 2

    assert fases.obter_arquivo_palavras() == "BancoPalavras/medio"


def test_obter_arquivo_palavras_nivel_dificil():
    fases = Fases()
    fases.nivel = 3

    assert fases.obter_arquivo_palavras() == "BancoPalavras/dificil"


def test_obter_arquivo_palavras_com_nivel_invalido():
    fases = Fases()
    fases.nivel = 4

    with pytest.raises(ValueError) as erro:
        fases.obter_arquivo_palavras()

    assert str(erro.value) == "Nível inválido."


def test_obter_arquivo_palavras_sem_nivel_selecionado():
    fases = Fases()

    with pytest.raises(ValueError):
        fases.obter_arquivo_palavras()
