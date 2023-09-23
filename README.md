# SBEC 2023

**Título:** Ser necessário fazer e ordenar fazer: classificadores gêneros
literários por meio de classes verbais do grego

**Autor:** Caio B. A. Geraldes [<caio.geraldes@usp.br>](mailto:caio.geraldes@usp.br)

## Reproduzindo os resultados

### Dependências

- `wget`
- Distribuição completa `LaTeX`
- `biber` versão `2.17`
- `poetry` versão `1.6.1`.

### Preparando as variáveis de ambiente

```bash
make env
```

### Preparando o ambiente `python`

```bash
make python
```

### Gerando o pdf

Para gerar as figuras, dados e pdf, executar:

```bash
make
```

### Limpando o ambiente

Se por algum motivo for necessário limpar o ambiente (arquivos de
compilação do `LaTeX`, figuras, e dados) rodar:

```bash
make clean
```
