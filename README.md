# Trabalho 3 - VV&T: Pipeline CI/CD com MySQL, Python e Pytest

Este projeto implementa uma solução completa para o trabalho de VV&T com foco em:

- provisionamento automatizado do ambiente Linux via pipeline
- inicialização de um servidor MySQL
- criação automática do banco de dados e da tabela `codigos_sequenciais`
- geração de códigos sequenciais no formato `PAIS + GRUPO + SEQUENCIA_4_DIGITOS + TIPO_ALIMENTO`
- execução de testes automatizados com `pytest`
- validação por query após inserção real no banco

## Estrutura do Projeto

- `.github/workflows/main.yml`: pipeline CI/CD
- `schema.sql`: criação do banco e da tabela
- `app.py`: conexão com MySQL, geração de código, inserção e consulta
- `test_gerador_codigo.py`: testes unitários
- `test_integracao_mysql.py`: testes de integração com MySQL real
- `RELATORIO_TECNICO.md`: relatório técnico breve

## Requisitos

- Python 3.10+
- MySQL 8.0+
- Dependências em `requirements.txt`

## Execução local

## Instalação e Configuração

1. **Instalar dependências Python:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar MySQL:**
   - Certifique-se de que o MySQL está rodando.
   - Execute o script `schema.sql` para criar o banco e tabela:
     ```bash
     mysql -u root -p < schema.sql
     ```

3. **Configurar variáveis de ambiente (opcional):**
   ```bash
   export MYSQL_HOST=localhost
   export MYSQL_USER=root
   export MYSQL_PASSWORD=sua_senha
   export MYSQL_DATABAS=db_vvt
   ```

## Como Executar

1. **Executar o script principal (inserir um produto de exemplo):**
   ```bash
   python app.py
   ```

2. **Executar os testes:**
   ```bash
   python -m pytest -q
   ```

## Funcionalidades

- **Geração de Código:** Calcula automaticamente o próximo código sequencial para um grupo de produtos, com formato `PAÍS+GRUPO+SEQUÊNCIA_4DIG+TIPO_ALIMENTO`.
- **Validação:** Verifica parâmetros de entrada e previne duplicidade.
- **Testes Isolados:** Utiliza mocks para testar sem depender de banco real.

## Resultados dos Testes

```
........                                                                 [100%]
8 passed in 0.05s
```

## Entrega

O documento `ENTREGA_FINAL.docx` contém todos os códigos, explicações e resultados conforme solicitado no enunciado.

## Autor

Samuel VPS