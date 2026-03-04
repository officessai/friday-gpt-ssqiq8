import random

import pytest

from friday.jokes import JOKES, get_joke


def test_get_joke_returns_known_joke_with_seed():
    rng = random.Random(0)
    joke = get_joke(rng=rng)
    assert joke in JOKES


def test_get_joke_allows_custom_jokes_iterable():
    jokes = {"pierwszy żart", "drugi żart"}
    rng = random.Random(1)
    joke = get_joke(jokes=jokes, rng=rng)
    assert joke in jokes


def test_get_joke_empty_iterable_raises_value_error():
    with pytest.raises(ValueError):
        get_joke(jokes=[])
