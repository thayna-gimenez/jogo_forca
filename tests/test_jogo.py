
import jogo as modulo_jogo
from jogo import JogoDaForca


def criar_jogo():
    return JogoDaForca(fases=None, forca=None)


# 1. Testes de partida_em_andamento

def test_partida_continua_com_erros_e_letras_ocultas():
    jogo = criar_jogo()

    resultado = jogo.partida_em_andamento(["_", "_", "_"], 0)

    assert resultado is True


def test_partida_termina_ao_atingir_maximo_erros():
    jogo = criar_jogo()

    resultado = jogo.partida_em_andamento(["_", "_", "_"], 6)

    assert resultado is False


def test_partida_termina_quando_todas_as_letras_sao_reveladas():
    jogo = criar_jogo()

    resultado = jogo.partida_em_andamento(["c", "a", "s", "a"], 0)

    assert resultado is False


def test_partida_continua_com_cinco_erros_e_letras_ocultas():
    jogo = criar_jogo()

    resultado = jogo.partida_em_andamento(["_", "_", "_"], 5)

    assert resultado is True


# 2. Testes de processar_tentativa

def test_processar_letra_correta():
    jogo = criar_jogo()
    palavra_oculta = ["_", "_", "_", "_"]
    letras_certas = []
    letras_erradas = []

    erros = jogo.processar_tentativa(
        "a", "casa", palavra_oculta,
        letras_certas, letras_erradas, 0
    )

    assert palavra_oculta == ["_", "a", "_", "a"]
    assert letras_certas == ["a"]
    assert letras_erradas == []
    assert erros == 0


def test_processar_letra_incorreta():
    jogo = criar_jogo()
    palavra_oculta = ["_", "_", "_"]
    letras_certas = []
    letras_erradas = []

    erros = jogo.processar_tentativa(
        "x", "sol", palavra_oculta,
        letras_certas, letras_erradas, 0
    )

    assert palavra_oculta == ["_", "_", "_"]
    assert letras_certas == []
    assert letras_erradas == ["x"]
    assert erros == 1


def test_letra_correta_repetida_nao_e_adicionada_novamente():
    jogo = criar_jogo()
    palavra_oculta = ["_", "_", "_", "_"]
    letras_certas = ["a"]
    letras_erradas = []

    erros = jogo.processar_tentativa(
        "a", "casa", palavra_oculta,
        letras_certas, letras_erradas, 0
    )

    assert letras_certas == ["a"]
    assert erros == 0


def test_letra_incorreta_repetida_nao_e_adicionada_novamente():
    jogo = criar_jogo()
    palavra_oculta = ["_", "_", "_"]
    letras_certas = []
    letras_erradas = ["x"]

    erros = jogo.processar_tentativa(
        "x", "sol", palavra_oculta,
        letras_certas, letras_erradas, 0
    )

    assert letras_erradas == ["x"]

    # Comportamento atual do código:
    # a tentativa repetida também incrementa os erros.
    assert erros == 1


def test_letra_incorreta_repetida_incrementa_erros_novamente():
    jogo = criar_jogo()
    palavra_oculta = ["_", "_", "_"]
    letras_certas = []
    letras_erradas = ["x"]

    erros = jogo.processar_tentativa(
        "x", "sol", palavra_oculta,
        letras_certas, letras_erradas, 2
    )

    assert erros == 3


# 3. Testes de revelar_letra

def test_revelar_letra_em_todas_as_posicoes():
    jogo = criar_jogo()
    palavra_oculta = ["_", "_", "_", "_"]

    jogo.revelar_letra("a", "casa", palavra_oculta)

    assert palavra_oculta == ["_", "a", "_", "a"]


def test_revelar_letra_que_nao_existe_na_palavra():
    jogo = criar_jogo()
    palavra_oculta = ["_", "_", "_"]

    jogo.revelar_letra("x", "sol", palavra_oculta)

    assert palavra_oculta == ["_", "_", "_"]


# 4. Testes de finalizar_partida

def test_finalizar_partida_mostra_mensagem_de_vitoria(capsys):
    jogo = criar_jogo()

    class FasesFalsas:
        def mostrar_tela_final(self):
            pass

    jogo.fases = FasesFalsas()

    jogo.finalizar_partida(
        "casa",
        ["c", "a", "s", "a"],
        ["c", "a", "s"],
        [],
        0
    )

    saida = capsys.readouterr().out

    assert "Você ganhou!" in saida
    assert "Você perdeu!" not in saida
    assert jogo.fases.palavra == "casa"
    assert jogo.fases.letras_certas == ["c", "a", "s"]
    assert jogo.fases.letras_erradas == []


def test_finalizar_partida_mostra_mensagem_de_derrota(capsys):
    jogo = criar_jogo()

    class FasesFalsas:
        def mostrar_tela_final(self):
            pass

    jogo.fases = FasesFalsas()

    jogo.finalizar_partida(
        "casa",
        ["_", "_", "_", "_"],
        [],
        ["x", "y", "z"],
        6
    )

    saida = capsys.readouterr().out

    assert "Você perdeu!" in saida
    assert "Você ganhou!" not in saida
    assert jogo.fases.palavra == "casa"


def test_finalizar_partida_nao_mostra_vitoria_ou_derrota(capsys):
    jogo = criar_jogo()

    class FasesFalsas:
        def mostrar_tela_final(self):
            pass

    jogo.fases = FasesFalsas()

    jogo.finalizar_partida(
        "casa",
        ["c", "a", "_", "a"],
        ["c", "a"],
        ["x"],
        1
    )

    saida = capsys.readouterr().out

    assert "Você ganhou!" not in saida
    assert "Você perdeu!" not in saida


# 5. Testes de perguntar_nova_partida

def test_perguntar_nova_partida_com_resposta_sim(monkeypatch):
    jogo = criar_jogo()

    monkeypatch.setattr("builtins.input", lambda _: "s")

    assert jogo.perguntar_nova_partida() is True


def test_perguntar_nova_partida_com_resposta_nao(monkeypatch):
    jogo = criar_jogo()

    monkeypatch.setattr("builtins.input", lambda _: "n")

    assert jogo.perguntar_nova_partida() is False


def test_perguntar_nova_partida_converte_resposta_para_minusculo(monkeypatch):
    jogo = criar_jogo()

    monkeypatch.setattr("builtins.input", lambda _: "S")

    assert jogo.perguntar_nova_partida() is True


# 6. Teste de iniciar

def test_iniciar_pergunta_se_jogador_deseja_jogar_novamente(monkeypatch):
    jogo = criar_jogo()
    partidas_iniciadas = []
    respostas = iter([True, False])

    def iniciar_partida_falsa():
        partidas_iniciadas.append(True)

    jogo.iniciar_partida = iniciar_partida_falsa
    jogo.perguntar_nova_partida = lambda: next(respostas)

    comandos_sistema = []
    monkeypatch.setattr(
        modulo_jogo.os,
        "system",
        lambda comando: comandos_sistema.append(comando)
    )

    jogo.iniciar()

    assert len(partidas_iniciadas) == 2
    assert comandos_sistema == ["cls"]
