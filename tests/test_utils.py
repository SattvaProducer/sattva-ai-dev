import pytest
from src.gui_tk import normalize_date  # или вынести в utils.py и импортировать оттуда

def test_numeric_format():
    assert normalize_date("05112004") == "05112004"

def test_dot_format():
    assert normalize_date("05.11.2004") == "05112004"

def test_dash_format():
    assert normalize_date("2004-11-05") == "05112004"

def test_text_russian():
    assert normalize_date("5 ноября 2004") == "05112004"

def test_text_english():
    assert normalize_date("5 nov 2004") == "05112004"

def test_invalid_date():
    with pytest.raises(ValueError):
        normalize_date("31 февраля 2000")
