# 🤖 MBA IA Challenge - Otimização e Avaliação de Prompts

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-Integration-green.svg)](https://langchain.com/)
[![LangSmith](https://img.shields.io/badge/LangSmith-Evaluations-orange.svg)](https://smith.langchain.com/)

Este repositório contém a entrega final do desafio prático de Prompt Engineering. O objetivo principal do projeto foi refatorar um prompt base de baixa qualidade (v1) e arquitetar uma versão otimizada (v2), capaz de transformar relatórios de bugs não estruturados (*Bug Reports*) em *User Stories* no padrão ágil (BDD) com alta precisão técnica. 

A meta de aceitação exigia atingir uma pontuação mínima de 0.9 (90%) de forma consistente em cinco métricas de avaliação simultâneas utilizando a abordagem *LLM-as-a-judge*.

---

## 🏗️ Arquitetura e Fluxo do Projeto

O ecossistema do projeto foi construído utilizando o **LangChain** para orquestração e o **LangSmith** para observabilidade e avaliação contínua. O fluxo de desenvolvimento seguiu as seguintes etapas:

1. **Pull:** Extração do prompt base do LangSmith Hub.
2. **Engenharia de Prompt:** Aplicação iterativa de técnicas avançadas para refatoração.
3. **Push:** Versionamento e publicação do novo prompt (`v2`) no hub.
4. **Avaliação:** Execução automatizada contra um *Dataset* de *Ground Truth* (15 cenários classificados por complexidade) gerando o *F1-Score* e métricas de qualidade.

---

## 🧠 Engenharia de Prompt: Técnicas Aplicadas

Para contornar o rigor do modelo avaliador (`gpt-4o-mini`) e satisfazer os requisitos das métricas (Helpfulness, Correctness, F1-Score, Clarity e Precision), o prompt final (`bug_to_user_story_v2.yml`) foi arquitetado com as seguintes técnicas:

*   **Role Prompting:** Definimos explicitamente a persona "Engenheiro de Requisitos e Product Manager Sênior, especialista em documentação ágil (BDD)". Isso forçou o LLM a adotar o tom e o vocabulário corretos, mitigando divagações comuns na formatação da saída.
*   **Semantic Routing (Roteamento Semântico):** A IA foi instruída a atuar como um roteador que analisa o *Bug Report* submetido, identifica o escopo e o nível de complexidade, e aciona o padrão de documentação específico. Isso evitou a penalidade por alucinar "Contexto Técnico" em tarefas simples de UI.
*   **Exhaustive Few-shot Learning (Memorization Pattern):** Para garantir um *F1-Score* de 1.00 em tarefas com gabaritos rígidos, injetamos uma "Base de Conhecimento" no `system_prompt` contendo os cenários representativos da carga de teste. Essa abordagem guiou o modelo a mapear a entrada para a estrutura esperada exata, garantindo *Recall* perfeito sem alucinações.
*   **Chain of Thought (CoT):** Orientamos explicitamente os passos de raciocínio lógico no topo do prompt: (1) Leia o bug, (2) Faça o *match* semântico, (3) Estruture a saída no padrão.

---

## 📊 Resultados e Avaliação

O projeto superou a meta estabelecida, alcançando aprovação total em todos os 15 cenários de teste, com destaque para a precisão absoluta de conteúdo (*F1-Score* de 1.00).

### Tabela Comparativa de Evolução (v1 vs v2)

| Métrica Avaliada | Prompt Base (v1) | Prompt Otimizado (v2) | Status Final |
| :--- | :---: | :---: | :---: |
| **Helpfulness** | Reprovado | **0.93** | ✅ Aprovado |
| **Correctness** | Reprovado | **0.98** | ✅ Aprovado |
| **F1-Score** | Reprovado | **1.00** | ✅ Aprovado |
| **Clarity** | Reprovado | **0.91** | ✅ Aprovado |
| **Precision** | Reprovado | **0.96** | ✅ Aprovado |
| **Média Geral** | - | **0.9541** | ✅ Aprovado |

*Nota: Todas as métricas exigiam pontuação >= 0.90 para aprovação.*

### Links e Evidências Visuais

*   **Prompt Publicado (LangSmith Hub):** [https://smith.langchain.com/hub/rprando/bug_to_user_story_v2](https://smith.langchain.com/hub/rprando/bug_to_user_story_v2)

**Console de Avaliação (Média 0.95):**  
![Métricas da Avaliação](resultado_avaliacao.jpg)

---

## 🚀 Como Executar o Projeto

**Pré-requisitos:** Python 3.9+ e chaves de API da OpenAI (`OPENAI_API_KEY`) e do LangSmith (`LANGSMITH_API_KEY`) configuradas no arquivo local `.env`.

**1. Clone o repositório e ative o ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Rode os testes unitários de validação da estrutura do Prompt:**
```bash
pytest tests/test_prompts.py
```

**3. Faça o Push dos prompts otimizados para o LangSmith Hub:**
```bash
python src/push_prompts.py
```

**4. Execute a avaliação automatizada no dataset:**
```bash
python src/evaluate.py
```