import pytest
import numpy as np
from kichtai.nn import get_rnn_seq_model

def test_get_rnn_seq_model():
    # Given
    vocab_size=16
    embedding_dim=3
    rnn_units=2
    batch_size=1

    # When
    model = get_rnn_seq_model(vocab_size, embedding_dim, rnn_units, batch_size)
