"""Tes the APD module."""
from pathlib import Path

import pytest

from scrapd.core import apd
from tests import mock_data

TEST_ROOT_DIR = Path(__file__).resolve().parent.parent
TEST_DATA_DIR = TEST_ROOT_DIR / 'data'


@pytest.fixture
def news_page(scope='session'):
    page_fd = TEST_DATA_DIR / 'news_page.html'
    return page_fd.read_text()


@pytest.fixture
def detail_page(scope='session'):
    page_fd = TEST_DATA_DIR / 'detail_page.html'
    return page_fd.read_text()


def test_parse_twitter_title_00():
    """Ensure the Twitter title gets parsed correctly."""
    actual = apd.parse_twitter_title(mock_data.twitter_title_00)
    expected = {'Fatal crashes this year': '73'}
    assert actual == expected


def test_parse_twitter_description_00():
    """Ensure the Twitter description gets parsed correctly."""
    actual = apd.parse_twitter_description(mock_data.twitter_description_00)
    expected = {
        'Case':
        '18-3640187',
        'Date':
        'December 30, 2018',
        'Time':
        '2:24 a.m.',
        'Location':
        '1400 E. Highway 71 eastbound',
        'DOB':
        '02/09/80',
        'Notes':
        'The preliminary investigation shows that a 2003 Ford F150 was traveling northbound on the US Highway 183 northbound ramp to E. Highway 71, eastbound. The truck went across the E. Highway 71 and US Highway 183 ramp, rolled and came to a stop north of the roadway.',
        'Gender':
        'male',
        'Ethnicity':
        'White',
        'Last Name':
        'Sabillon-Garcia',
        'First Name':
        'Corbin',
        'Age':
        38,
    }
    assert actual == expected


def test_parse_twitter_description_01():
    """Ensure the Twitter description gets parsed correctly."""
    actual = apd.parse_twitter_description(mock_data.twitter_description_01)
    expected = {
        'Case': '19-0161105',
    }
    assert actual == expected


def test_extract_traffic_fatalities_page_details_link_00(news_page):
    """Ensure page detail links are extracted from news page."""
    actual = apd.extract_traffic_fatalities_page_details_link(news_page)
    expected = [
        ('/news/traffic-fatality-2-3', 'Traffic Fatality #2', '2'),
        ('/news/traffic-fatality-1-4', 'Traffic Fatality #1', '1'),
        ('/news/traffic-fatality-72-1', 'Traffic Fatality #72', '72'),
        ('/news/traffic-fatality-73-2', 'Traffic Fatality #73', '73'),
        ('/news/traffic-fatality-71-2', 'Traffic Fatality #71', '71'),
        ('/news/traffic-fatality-69-3', 'Traffic Fatality #69', '69'),
    ]
    assert actual == expected


def test_generate_detail_page_urls_00():
    """Ensure a full URL is generated from a partial one."""
    actual = apd.generate_detail_page_urls([
        ('/news/traffic-fatality-1-4', 'Traffic Fatality #1', '1'),
        ('/news/traffic-fatality-2-3', 'Traffic Fatality #2', '2'),
    ])
    expected = [
        'http://austintexas.gov/news/traffic-fatality-1-4',
        'http://austintexas.gov/news/traffic-fatality-2-3',
    ]
    assert actual == expected


def test_has_next_00(news_page):
    """Ensure we detect whether there are more news pages."""
    assert apd.has_next(news_page)


def test_parse_detail_page_00(detail_page):
    """Ensure information are properly extracted from the detail page."""
    actual = apd.parse_detail_page(detail_page)
    expected = {
        'Age': 38,
        'Case': '18-3640187',
        'DOB': '02/09/80',
        'Date': 'December 30, 2018',
        'Ethnicity': 'White',
        'First Name': 'Corbin',
        'Gender': 'male',
        'Last Name': 'Sabillon-Garcia',
        'Location': '1400 E. Highway 71 eastbound',
        'Notes': '',
        'Time': '2:24 a.m.',
    }
    assert actual == expected


def test_parse_detail_page_01():
    """Ensure information are properly extracted from the detail page."""
    page_fd = TEST_DATA_DIR / 'traffic-fatality-2-3'
    detail_page = page_fd.read_text()
    actual = apd.parse_detail_page(detail_page)
    expected = {
        'Age': 58,
        'DOB': '02/15/1960',
        'Date': 'January 16, 2019',
        'Ethnicity': 'White',
        'First Name': 'Ann',
        'Gender': 'female',
        'Last Name': 'Bottenfield-Seago',
        'Location': 'West William Cannon Drive and Ridge Oak Road',
        'Notes': '',
        'Time': '3:42 p.m.'
    }
    assert actual == expected