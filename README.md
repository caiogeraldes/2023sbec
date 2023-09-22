# SBEC 2023: Ser necessário fazer e ordenar fazer: classificadores gêneros literários por meio de classes verbais do grego

**Autor**: Caio B. A. Geraldes [<caio.geraldes@usp.br>](mailto:caio.geraldes@usp.br)

<!--toc:start-->
- [SBEC 2023: Ser necessário fazer e ordenar fazer: classificadores gêneros literários por meio de classes verbais do grego](#sbec-2023-ser-necessário-fazer-e-ordenar-fazer-classificadores-gêneros-literários-por-meio-de-classes-verbais-do-grego)
  - [Reproduzindo os resultados](#reproduzindo-os-resultados)
    - [Dados Diorisis](#dados-diorisis)
    - [Ambiente `python`](#ambiente-python)
<!--toc:end-->

Para gerar as figuras, dados e pdf, executar:

```bash
make
```

Para limpar os arquivos de compilação do `LaTeX`, executar:

```bash
make clean
```

## Reproduzindo os resultados

### Dados Diorisis

Baixe o corpus Diorisis do [repositório dos autores](https://figshare.com/articles/dataset/The_Diorisis_Ancient_Greek_Corpus_JSON_/12251468), copie para `./dados/diorisis/` e exclua os textos que não interessam ao modelo.

Se houver acesso ao comando `wget`, utilizar:

```bash
make diorisis
```

### Ambiente `python`

Dependências:
 - Python
