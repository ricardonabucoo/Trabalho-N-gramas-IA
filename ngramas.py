import random
import re
import os
import PyPDF2
from collections import defaultdict

def ler_slides_da_pasta(caminho_pasta):
    texto_geral = ""
    for nome_arquivo in os.listdir(caminho_pasta):
        if nome_arquivo.lower().endswith('.pdf'):
            caminho_pdf = os.path.join(caminho_pasta, nome_arquivo)
            try:
                with open(caminho_pdf, 'rb') as arquivo:
                    leitor = PyPDF2.PdfReader(arquivo)
                    for pagina in leitor.pages:
                        texto = pagina.extract_text()
                        if texto:
                            texto_geral += texto + " "
            except Exception as e:
                print(f"Ops, erro ao ler o arquivo {nome_arquivo}: {e}")
    
    return texto_geral


class ModeloNGrama:
    def __init__(self, n):
        self.n = n
        self.counts = defaultdict(lambda: defaultdict(int))
        self.context_totals = defaultdict(int)

    def limpar_e_tokenizar(self, texto):
        # tokens <- PREPROCESS-AND-TOKENIZE(corpus)
        texto = texto.lower()
        
        # Mantém todo o texto intacto, removendo apenas a pontuação 
        # (para evitar bugs quando o usuário digitar palavras no terminal)
        texto = re.sub(r'[^\w\s]', ' ', texto) 
        texto = re.sub(r'\s+', ' ', texto) 
        
        return texto.split()
         #buscando adequeação com a referência do pseudocódigo. Um pouco literal, mas ok
    def treinar(self, corpus):
        # Referência: function TRAIN-NGRAM-MODEL(corpus, n) returns a model
        tokens = self.limpar_e_tokenizar(corpus)
        
        vocabulario_unico = len(set(tokens))
        print(f"O modelo aprendeu um vocabulário de {vocabulario_unico} palavras únicas de todo o material")
        
        #  tokens <- ADD-PADDING(tokens, n-1)
        padding = ['<s>'] * (self.n - 1)
        tokens = padding + tokens + ['</s>']
        
        # for i=1 to LENGTH(tokens) - n + 1 do
        for i in range(len(tokens) - self.n + 1):
            
            #  window <- SUBSEQUENCE(tokens, i, i + n - 1)
            janela = tokens[i : i + self.n]
            
            #  history <- window[1... n-1]
            historico = tuple(janela[:-1]) 
            
            #  word <- window[n]
            palavra_alvo = janela[-1]      
            
            # INCREMENT-COUNT(model.counts, history, word)
            self.counts[historico][palavra_alvo] += 1
            
            # INCREMENT-COUNT(model.context_totals, history)
            self.context_totals[historico] += 1

    def calcular_probabilidade(self, word, history):
        # Referência: function GET-PROBABILITY(model, word, history) returns a probability
        
        numerator = self.counts[history][word]
        denominator = self.context_totals[history]
        if denominator == 0:
            return 0.0
        return numerator / denominator
        
    def gerar_texto(self, seed_history, length):
        # Referência: function GENERATE-TEXT(model, seed_history, length) returns a string
        
        # output <- seed_history
        output = list(seed_history)
        
        # current_history <- seed_history
        current_history = tuple(seed_history)
        
        probabilidade_sequencia = 1.0 
        
        for _ in range(length):
            # candidates <- model.VOCABULARY()
            candidates = list(self.counts[current_history].keys())
            
            if not candidates:
                break
                
            # Calcula as probabilidades de todos os candidatos para criar a distribuição
            chances = [self.calcular_probabilidade(cand, current_history) for cand in candidates]
            
            # next_word <- SAMPLE-FROM-DISTRIBUTION(model, candidates, current_history)
            next_word = random.choices(candidates, weights=chances, k=1)[0]
            
            # Matemática da Probabilidade Conjunta
            prob_da_palavra_escolhida = self.calcular_probabilidade(next_word, current_history)
            probabilidade_sequencia *= prob_da_palavra_escolhida
            
            # Referência: APPEND(output, next_word)
            output.append(next_word)
            
            # UPDATE(current_history, next_word)
            current_history = tuple(output[-(self.n - 1):])
            
            if next_word == '</s>':
                break
                
        texto_limpo = " ".join(output).replace('<s>', '').replace('</s>', '').strip()
        return texto_limpo, probabilidade_sequencia