# Trabalho-N-gramas-IA
# Aplicativo 2: Modelo de Linguagem N-Gramas

**Disciplina:** COMP0427 - Inteligência Artificial  
**Professor:** Prof. Dr. Hendrik Macedo  
**Período:** 2025.2  
**Unidade:** U4  

## Sobre o Projeto

Este repositório contém a implementação do Aplicativo 2, focado no algoritmo de N-Gramas. O objetivo do projeto é aplicar os conceitos de Processamento de Linguagem Natural (NLP) e Modelos de Linguagem Clássicos para construir um gerador de texto probabilístico treinado estritamente com o material didático da disciplina.

### Resumo da Funcionalidade (Algoritmo N-Grama)

O algoritmo implementado atua como um modelo de previsão de texto baseado na Estimativa de Máxima Verossimilhança (MLE - Maximum Likelihood Estimation). Seu funcionamento ocorre nas seguintes etapas:

1. **Extração e Pré-processamento:** O sistema varre uma pasta local (`slides_base`) contendo arquivos em formato PDF, extrai todo o texto bruto, converte para minúsculas e remove pontuações indesejadas, gerando um corpus limpo e unificado.
2. **Treinamento e Contagem:** A aplicação utiliza um modelo de Bigrama (N=2). O algoritmo percorre o texto tokenizado utilizando uma janela deslizante, mapeando cada palavra (histórico) e contabilizando a frequência exata das palavras que a sucedem.
3. **Cálculo de Probabilidade:** Quando o usuário insere uma palavra-chave (semente), o modelo calcula a probabilidade condicional de todos os candidatos possíveis para a próxima palavra, dividindo a contagem da sequência específica pelo total de aparições da palavra de histórico.
4. **Geração Estocástica:** O texto não é gerado de forma determinística. O algoritmo utiliza amostragem a partir da distribuição de probabilidade construída (método da roleta com pesos) para escolher as próximas palavras iterativamente. Ao final, a aplicação exibe a sequência gerada e a probabilidade conjunta da frase existir naquele contexto.

## Estrutura do Repositório

* `ngramas.py`: Módulo principal que contém a classe `ModeloNGrama` com a lógica matemática de MLE, funções de treinamento, pré-processamento e extração de texto de arquivos PDF. A implementação possui comentários que referenciam diretamente o pseudocódigo estudado em aula.
* `main.py`: Script de execução que instancia o modelo, gerencia o fluxo de interação via terminal com o usuário e exibe as estatísticas de probabilidade.
* `slides_base/`: Diretório destinado a armazenar os arquivos `.pdf` que servirão como base de dados (corpus) para o treinamento do modelo.
