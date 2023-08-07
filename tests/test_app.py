import pytest
from stackmng import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# monkey patch crawler in app.py
def test_find_best_answer(client, monkeypatch):
    # response = client.post('/find_best_answer', json={
    #     "link": "a",
    #     "prompt": "How to convert a string to a datetime object in Python?"
    # })
    # monkeypatch.setattr(stackmng.crawler, "get", mock_get)
    # assert response.status_code == 200
    # assert response.json['links'] == ['a', 'b', 'c']
    pass
