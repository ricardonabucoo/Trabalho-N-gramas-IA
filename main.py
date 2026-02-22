from ngramas import ModeloNGrama, ler_slides_da_pasta
import random

print("Lendo os PDFs")
texto_slides = ler_slides_da_pasta("slides_base")

if not texto_slides.strip():
    exit()

# Utilizando modelo Bigrama (N=2).
# usuário só precisa digitar UMA palavra para começar a geração
ordem_n = 2
tamanho_semente = ordem_n - 1 

modelo = ModeloNGrama(n=ordem_n)

print("Treinando  com os slides da disciplina")
modelo.treinar(texto_slides)

print("Autopreenchimento de texto com o modelo Bigrama")
print("Digite pelo menos UMA palavra para dar contexto.")

while True:
    entrada = input("\nVocê: ").strip()
    
    if entrada.lower() == 'sair':
        break
        
    # Passa o que o usuário digitou pelo mesmo limpador do modelo
    palavras_digitadas = modelo.limpar_e_tokenizar(entrada)
    
    if len(palavras_digitadas) < tamanho_semente:
        print("Bot: Digite pelo menos uma palavra válida para eu continuar.")
        continue
        
    # Extrai o contexto necessário para a matemática do Bigrama
    semente = tuple(palavras_digitadas[-tamanho_semente:])
    
    prefixo = ""
    if len(palavras_digitadas) > tamanho_semente:
        prefixo = " ".join(palavras_digitadas[:-tamanho_semente]) + " "
        
    # se a palavra não existir nos slides
    if semente not in modelo.counts or len(modelo.counts[semente]) == 0:
        palavra_formatada = semente[0]
        palavras_conhecidas = [k[0] for k in modelo.counts.keys() if k[0] != '<s>']
        
            
        print(f"Bot: A palavra '{palavra_formatada}' não aparece no histórico treinado. ")
        continue
        
    # Gera as próximas palavras e retorna a probabilidade da frase
    texto_novo, chance = modelo.gerar_texto(semente, length= 3)
    
    chance_percentual = chance * 100
    
    print(f"Bot: {prefixo}{texto_novo}...")
    print(f"Probabilidade MLE da sequência gerada: {chance_percentual:.6f}%")