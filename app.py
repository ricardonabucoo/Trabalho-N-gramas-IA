





##### Interface para o hughingfaces ( usada ao inves da main)

import streamlit as st
from ngramas import ModeloNGrama, ler_slides_da_pasta
import random

# Configuração da página
st.set_page_config(page_title="Bot de IA", page_icon=" :)")

st.title("Autocompletar da Disciplina de IA")
st.write("Baseado em N-Gramas (Cadeias de Markov) e treinado com os slides do Prof. Hendrik.")


@st.cache_resource
def carregar_e_treinar_modelo():
    texto_slides = ler_slides_da_pasta("slides_Base")
    if not texto_slides.strip():
        return None
    
    # Bigrama (N=2)
    modelo = ModeloNGrama(n=2)
    modelo.treinar(texto_slides)
    return modelo

# Mostra um "carregando" 
with st.spinner("Lendo PDFs e treinando o modelo MLE..."):
    modelo = carregar_e_treinar_modelo()

if modelo is None:
    st.error("Erro: Não foi possível ler os PDFs da pasta 'slides_base'. Verifique os arquivos.")
else:
    st.success("Modelo  pronto")
    
    # Cria a caixa de texto para o usuário digitar
    entrada = st.text_input("Digite UMA palavra de contexto :")
    tamanho_semente = modelo.n - 1
    
    # Cria o botão
    if st.button("Gerar Continuação"):
        if entrada:
            palavras_digitadas = modelo.limpar_e_tokenizar(entrada)
            
            if len(palavras_digitadas) < tamanho_semente:
                st.warning("Digite pelo menos uma palavra válida.")
            else:
                semente = tuple(palavras_digitadas[-tamanho_semente:])
                prefixo = " ".join(palavras_digitadas[:-tamanho_semente]) + " " if len(palavras_digitadas) > tamanho_semente else ""
                
                # Validação se a palavra não existe
                if semente not in modelo.counts or len(modelo.counts[semente]) == 0:
                    palavra_formatada = semente[0]
                    palavras_conhecidas = [k[0] for k in modelo.counts.keys() if k[0] != '<s>']
                    st.error(f"A palavra  não aparece no histórico treinado. Tente estas: ")
                else:
                    # Gera as próximas 5 palavras e a probabilidade
                    texto_novo, chance = modelo.gerar_texto(semente, length=5)
                    chance_percentual = chance * 100
                    
                    # Exibe o resultado na tela com caixas coloridas
                    st.info(f"**Continuação gerada:** {prefixo}{texto_novo}...")
                    st.caption(f"Probabilidade matemática (MLE) da sequência: {chance_percentual:.6f}%")