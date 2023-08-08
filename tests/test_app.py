import pytest
from stackmng import app
from unittest.mock import patch

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

async def walk():
    yield 'link1', 'html1'
    yield 'link2', 'html2'

@patch('stackmng.crawler.Crawler.walk', return_value=walk())
def test_find_best_answer(mock_crawler, client):
    response = client.post('/find_best_answer', json={'link': 'a'})
    assert response.status_code == 200
    assert response.json == {
        'links': ['link1', 'link2']
    }
    assert mock_crawler.call_args[0][0] == 'a'