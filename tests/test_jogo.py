
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

# 7. Teste de integração turbinado para matar os mutantes restantes

def test_iniciar_partida_fluxo_completo_vitoria(monkeypatch, capsys):
    import jogo as modulo_jogo
    
    class FasesFalsas:
        def mostrar_tela_inicial(self): pass
        def obter_arquivo_palavras(self): return "caminho/falso.txt"
        def mostrar_tela_final(self): pass

    class ForcaFalsa:
        def desenhar(self, erros): pass

    class PalavraFalsa:
        def __init__(self, arquivo): pass
        def escolher(self): return "oi" # Palavra curta

    monkeypatch.setattr(modulo_jogo, "Palavra", PalavraFalsa)
    jogo = JogoDaForca(fases=FasesFalsas(), forca=ForcaFalsa())

    # Capturamos o texto exato que o jogo tenta passar para o input()
    textos_input = []
    def input_falso(texto):
        textos_input.append(texto)
        return next(entradas)

    entradas = iter(["o", "i"])
    monkeypatch.setattr("builtins.input", input_falso)

    jogo.iniciar_partida()
    
    saida = capsys.readouterr().out

    # 1. Verifica se o tabuleiro com underline foi impresso corretamente
    assert "_ _" in saida 
    
    # 2. Verifica se os textos do input estão EXATOS (mata mutantes 20, 21, 22)
    assert "Digite uma letra: " in textos_input
    assert "XX" not in textos_input[0] # Mata o mutante 20
    assert "d" not in textos_input[0]  # Mata o mutante 21 (que trocou para minúsculo)
    assert "D" in textos_input[0]      # Garante que a primeira letra é maiúscula
    
    # 3. Verifica se a mensagem de vitória está correta (mata mutantes 14, 19, 37, 39)
    assert "Você ganhou!" in saida
    assert "XX" not in saida
  

def test_iniciar_partida_fluxo_completo_derrota(monkeypatch, capsys):
    import jogo as modulo_jogo
    
    class FasesFalsas:
        def mostrar_tela_inicial(self): pass
        def obter_arquivo_palavras(self): return "falso.txt"
        def mostrar_tela_final(self): pass
    
    class ForcaFalsa:
        def desenhar(self, erros): pass
        
    class PalavraFalsa:
        def __init__(self, arquivo): pass
        def escolher(self): return "a"

    monkeypatch.setattr(modulo_jogo, "Palavra", PalavraFalsa)
    jogo = JogoDaForca(fases=FasesFalsas(), forca=ForcaFalsa())

    # Erra 6 vezes
    entradas = iter(["x", "x", "x", "x", "x", "x"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    jogo.iniciar_partida()
    saida = capsys.readouterr().out
    
    assert "Você perdeu!" in saida
    assert "XX" not in saida


# 8. Testes específicos para os mutantes do perguntar_nova_partida e finalizar_partida

def test_perguntar_nova_partida_envia_texto_correto(monkeypatch):
    jogo = criar_jogo()
    texto_recebido = ""
    
    def input_falso(texto):
        nonlocal texto_recebido
        texto_recebido = texto
        return "s"
        
    monkeypatch.setattr("builtins.input", input_falso)
    jogo.perguntar_nova_partida()
    
    # Garante que o texto passado para o input é exatamente o esperado
    assert "Deseja jogar novamente? (s/n): " in texto_recebido
    assert "XX" not in texto_recebido

def test_finalizar_partida_impressoes_exatas(capsys):
    jogo = criar_jogo()
    
    class FasesFalsas:
        def mostrar_tela_final(self): pass
    jogo.fases = FasesFalsas()

    # Testa a derrota
    jogo.finalizar_partida("casa", ["_", "_"], [], [], 6)
    saida_derrota = capsys.readouterr().out
    assert "Você perdeu!" in saida_derrota
    assert "XX" not in saida_derrota # Mata os mutantes do print("XXVocê perdeuXX")

    # Testa a vitória
    jogo.finalizar_partida("casa", ["c", "a", "s", "a"], [], [], 0)
    saida_vitoria = capsys.readouterr().out
    assert "Você ganhou!" in saida_vitoria
    assert "XX" not in saida_vitoria # Mata os mutantes do print("XXVocê ganhouXX")


# 9. Testes para matar mutantes específicos de iniciar_partida

def test_iniciar_partida_verifica_chamadas_internas(monkeypatch):
    import jogo as modulo_jogo
    
    # Listas para capturar os argumentos (Spies)
    captura_arquivo = []
    captura_desenhar = []
    captura_finalizar = []
    captura_processar = []

    class FasesFalsas:
        def mostrar_tela_inicial(self): pass
        def obter_arquivo_palavras(self):
            return "meu_arquivo.txt"  # Valor sentinela
        def mostrar_tela_final(self): pass

    class PalavraFalsa:
        def __init__(self, arquivo):
            captura_arquivo.append(arquivo) # Captura o mutante 2
        def escolher(self): return "ab"

    class ForcaFalsa:
        def desenhar(self, erros):
            captura_desenhar.append(erros) # Captura o mutante 36

    jogo = JogoDaForca(fases=FasesFalsas(), forca=ForcaFalsa())
    monkeypatch.setattr(modulo_jogo, "Palavra", PalavraFalsa)

    # Espiões para métodos do próprio jogo
    def processar_falso(letra, palavra, palavra_oculta, letras_certas, letras_erradas, numero_erros):
        captura_processar.append(numero_erros) # Captura o mutante 9 (inicial)
        # Simula o comportamento real para não travar o loop
        if letra in palavra:
            jogo.revelar_letra(letra, palavra, palavra_oculta)
            if letra not in letras_certas:
                letras_certas.append(letra)
        else:
            if letra not in letras_erradas:
                letras_erradas.append(letra)
            numero_erros += 1
        return numero_erros
    jogo.processar_tentativa = processar_falso

    def finalizar_falso(palavra, palavra_oculta, letras_certas, letras_erradas, numero_erros):
        captura_finalizar.append({
            "palavra": palavra,
            "letras_certas": letras_certas,
            "letras_erradas": letras_erradas
        }) # Captura os mutantes 37, 39 e 40
    jogo.finalizar_partida = finalizar_falso

    # Entradas para vencer rápido ("a" e "b")
    entradas = iter(["a", "b"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    jogo.iniciar_partida()

    # --- Asserções ---
    
    # Mata o mutante 2 (arquivo passado como None)
    assert captura_arquivo[0] == "meu_arquivo.txt"
    
    # Mata o mutante 9 (erros começando em 1 em vez de 0)
    assert captura_processar[0] == 0 
    
    # Mata o mutante 36 (forca desenhada com None)
    assert captura_desenhar[0] == 0
    assert None not in captura_desenhar
    
    # Mata os mutantes 37, 39, 40 (argumentos None no finalizar_partida)
    assert len(captura_finalizar) == 1
    assert captura_finalizar[0]["palavra"] == "ab"
    assert captura_finalizar[0]["letras_certas"] == ["a", "b"]
    assert captura_finalizar[0]["letras_erradas"] == []
    assert None not in captura_finalizar[0].values()
