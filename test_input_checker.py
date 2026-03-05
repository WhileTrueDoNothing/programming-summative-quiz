from quiz_utils import StringInputChecker
import pytest

@pytest.fixture(scope="module")
def name_checker():
    return StringInputChecker(max_len=50, format_regex=r"[A-Z][^1-9`¬!?\"£$%^&*()_+={}[\];:@#~|\\,<>\/]*")

def test_empty_name(name_checker):
    assert not name_checker.presence_check("")
    assert not name_checker.presence_check("    ")

def test_names_with_chars(name_checker):
    assert name_checker.format_check("Anne-Marie")
    assert name_checker.format_check("Françoise")
    assert name_checker.format_check("Thomas O'Malley")
    assert not name_checker.format_check(".")
    assert not name_checker.format_check("1337 H@x0r")
    assert not name_checker.format_check("0liver")

def test_name_lengths(name_checker):
    assert name_checker.length_check("Maria Euphonia Demetria Alexandra Jeanette Susanne")
    assert not name_checker.length_check("Suigyō-matsu Unrai-matsu Fūrai-matsu Kū-Neru Tokoro")