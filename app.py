import re
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import spacy
import spacy_streamlit
from operations import load_data, transform_text_dict, sentence_tokenizer, normalizer, count_sort_n_tokens, \
    plot_bar_chart, word_cloud_maker

url = 'https://noticias.uol.com.br/eleicoes/2022/09/30/integra-debate-na-globo.htm'

candidates = ['Lula', 'Jair Bolsonaro', 'Ciro Gomes', 'Simone Tebet', "Felipe D'Avila", 'Soraya Thronicke',
              'Padre Kelmon']

dict_speech_candidates, dict_speech_bonner = transform_text_dict(load_data(url))

candidates_tokens = {}
for candidate in candidates:
    candidates_tokens[candidate] = sentence_tokenizer(' '.join(dict_speech_candidates[candidate]))

tokens_bonner = {'Bonner': sentence_tokenizer(' '.join(dict_speech_bonner['Bonner']))}

speech_all_candidates = []
for item in dict_speech_candidates.values():
    speech_all_candidates.append(' '.join(item))

tokens_all_candidates = {'Todos candidatos': sentence_tokenizer(' '.join(speech_all_candidates))}

tokens_per_candidate = defaultdict(list)

for candidate in candidates:
    tokens_per_candidate[candidate] = pd.DataFrame(count_sort_n_tokens(candidates_tokens[candidate], 30), columns=[
        'word', 'quantity'])

df_quantity_words_candidate = pd.DataFrame(columns=['candidate', 'word_quantity'])

for candidate in candidates:
    df_quantity_words_candidate = df_quantity_words_candidate.append({
        'candidate': candidate,
        'word_quantity': len(candidates_tokens[candidate])}, ignore_index=True)

candidates_tokens_wordcloud = defaultdict(list)
for candidate in candidates:
    candidates_tokens_wordcloud[candidate] = ' '.join(candidates_tokens[candidate])

common_words_general = count_sort_n_tokens(tokens_all_candidates['Todos candidatos'], 30)
df_common_words_general = pd.DataFrame(common_words_general, columns=['word', 'quantity'])
content_wordcloud_general = ' '.join(tokens_all_candidates['Todos candidatos'])


st.subheader('Análise estatística sobre as falas dos candidatos a presidente '
         'durante o último debate do primeiro turno das eleições de 2022')

st.text('Eventos como esse são oportunidades para aplicar os conhecimentos básicos sobre '
             '\nProcessamento de Linguagem Natural no sentido de compor análises construindo observações\n'
             'que interessem a população em busca da confirmação da opção de voto.')


st.sidebar.header("Sobre o Debate")
st.sidebar.info("Ocorreu no dia 29/09 (a 3 dias da eleição) e foi realizado pela Rede Globo."
                "\n\n\n"
                "A transcrição do debate foi obtida em: "
                "https://noticias.uol.com.br/eleicoes/2022/09/30/integra-debate-na-globo.htm"
                "\n\n\n\n\n\n\n"
                "A análise sobre o debate ocorrido em 28/08 está disponível em: \n"
                "https://alexvaroz-app-analise-debate-01-2022-app-i5pv0j.streamlitapp.com/")

st.subheader('Número de palavras utilizadas por cada candidato')
st.plotly_chart(
    plot_bar_chart(df_quantity_words_candidate.candidate.values, df_quantity_words_candidate.word_quantity.values),
    use_container_width=True)

st.subheader('30 palavras mais citadas pelos candidatos')
st.plotly_chart(
    plot_bar_chart(df_common_words_general.word.values, df_common_words_general.quantity.values),
    use_container_width=True)

st.subheader('Nuvem de palavras mais citadas por todos os candidatos')
word_cloud_maker(content_wordcloud_general)
st.pyplot()

st.subheader('Análise por candidato')
selected_candidate = st.selectbox('Selecione o candidato', candidates)


st.plotly_chart(
    plot_bar_chart(tokens_per_candidate[selected_candidate].word.values,
                   tokens_per_candidate[selected_candidate].quantity.values), use_container_width=True)

word_cloud_maker(candidates_tokens_wordcloud[selected_candidate])
st.pyplot()

