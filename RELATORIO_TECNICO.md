# Relatório Técnico Breve

## Visão Geral

Este projeto implementa uma pipeline CI/CD para automatizar a preparação do ambiente de testes, a disponibilização do MySQL, a criação do esquema de banco de dados, a execução do código Python responsável pela geração de códigos sequenciais e a execução dos testes automatizados com `pytest`.

## Arquitetura da Solução

- `app.py`: concentra a conexão com o MySQL, a inicialização automática do banco/tabela, a geração do próximo código sequencial, a inserção de registros e as consultas de validação.
- `schema.sql`: cria o banco `db_vvt`, a tabela `codigos_sequenciais` e insere a base de referência inicial.
- `test_gerador_codigo.py`: valida a regra de negócio com testes unitários usando cursor simulado.
- `test_integracao_mysql.py`: valida a conexão com MySQL real, inserções, consultas e incremento do campo `sec`.
- `.github/workflows/main.yml`: orquestra todo o processo em ambiente Linux no GitHub Actions.

## Ferramentas Utilizadas

- Python 3.12
- MySQL 8.0
- Pytest
- mysql-connector-python
- GitHub Actions

## Decisões Técnicas

- O workflow usa GitHub Actions por ser integrado ao repositório e facilitar a demonstração de CI/CD.
- O MySQL é disponibilizado automaticamente no job para garantir repetibilidade do ambiente.
- O script SQL foi deixado idempotente para permitir múltiplas execuções sem destruir o banco nem falhar por duplicidade.
- O `app.py` cria automaticamente o banco e a tabela caso o banco ainda não exista, reduzindo falhas em ambientes novos.
- Os testes foram separados em unitários e de integração para equilibrar velocidade e validação real com banco de dados.

## Desafios Encontrados

- O projeto inicialmente dependia da existência prévia do banco `db_vvt`, o que causava erro de conexão em ambientes limpos.
- O workflow estava restrito à branch `main`, enquanto o repositório de continuidade passou a usar também `master`.
- O script SQL anterior era destrutivo e menos adequado para reexecuções na pipeline.

## Como os Desafios Foram Superados

- Foi implementado bootstrap automático do banco em `app.py`.
- O workflow foi ajustado para disparar em `main` e `master`.
- O `schema.sql` passou a usar `CREATE ... IF NOT EXISTS` e `INSERT IGNORE`.
- A pipeline passou a validar explicitamente a disponibilidade do MySQL, a aplicação do schema e a execução dos testes.

## Resultado

A solução atende aos requisitos do trabalho ao automatizar o ambiente Linux de CI, preparar o MySQL, criar o banco e a tabela, validar a conexão Python-MySQL, gerar códigos sequenciais corretamente e executar os testes automatizados com sucesso.
