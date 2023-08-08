import pytest
from stackmng import app
from unittest.mock import patch
import asyncio

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f

# patch stackmng.crawler.crawler.Crawler.walk to return [('a', 'b')]
@patch('stackmng.crawler.Crawler.walk', return_value=async_return([('a', 'b')]))
def test_find_best_answer(walk_mock, client):
    # response = client.post('/find_best_answer', json={
    #     "link": "a",
    #     "prompt": "How to convert a string to a datetime object in Python?"
    # })
    # assert response.status_code == 200
    # assert response.json['links'] == ['a', 'b', 'c']
    pass
