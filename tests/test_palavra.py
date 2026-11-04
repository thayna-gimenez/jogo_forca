
import pytest
from palavra import Palavra


# 1. Testes do construtor

def test_caminho_sem_extensao_txt():
    palavra = Palavra("BancoPalavras/facil")

    assert palavra.caminho == "BancoPalavras/facil.txt"


def test_caminho_com_extensao_txt():
    palavra = Palavra("BancoPalavras/facil.txt")

    assert palavra.caminho == "BancoPalavras/facil.txt"


# 2. Testes de escolher

def test_escolher_palavra_do_arquivo(tmp_path, monkeypatch):
    arquivo = tmp_path / "palavras.txt"
    arquivo.write_text("casa\nbola\ncarro\n", encoding="utf-8")

    palavra = Palavra(str(arquivo))

    monkeypatch.setattr(
        "palavra.random.choice",
        lambda palavras: palavras[0]
    )

    assert palavra.escolher() == "casa"


def test_escolher_ignora_linhas_vazias(tmp_path, monkeypatch):
    arquivo = tmp_path / "palavras.txt"
    arquivo.write_text(
        "\ncasa\n\nbola\n\n",
        encoding="utf-8"
    )

    palavra = Palavra(str(arquivo))

    def escolher_primeira(palavras):
        assert palavras == ["casa", "bola"]
        return palavras[0]

    monkeypatch.setattr(
        "palavra.random.choice",
        escolher_primeira
    )

    assert palavra.escolher() == "casa"


def test_escolher_palavra_remove_espacos_das_linhas(
    tmp_path, monkeypatch
):
    arquivo = tmp_path / "palavras.txt"
    arquivo.write_text(
        "  casa  \n  bola  \n",
        encoding="utf-8"
    )

    palavra = Palavra(str(arquivo))

    def escolher_primeira(palavras):
        assert palavras == ["casa", "bola"]
        return palavras[0]

    monkeypatch.setattr(
        "palavra.random.choice",
        escolher_primeira
    )

    assert palavra.escolher() == "casa"


def test_arquivo_vazio_gera_value_error(tmp_path):
    arquivo = tmp_path / "palavras.txt"
    arquivo.write_text("", encoding="utf-8")

    palavra = Palavra(str(arquivo))

    with pytest.raises(ValueError, match="O arquivo de palavras está vazio."):
        palavra.escolher()


def test_arquivo_apenas_com_linhas_vazias_gera_value_error(tmp_path):
    arquivo = tmp_path / "palavras.txt"
    arquivo.write_text("\n\n   \n", encoding="utf-8")

    palavra = Palavra(str(arquivo))

    with pytest.raises(ValueError):
        palavra.escolher()


def test_arquivo_inexistente_gera_file_not_found_error(tmp_path):
    caminho = tmp_path / "inexistente.txt"
    palavra = Palavra(str(caminho))

    with pytest.raises(FileNotFoundError):
        palavra.escolher()
