import pytest
from kichtai.corpus import RapCorpus

dict_artists = {
    'Booba': {
        'id': 1282,
        'list_songs': ['92i Veyron'],
        'lyrics': {
            '92i Veyron': '\n92i Veyron Lyrics\n\n\n\n[Paroles de "92i Veyron"]\n\n[Intro]\nPersonne, personne\nPersonne, personne\n\n'
        }
    }
}

def test_init_corpus():
    # Given
    corpus = RapCorpus(dict_artists)

    # Then
    corpus.info() 

def test_clean_corpus():
    # Given
    corpus = RapCorpus(dict_artists)
    corpus.create_corpus()

    # When
    corpus.clean_text()

    # Then
    assert corpus.corpus == 'personne personne\npersonne personne'
