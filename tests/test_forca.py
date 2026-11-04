
from forca import Forca


def test_desenhar_primeira_fase(capsys):
    forca = Forca()

    forca.desenhar(0)

    saida = capsys.readouterr().out

    assert saida == forca.FASES[0] + "\n"


def test_desenhar_fase_com_um_erro(capsys):
    forca = Forca()

    forca.desenhar(1)

    saida = capsys.readouterr().out

    assert saida == forca.FASES[1] + "\n"


def test_desenhar_fase_com_tres_erros(capsys):
    forca = Forca()

    forca.desenhar(3)

    saida = capsys.readouterr().out

    assert saida == forca.FASES[3] + "\n"


def test_desenhar_ultima_fase(capsys):
    forca = Forca()

    ultimo_indice = len(forca.FASES) - 1

    forca.desenhar(ultimo_indice)

    saida = capsys.readouterr().out

    assert saida == forca.FASES[-1] + "\n"


def test_desenhar_quando_erros_ultrapassam_limite(capsys):
    forca = Forca()

    forca.desenhar(10)

    saida = capsys.readouterr().out

    assert saida == forca.FASES[-1] + "\n"


def test_desenhar_com_numero_erros_igual_ao_total_de_fases(capsys):
    forca = Forca()

    forca.desenhar(len(forca.FASES))

    saida = capsys.readouterr().out

    assert saida.strip() == forca.FASES[-1].strip()
