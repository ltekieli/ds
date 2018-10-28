from random import choice
from string import ascii_lowercase

from ds.printer import trim


def generate_string(length):
    return "".join(choice(ascii_lowercase) for i in range(length))


def generate_empty_string(length):
    return "".join(" " for i in range(length))


def test_trim():
    title = generate_string(60)
    out = trim(title, 50)
    assert title[0:47] + "..." == out
    assert 50 == len(out)

    title = generate_string(50)
    out = trim(title, 50)
    assert title == out
    assert 50 == len(out)

    title = generate_string(49)
    out = trim(title, 50)
    assert title + generate_empty_string(1) == out
    assert 50 == len(out)
