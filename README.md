# Sistema de Gerenciamento de Peças com controle de qualidade e automação de armazenamento em caixas, desenvolvido em Python com SQLite.

**Aluna:** Eugenia Kazue Takara Stefens  
**R.A.:** 237219  
**Disciplina:** Algoritmos e Lógica de Programação

---

## Descrição do Projeto

Este projeto foi desenvolvido em Python como um protótipo de automação digital para controle de produção e qualidade de peças em uma linha de montagem industrial.

O sistema automatiza o processo de inspeção, classificando as peças como aprovadas ou reprovadas com base em critérios definidos, organizando as peças aprovadas em caixas e gerando relatórios consolidados.

---

## Objetivo

Automatizar o controle de qualidade e armazenamento de peças, reduzindo erros manuais e melhorando a organização da produção.

---

## Regras de Aprovação

Uma peça é considerada **aprovada** quando atende a todos os critérios abaixo:

- Peso entre 95g e 105g
- Cor azul ou verde
- Comprimento entre 10cm e 20cm

Caso algum critério não seja atendido, a peça será reprovada, e o sistema registrará o motivo.

---

## Funcionalidades

- 1. Cadastrar nova peça
- 2. Listar peças aprovadas/reprovadas
- 3. Remover peça cadastrada
- 4. Listar caixas fechadas
- 5. Gerar relatório final
- 6. Listar caixa aberta (extra)
- 0. Sair

---

## Arquivos do Projeto

O projeto é composto pelos seguintes arquivos:

- `trabalhoAlgoritmoLogicaProgramacao4.py` -> código principal do sistema
- `pecas.db` -> banco de dados SQLite com as informações das peças e caixas

---

## Estrutura do Sistema

### Tabela `pecas`

- ID automático (O campo ID das peças é gerado automaticamente pelo banco de dados)
- peso
- cor
- comprimento
- status
- motivos
- caixa associada

### Tabela `caixas`

- ID automático (O campo ID das caixas é gerado automaticamente pelo banco de dados)
- status (aberta ou fechada)

---

## Explicação do Funcionamento

O sistema recebe os dados de cada peça produzida e verifica automaticamente se ela atende aos critérios de qualidade definidos no projeto.

O ID da peça é gerado automaticamente pelo SQLite.

Se a peça estiver dentro dos padrões de peso, cor e comprimento, ela é classificada como **Aprovada** e armazenada em uma caixa aberta. Cada caixa suporta até 10 peças. Quando esse limite é atingido, a caixa é fechada automaticamente e o sistema passa a utilizar uma nova caixa.

Se a peça não atender aos critérios, ela é classificada como **Reprovada** e o sistema registra os motivos da reprovação.

O sistema também garante integridade dos dados ao impedir a remoção de peças que pertencem a caixas já fechadas.

Além disso, o sistema permite:

- listar peças aprovadas e reprovadas
- remover peças cadastradas
- listar caixas fechadas
- listar a caixa aberta atual
- gerar relatório final com resumo da produção

---

## Tecnologias Utilizadas

- Python 3
- SQLite
- Colorama

---

## Como Rodar o Programa

### 1. Instalar o Python

No terminal, verifique se o Python está instalado:

```bash
python --version
```

### 2. Instalar a biblioteca Colorama

No terminal, execute:

```bash
python -m pip install colorama
```

### 3. Certificar-se de que os arquivos estão na mesma pasta

Os arquivos abaixo devem estar juntos no mesmo diretório:

- `trabalhoAlgoritmoLogicaProgramacao4.py`
- `pecas.db`

### 4. Executar o programa

No terminal, execute:

```bash
python trabalhoAlgoritmoLogicaProgramacao4.py
```

---

## Exemplos de Entradas e Saídas

### Exemplo 1 - Cadastro de peça aprovada

**Entrada:**

- Peso: 100
- Cor: azul
- Comprimento: 15

**Saída esperada:**

- Peça cadastrada com sucesso
- Status: Aprovada
- Peça armazenada em uma caixa aberta

---

### Exemplo 2 - Cadastro de peça reprovada por peso

**Entrada:**

- Peso: 110
- Cor: azul
- Comprimento: 15

**Saída esperada:**

- Peça cadastrada com sucesso
- Status: Reprovada
- Motivo: Peso fora do intervalo permitido (95g a 105g)

---

### Exemplo 3 - Cadastro de peça reprovada por cor

**Entrada:**

- Peso: 100
- Cor: vermelha
- Comprimento: 15

**Saída esperada:**

- Peça cadastrada com sucesso
- Status: Reprovada
- Motivo: Cor inválida (somente azul ou verde)

---

### Exemplo 4 - Cadastro de peça reprovada por comprimento

**Entrada:**

- Peso: 100
- Cor: verde
- Comprimento: 25

**Saída esperada:**

- Peça cadastrada com sucesso
- Status: Reprovada
- Motivo: Comprimento fora do intervalo permitido (10cm a 20cm)

---

### Exemplo 5 - Fechamento automático de caixa

**Entrada:**

- Cadastro de 10 peças aprovadas

**Saída esperada:**

- As 10 peças são armazenadas na mesma caixa
- Ao cadastrar a décima peça, a caixa é fechada automaticamente

---

### Exemplo 6 - Relatório final

**Saída esperada:**

- Total de peças cadastradas
- Total de peças aprovadas
- Total de peças reprovadas
- Quantidade de caixas fechadas
- Quantidade de caixas utilizadas
- Motivos de reprovação

---

## Boas Práticas Aplicadas

- Uso de funções
- Banco de dados SQLite
- Validação de entrada
- Uso de `with sqlite3.connect(...)`
- Organização do código

---

## Possíveis Melhorias Futuras

- Interface gráfica
- Integração com sensores
- Uso de inteligência artificial

---

## Referências

- https://docs.python.org/3/
- https://python.org.br/
