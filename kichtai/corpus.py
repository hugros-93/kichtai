import re
import string
import random
import numpy as np
import pandas as pd
import plotly.express as px
from itertools import chain

class RapCorpus():
    def __init__(self, dict_artists):
        self.dict_artists = dict_artists
        self.list_artists = list(dict_artists.keys())
        self.corpus = ""

    def info(self):
        print("# Lyrics #")
        for artist_name in self.list_artists:
            print(
                f" > {artist_name} ({len(self.dict_artists[artist_name]['lyrics'].keys())})"
            )

    def create_corpus(self):
        for artist_name in self.list_artists:
            for song_title in self.dict_artists[artist_name]["lyrics"]:
                self.corpus += self.dict_artists[artist_name]["lyrics"][song_title].replace("\n", "\n\n")

    def clean_text(self):
        self._clean_brackets()
        self._clean_more_on_genius()
        self._clean_header_lyrics()
        self._clean_letters()
        self._clean_spaces()

    def _clean_brackets(self):
        is_on = True
        clean_txt = ""
        for i in self.corpus:
            if i == "[":
                is_on = False

            if is_on:
                clean_txt += i

            elif i == "]":
                is_on = True
        self.corpus = clean_txt

    def _clean_spaces(self):
        while "\n\n" in self.corpus:
            self.corpus = self.corpus.replace("\n\n", "\n")
        while "  " in self.corpus:
            self.corpus = self.corpus.replace("  ", " ")
        self.corpus = self.corpus.replace("\n ", "\n")

    def _clean_more_on_genius(self):
        self.corpus = self.corpus.replace("\nMore on Genius", "")


    def _clean_header_lyrics(self):
        text_list = self.corpus.split("\n")
        text_list = [x for x in text_list if x[-6:] != "Lyrics"]

        self.corpus = "\n".join(text_list).strip()


    def _clean_numbers(self):
        self.corpus = re.sub(r"\d+", "", self.corpus)


    def _clean_letters(self):

        # lower
        text = self.corpus.lower()

        # specific characters
        list_a = ["à", "â", "á", "ä", "ã", "ā", "ă", "ą"]
        for a in list_a:
            text = text.replace(a, "a")

        list_e = ["е", "è", "é", "ê", "ë", "ę"]
        for e in list_e:
            text = text.replace(e, "e")

        list_i = ["î", "ï", "í", "ì", "ī"]
        for i in list_i:
            text = text.replace(i, "i")

        list_o = ["ò", "ô", "ó", "ö", "õ", "ō"]
        for o in list_o:
            text = text.replace(o, "o")

        list_u = ["ù", "ú", "û", "ü"]
        for u in list_u:
            text = text.replace(u, "u")

        list_c = ["ç", "ć", "č"]
        for c in list_c:
            text = text.replace(c, "c")

        text = text.replace("ñ", "n")
        text = text.replace("ğ", "g")
        text = text.replace("ł", "l")
        text = text.replace("ś", "s")
        text = text.replace("š", "s")
        text = text.replace("ż", "z")
        text = text.replace("×", "x")

        text = text.replace("'̀'", "")

        text = text.replace("'", " ")
        text = text.replace("-", " ")
        text = text.replace("’", " ")
        text = text.replace("\u2005", " ")
        text = text.replace("\u205f", " ")
        text = text.replace("c\xad\xad", " ")

        text = text.replace("\x9c", "œ")
        text = text.replace("oeœ", "œ")
        text = text.replace("œ", "oe")
        text = text.replace("æ", "ae")
        text = text.replace("\x90e", "é")

        str_to_del = "€¡°¿—“”!#%&(),./:;?θιςυχавгдежиклмнорстучыьяḥṭ∞かだでとのひるテホル京内東都ﬁﬂ￼…«»₂²"
        for char in str_to_del:
            text = text.replace(char, "")

        list_to_del = [
            '"',
            "...",
            "\t",
            "\xa0",
            "\xad",
            "\x93",
            "\x94",
            "\ufeff",
            "\u200e",
            "\u200a",
            "\u200b",
        ]
        for char in list_to_del:
            text = text.replace(char, "")

        self.corpus = text

    def print_text(self, limit=500, random_select=False):
        print("# Text #")
        if not random_select:
            print(f"\n{self.corpus[:limit]}...")
        else:
            i = random.randint(0, len(self.corpus))
            print(f"\n...{self.corpus[i:i+limit]}...")

    def export(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.corpus)

    def plot_vocabulary(self):
        df = pd.DataFrame(1, index = [x for x in self.corpus], columns=['letters'])
        df = df.reset_index()
        df.columns = ['letters', 'count']
        df = df.groupby('letters').count().sort_values('count', ascending=False).reset_index()

        fig = px.bar(df, x='letters', y='count',title='Vocabulary')
        
        return fig

    def plot_dictionary(self, top=10):
        list_corpus = [x for x in self.corpus.split('\n') if x!='']
        list_words=list(chain(*[x.split(' ') for x in list_corpus]))

        df = pd.DataFrame(1, index = [x for x in np.array(list_words).ravel() if x != 0], columns=['words'])
        df = df.reset_index()
        df.columns = ['words', 'count']
        df = df.groupby('words').count().sort_values('count', ascending=False).reset_index()

        fig = px.bar(df.iloc[:top, :], x='words', y='count',title='Dictionary')
        
        return fig
