# Jogo da Forca

Jogo da forca desenvolvido na linguagem Python, com o objetivo de aplicar os princípios de manutenção de software e realizar testes baseados em defeitos.

## Estrutura

- `main.py`: ponto de entrada do programa.
- `jogo.py`: fluxo e regras da partida de forca.
- `palavra.py`: leitura e escolha das palavras de acordo com o banco de dados.
- `forca.py`: desenhos da forca de acordo com os erros do jogador.
- `fases.py`: criação e manipulação de telas e seleção do nível.
- `BancoPalavras/`: arquivos de palavras para o jogo.

## Princípios aplicados

Foram aplicadas no código as seis premissas apresentadas no capítulo 2 do livro “Fundamentos de Manutenção de Software”, com base no guia de estilo para Python da Google. As seis premissas são:

1. **Verificadores de estilo e formatadores**
2. **Nomes legíveis**
3. **Evitar números mágicos**
4. **Linguagem ubíqua**
5. **Funções coesas e desacopladas**
6. **Separação dos fluxos de execução**

## Mutações

Para o teste de mutação foi utilizada a ferramenta [MutMut](https://github.com/boxed/mutmut). Inicialmente, foram criados casos de teste para grande parte do código. Após analisar os mutantes vivos, novos casos de teste foram adicionados e os antigos foram alterados, de forma a alcançar o maior número possível de mutantes mortos. O escore inicial de mutação foi de 0,84, posteriormente alcançando 1.

## Requisitos

Antes de executar o projeto, é necessário ter instalado:

* Python 3.8 ou superior
* pip

Caso o sistema do usuário seja Windows, é necessário executar o código em ambiente WSL.

## Instalação e execução

O código deve ser executado pelo usuário root.

Primeiramente, crie um ambiente virtual.
```
python3 -m venv .venv
source .venv/bin/activate
```

Instale o framework e ferramenta necessários.
```
pip install pytest
pip install mutmut
```

Realize os testes automatizados com pytest.
```
python3 -m pytest -v
```

Crie os mutantes e analise os mutantes sobreviventes.
```
mutmut run
mutmut browse
```