import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from parser import parser_kolesa_kz, build_kolesa_url

FIXTURES = Path(__file__).parent / "fixtures"


def _mock_get(fixture_file):
    html = (FIXTURES / fixture_file).read_text(encoding="utf-8")
    mock_response = MagicMock()
    mock_response.text = html
    mock_response.raise_for_status = MagicMock()
    return mock_response


def test_parser_kolesa_kz_returns_avg_price():
    with patch("parser.requests.get", return_value=_mock_get("toyota_rav4_2007.html")):
        result = parser_kolesa_kz("https://kolesa.kz/cars/toyota/rav4/?year[from]=2007&year[to]=2007")
    assert result == 6621000


def test_build_kolesa_url_removes_parentheses():
    url = build_kolesa_url("kia", "k5 (optima) qt", "2020")
    assert "(" not in url
    assert ")" not in url
    assert url == "https://kolesa.kz/cars/kia/k5-optima-qt/?year[from]=2020&year[to]=2020"


def test_build_kolesa_url_slugs_cyrillic():
    pytest.skip("TODO: decide how to handle Cyrillic make names like 'ВАЗ (Lada)'")
    pytest.skip("TODO: decide how to handle Cyrillic make names like 'GAZ (ГАЗ)'")


def test_parser_kolesa_kz_returns_none_when_no_avg_price():
    mock_response = MagicMock()
    mock_response.text = "<html>no price here</html>"
    mock_response.raise_for_status = MagicMock()
    with patch("parser.requests.get", return_value=mock_response):
        result = parser_kolesa_kz("https://kolesa.kz/cars/toyota/rav4/?year[from]=2007&year[to]=2007")
    assert result is None
