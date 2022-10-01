import re
from goose3 import Goose
from collections import defaultdict
import spacy
import spacy_streamlit
import streamlit as st
from collections import Counter
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_option('deprecation.showPyplotGlobalUse', False)
nlp = spacy.load('pt_core_news_sm')


@st.cache
def load_data(url):
    g = Goose()
    article = g.extract(url=url)
    raw_text = article.cleaned_text
    regex = r'(\[William Bonner\]|\[Padre Kelmon\]|\[Jair Bolsonaro\]|\[Luiz Inácio Lula da Silva\]|' \
            r'\[Simone Tebet\]|\[Ciro Gomes\]|\[Soraya Thronicke\]|\[Felipe D\'Avila\]): (.*)\n\n'
    text = re.findall(
        regex, raw_text, re.MULTILINE)
    return text


def transform_text_dict(text):
    dict_speech_candidates = defaultdict(list)
    dict_speech_bonner = defaultdict(list)
    for item in text:
        if item[0] == '[William Bonner]':
            dict_speech_bonner['Bonner'].append(item[1])
        if item[0] == '[Soraya Thronicke]':
            dict_speech_candidates['Soraya Thronicke'].append(item[1])
        if item[0] == '[Simone Tebet]':
            dict_speech_candidates['Simone Tebet'].append(item[1])
        if item[0] == '[Jair Bolsonaro]':
            dict_speech_candidates['Jair Bolsonaro'].append(item[1])
        if item[0] == '[Ciro Gomes]':
            dict_speech_candidates['Ciro Gomes'].append(item[1])
        if item[0] == "[Felipe D'Avila]":
            dict_speech_candidates["Felipe D'Avila"].append(item[1])
        if item[0] == "[Luiz Inácio Lula da Silva]":
            dict_speech_candidates["Lula"].append(item[1])
        if item[0] == "[Padre Kelmon]":
            dict_speech_candidates["Padre Kelmon"].append(item[1])
    return dict_speech_candidates, dict_speech_bonner


def sentence_tokenizer(sentence):
    return [token.lemma_ for token in nlp(sentence.lower()) if (token.is_alpha & ~token.is_stop)]


def normalizer(sentence):
    tokenized_sentence = sentence_tokenizer(sentence)
    return ' '.join(tokenized_sentence)


def count_sort_n_tokens(tokens, n=30):
    return Counter(tokens).most_common(n)


def plot_bar_chart(values_axis_x, values_axis_y):
    fig = go.Figure([go.Bar(x=values_axis_x, y=values_axis_y, text=values_axis_y, textposition='auto')])
    fig.update_layout(autosize=False, width=500, height=500)
    fig.update_xaxes(tickangle=-45)
    return fig


def word_cloud_maker(content):
    wordcloud = WordCloud(background_color="#f5f5f5", colormap='Dark2').generate(content)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
