import os
import pytest
from pytest_httpserver import HTTPServer
import asyncio as aio
import json
from stackmng.crawler import Crawler
import stackmng.crawler as crawler

local_srv_url = ''

def so_handeler(request):
    filename = None
    paths_dict = {
        '/foobar/root': 'tests/testdata/root.html',
        '/foobar/questions/1': 'tests/testdata/q1.html',
        '/foobar/questions/2': 'tests/testdata/q2.html',
        '/foobar/questions/3': 'tests/testdata/q3.html',
        '/foobar/questions/4': 'tests/testdata/q4.html',
        '/foobar/questions/5': 'tests/testdata/q5.html',
        '/foobar/questions/6': 'tests/testdata/q6.html'
    }

    filename = paths_dict.get(request.path)
    host_url = request.headers.get('host')
    stack_overflow_resp = None
    with open(filename, 'r') as f:
        stack_overflow_resp = f.read()
        stack_overflow_resp = stack_overflow_resp.replace(
            'url', f'http://{host_url}/foobar')
    return stack_overflow_resp

@pytest.mark.asyncio
async def test_crawler(httpserver: HTTPServer):
    httpserver.expect_request("/foobar/root").respond_with_handler(so_handeler)
    httpserver.expect_request("/foobar/questions/1").respond_with_handler(so_handeler)
    httpserver.expect_request("/foobar/questions/2").respond_with_handler(so_handeler)
    httpserver.expect_request("/foobar/questions/3").respond_with_handler(so_handeler)
    httpserver.expect_request("/foobar/questions/4").respond_with_handler(so_handeler)
    httpserver.expect_request("/foobar/questions/5").respond_with_handler(so_handeler)
    httpserver.expect_request("/foobar/questions/6").respond_with_handler(so_handeler)
    so_url = httpserver.url_for("/foobar")
    crl = Crawler.create(max_depth=3, stackoverflow_url=so_url)

    lnk_html = []

    async for link, html in crl.walk(so_url + '/root'):
       lnk_html.append((link, html))

    print(lnk_html)
    assert len(lnk_html) == 6

    lnk_html_dct = {link: html for link, html in lnk_html}

    assert 'title root' in lnk_html_dct[so_url + '/root']
    assert 'title q1' in lnk_html_dct[so_url + '/questions/1']
    assert 'title q2' in lnk_html_dct[so_url + '/questions/2']
    assert 'title q3' in lnk_html_dct[so_url + '/questions/3']
    assert 'title q4' in lnk_html_dct[so_url + '/questions/4']
    assert 'title q5' in lnk_html_dct[so_url + '/questions/5']

def test_get_question_links():
    with open('tests/testdata/so.html', 'r', encoding='utf-8') as f:
        stack_overflow_resp = f.read()
    crl = Crawler.create(
        max_depth=3, 
        stackoverflow_url='https://stackoverflow.com')
    links = crl.get_question_links(stack_overflow_resp)
    assert links == [
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584?lastactivity',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class?answertab=scoredesc#tab-top',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#comment125516998_70995584',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#comment125517486_70995584',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/42388864/mock-a-method-of-already-instantiated-object?rq=3',
    'https://stackoverflow.com/questions/43003380/how-to-mock-async-with-statements?rq=3',
    'https://stackoverflow.com/questions/44004302/python-mock-patch-a-coroutine-function-within-another-function-using-pytest?rq=3',
    'https://stackoverflow.com/questions/50991740/how-to-patch-an-asynchronous-class-method?rq=3',
    'https://stackoverflow.com/questions/53508368/python-unit-testing-nested-async-with-how-to-mock-patch?rq=3',
    'https://stackoverflow.com/questions/53856568/python-how-do-i-mock-an-async-method-that-gets-called-multiple-times?rq=3',
    'https://stackoverflow.com/questions/66037643/how-to-mock-a-method-within-an-async-unit-test?rq=3',
    'https://stackoverflow.com/questions/69034187/async-patching-issue-with-static-methods-in-python?rq=3',
    'https://stackoverflow.com/questions/74000515/python-unit-testing-how-to-patch-an-async-call-internal-to-the-method-i-am-tes?rq=3',
    'https://stackoverflow.com/questions/74470798/how-to-mock-await-asyncio-future?rq=3',
    'https://stackoverflow.com/questions/76852001/how-to-move-or-assign-one-vector-into-another-depending-of-their-type-using-if-c',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    'https://stackoverflow.com/questions/70995419/how-to-mock-an-async-instance-method-of-a-patched-class/70995584#',
    ]

def test_get_answers():
    with open('tests/testdata/so.html', 'r', encoding='utf-8') as f:
        stack_overflow_resp = f.read()
    crl = Crawler.create(
        max_depth=3,
        stackoverflow_url='https://stackoverflow.com')
    answers = crl.get_answers(stack_overflow_resp)
    assert len(answers) == 2
    assert len(answers[0]) == 3307
    assert len(answers[1]) == 331

def test_get_answer_empty():
    with open('tests/testdata/q1.html', 'r', encoding='utf-8') as f:
        stack_overflow_resp = f.read()
    crl = Crawler.create(
        max_depth=3,
        stackoverflow_url='https://stackoverflow.com')
    answers = crl.get_answers(stack_overflow_resp)
    assert len(answers) == 0

# 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