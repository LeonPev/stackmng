import os
import pytest
from pytest_httpserver import HTTPServer
import asyncio as aio
import json
from stackmng.crawler import Crawler, get_question_links
import stackmng.crawler as crawler


def so_handeler(request):
    filename = None
    if request.path == '/foobar/root':
        filename = 'tests/testdata/root.html'
    elif request.path == '/foobar/questions/q1':
        filename = 'tests/testdata/q1.html'
    elif request.path == '/foobar/questions/q2':
        filename = 'tests/testdata/q2.html'
    elif request.path == '/foobar/questions/q3':
        filename = 'tests/testdata/q3.html'

    stack_overflow_resp = None
    with open(filename, 'r') as f:
        stack_overflow_resp = f.read()
    return stack_overflow_resp

@pytest.mark.asyncio
async def test_crawler(httpserver: HTTPServer):
    httpserver.expect_request("/foobar/root").respond_with_handler(so_handeler)
    httpserver.expect_request("/foobar/questions/q1").respond_with_handler(so_handeler)
    httpserver.expect_request("/foobar/questions/q2").respond_with_handler(so_handeler)
    httpserver.expect_request("/foobar/questions/q3").respond_with_handler(so_handeler)
    so_url = httpserver.url_for("/foobar")
    crawler.stack_overflow_url = so_url
    crl = Crawler(max_depth=2)

    lnk_html = {}

    async for link, html in crl.walk(so_url + '/root'):
       lnk_html[link] = html


    print(list(lnk_html.keys()))
    assert 'title root' in lnk_html[so_url + '/root']
    assert 'title q1' in lnk_html[so_url + '/questions/q1']
    assert 'title q2' in lnk_html[so_url + '/questions/q2']
    assert 'title q3' in lnk_html[so_url + '/questions/q3']
    