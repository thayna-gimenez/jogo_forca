
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

from unittest.mock import patch, mock_open
import pytest
from palavra import Palavra

# ... (mantenha os seus testes anteriores) ...

# 3. Testes para matar os mutantes de encoding (5, 6, 10)

@patch("builtins.open", new_callable=mock_open, read_data="casa\nbola\n")
def test_escolher_usa_encoding_utf_8_corretamente(mock_file):
    palavra = Palavra("falso.txt")
    palavra.escolher()
    
    # Verifica se o open() foi chamado exatamente com encoding="utf-8"
    mock_file.assert_called_once_with("falso.txt", "r", encoding="utf-8")


def test_escolher_com_arquivo_encoding_invalido_gera_erro(tmp_path):
    arquivo = tmp_path / "palavras.txt"
    # Escreve bytes inválidos para UTF-8
    arquivo.write_bytes(b"\xff\xfe\xfa\xfb")
    
    palavra = Palavra(str(arquivo))
    
    # Se o mutante remover o encoding="utf-8", o Python pode tentar ler com o encoding padrão do sistema 
    # e não dar erro. Forçando o erro, garantimos que o parâmetro está lá.
    with pytest.raises(UnicodeDecodeError):
        palavra.escolher()


# 4. Testes para matar os mutantes do ValueError (3 e 14)

def test_arquivo_vazio_mensagem_de_erro_exata(tmp_path):
    arquivo = tmp_path / "palavras.txt"
    arquivo.write_text("", encoding="utf-8")
    palavra = Palavra(str(arquivo))

    with pytest.raises(ValueError) as exc_info:
        palavra.escolher()
    
    # Usa == em vez de match para garantir que não tem nenhum "XX" extra
    assert str(exc_info.value) == "O arquivo de palavras está vazio."


def test_arquivo_apenas_linhas_vazias_mensagem_exata(tmp_path):
    arquivo = tmp_path / "palavras.txt"
    arquivo.write_text("\n\n   \n", encoding="utf-8")
    palavra = Palavra(str(arquivo))

    with pytest.raises(ValueError) as exc_info:
        palavra.escolher()
        
    assert str(exc_info.value) == "O arquivo de palavras está vazio."
