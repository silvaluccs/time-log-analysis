# 🕐 Time Log Analysis

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)

Aplicação containerizada para análise de registros de timesheet. Lê um arquivo JSON com entradas de tempo, processa as informações e gera um relatório analítico completo em JSON.

---

## 📋 Sobre o projeto

A aplicação recebe um conjunto de registros de tempo trabalhado por funcionários em tarefas, filtra entradas inválidas e produz um resumo com rankings, percentuais e estatísticas agregadas.

### O que é gerado no relatório

- **Total de minutos** trabalhados no período
- **Tarefas** com total de minutos e percentual sobre o geral
- **Tarefa mais trabalhada** do período
- **Top 3 tarefas** por minutos com percentual formatado
- **Top 3 funcionários** com maior total de minutos
- **Funcionário com mais tarefas distintas** e a lista de tarefas
- **Quantidade de registros ignorados** por dados inválidos

---

## 🗂 Estrutura do projeto

```
.
├── src/
│   ├── filter.py        # Carregamento e filtragem dos dados
│   ├── aggregator.py    # Agrupamentos, rankings e cálculos
│   └── app.py           # Pipeline principal e escrita do resultado
├── main.py              # Entrypoint da aplicação
├── data.json            # Arquivo de entrada com os registros
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🔄 Como funciona

```
data.json
    │
    ▼
[ Filtragem ]
  Remove registros com minutes <= 0
    │
    ▼
[ Agregação ]
  Agrupa por tarefa e por funcionário
  Calcula totais, percentuais e rankings
    │
    ▼
[ Resultado ]
  Salva result.json com o resumo analítico
```

---

## 🚀 Como executar

### Pré-requisitos

- [Docker](https://www.docker.com/) instalado
- [Docker Compose](https://docs.docker.com/compose/) instalado

### Executar

```bash
docker compose up --build
```

O arquivo `result.json` será gerado automaticamente na raiz do projeto após a execução.

---

## 📁 Arquivos

| Arquivo | Descrição |
|---|---|
| `data.json` | Arquivo de entrada com os registros de timesheet |
| `result.json` | Arquivo de saída gerado pela aplicação |

---

## 📊 Estrutura do result.json

```json
{
  "totalMinutes": 28408,
  "tasks": [...],
  "mostWorkedTask": {...},
  "top3TasksPercentage": [...],
  "top3Employees": [...],
  "mostDistinctUserOnTasks": {...},
  "ignoredRecords": 41
}
```

---
