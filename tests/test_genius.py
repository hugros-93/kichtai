import pytest

from kichtai.genius import GeniusParser

def test_token():
    # Given
    rap_parser = GeniusParser("OnEfAkEToKeN")

    # Then
    with pytest.raises(Exception):
        rap_parser.test_token()