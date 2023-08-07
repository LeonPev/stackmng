import os
import pytest
from pytest_httpserver import HTTPServer
from stackmng import app, parse_html
import asyncio as aio
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def so_handeler(request):
    filename = None
    if request.path == '/foobar/root':
        filename = 'tests/testdata/root.html'
    elif request.path == '/foobar/q1':
        filename = 'tests/testdata/q1.html'
    elif request.path == '/foobar/q2':
        filename = 'tests/testdata/q2.html'
    elif request.path == '/foobar/q3':
        filename = 'tests/testdata/q3.html'

    stack_overflow_resp = None
    with open(filename, 'r', encoding='utf-8') as f:
        stack_overflow_resp = f.read()
    return stack_overflow_resp

def test_find_best_answer(client, httpserver: HTTPServer):
    httpserver.expect_request("/foobar").respond_with_handler(so_handeler)
    #.respond_with_data(stack_overflow_resp)
    so_url = httpserver.url_for("/foobar")
    parse_html.stack_overflow_url = so_url
    response = client.post('/find_best_answer', json={
        "link": so_url,
        "prompt": "How to convert a string to a datetime object in Python?"
    })
    assert response.status_code == 200
    assert response.json['links'] == ['a', 'b', 'c']
