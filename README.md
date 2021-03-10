# __kichtAI__
## *''Té-ma la kichtAI, té-ma la taille d'la kichtAI''*

- Scrap lyrics from __Genius API__ and create a clean text corpus
- Train from scratch a sequence model for text generation using __tensorflow__

You need a token to connect to the Genius API. After subscribing, use your token to connect and scrap lyrics.

```python
from kichtai.genius import GeniusParser

# Search for songs of artists
rap_parser = GeniusParser("your_genius_token")
rap_parser.create_dict_artists(list_artists=['Gazo'])
rap_parser.search_for_songs(nb_page=1, per_page=1)

# Search for raw lyrics
rap_parser.search_for_lyrics()

```
`output:`

```python
{'Gazo': {
    'id': 23012, 
    'list_songs': ['Drill FR 4'], 
    'lyrics': {
        'Drill FR 4': '\nDrill FR 4 Lyrics\n\n\n\n[Paroles de "Drill FR 4" ft. Freeze Corleone]\n\n[Intro : Gazo & Freeze Corleone]\nS/o le Flem\nEkip, ekip, ekip, ekip\nMaLaGaNgx et six-six-seven, pétasse\nMMS, LDO, NRM, (baw) 667, baw\nBaw, ekip,\u2005hey,\u2005hey, hey\nBaw, skrt,\u2005la MaLa est GaNgx, ekip, ekip,\u2005ekip\n\n[Refrain : Gazo]\nLes bonbonnes sont remplies de cocaïne (baw, flexin\')...'
        }
    }
}
```

Create a clean corpus easily using `RapCorpus`:

```python
from kichtai.corpus import RapCorpus

corpus = RapCorpus(rap_parser.dict_artists)
corpus.create_corpus()
corpus.clean_text()
corpus.print_text(limit=500)
```

`output:`

```
# Text #

so le flem
ekip ekip ekip ekip
malagangx et six six seven petasse
mms ldo nrm baw 667 baw
baw ekip hey hey hey
baw skrt la mala est gangx ekip ekip ekip
les bonbonnes sont remplies de cocaine baw flexin 
```

A toy example (corpus creation, model training and text generation) is available in `example.py`. To reach acceptable performances, generate a huge corpus with many artists and many songs.
- Add your favorite artitsts in `list_artists`
- Increase the number of pages `nb_page` and number of results per page `per_page` in order to get the lyrics of multiple songs
- Increase the dimensions of the deep learning architecture `embedding_dim` and `rnn_units`
- Use your own model ! ;)

_References:_
- *https://docs.genius.com/*
- *https://dev.to/willamesoares/how-to-integrate-spotify-and-genius-api-to-easily-crawl-song-lyrics-with-python-4o62*
- *https://www.tensorflow.org/tutorials/text/text_generation*
