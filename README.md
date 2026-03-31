# Trabalho 3 - VV&T: Pipeline CI/CD com MySQL, Python e Pytest

Este projeto implementa uma solução completa para o trabalho de VV&T com foco em:

- provisionamento automatizado do ambiente Linux via GitHub Actions
- inicialização de um servidor MySQL para o ambiente de testes
- criação automática do banco de dados, da tabela `codigos_sequenciais` e carga inicial dos registros padrão
- geração de códigos sequenciais no formato `PAIS + GRUPO + SEQUENCIA_4_DIGITOS + TIPO_ALIMENTO`
- execução de testes automatizados com `pytest`
- validação por query após inserção real no banco

## Estrutura do Projeto

- `.github/workflows/main.yml`: pipeline CI/CD
- `schema.sql`: criação do banco, tabela e dados iniciais
- `app.py`: conexão com MySQL, bootstrap do banco, geração de código, inserção e consulta
- `test_gerador_codigo.py`: testes unitários da regra de negócio
- `test_integracao_mysql.py`: testes de integração com MySQL real
- `RELATORIO_TECNICO.md`: relatório técnico breve

## Requisitos

- Python 3.10+
- MySQL 8.0+
- Dependências em `requirements.txt`

## Instalação e Configuração Local

1. Instalar dependências Python:
   ```bash
   pip install -r requirements.txt
   ```

2. Garantir que o MySQL esteja em execução.

3. Aplicar o script SQL para criar ou atualizar o banco, a tabela e os registros iniciais:
   ```bash
   mysql -u root -p < schema.sql
   ```

4. Configurar variáveis de ambiente, se necessário:
   ```bash
   export MYSQL_HOST=localhost
   export MYSQL_USER=root
   export MYSQL_PASSWORD=sua_senha
   export MYSQL_DATABASE=db_vvt
   ```

## Execução

O `app.py` também consegue criar automaticamente o banco e a tabela caso `db_vvt` ainda não exista.

1. Executar o script principal:
   ```bash
   python app.py
   ```

2. Executar os testes:
   ```bash
   python -m pytest -q
   ```

## Cobertura dos Requisitos do Trabalho

- Ambiente Linux automatizado pela pipeline em `.github/workflows/main.yml`
- MySQL configurado automaticamente no job de CI
- Script SQL com criação de banco e tabela em `schema.sql`
- Conexão Python-MySQL implementada em `app.py`
- Função de geração de código sequencial implementada e testada
- Testes unitários e de integração executados com `pytest`

## Resultado Atual dos Testes

```
..............                                                           [100%]
14 passed in 0.25s
```

## Entregáveis

- Pipeline CI/CD
- Script SQL
- Código Python de conexão e geração
- Testes automatizados com pytest
- Relatório técnico breve

## Autor

Samuel VPS
