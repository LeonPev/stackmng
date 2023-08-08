import os
import pytest
from pytest_httpserver import HTTPServer
import asyncio as aio
import json
from stackmng.crawler import Crawler, get_question_links, get_answers
import stackmng.crawler as crawler


def so_handeler(request):
    filename = None
    paths_dict = {
        '/foobar/root': 'tests/testdata/root.html',
        '/foobar/questions/q1': 'tests/testdata/q1.html',
        '/foobar/questions/q2': 'tests/testdata/q2.html',
        '/foobar/questions/q3': 'tests/testdata/q3.html',
        '/foobar/questions/q4': 'tests/testdata/q4.html',
        '/foobar/questions/q5': 'tests/testdata/q5.html',
        '/foobar/questions/q6': 'tests/testdata/q6.html'
    }

    filename = paths_dict.get(request.path)

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
    httpserver.expect_request("/foobar/questions/q4").respond_with_handler(so_handeler)
    httpserver.expect_request("/foobar/questions/q5").respond_with_handler(so_handeler)
    httpserver.expect_request("/foobar/questions/q6").respond_with_handler(so_handeler)
    so_url = httpserver.url_for("/foobar")
    crawler.stack_overflow_url = so_url
    crl = Crawler(max_depth=3)

    lnk_html = []

    async for link, html in crl.walk(so_url + '/root'):
       lnk_html.append((link, html))

    print(lnk_html)
    assert len(lnk_html) == 6

    lnk_html_dct = {link: html for link, html in lnk_html}

    assert 'title root' in lnk_html_dct[so_url + '/root']
    assert 'title q1' in lnk_html_dct[so_url + '/questions/q1']
    assert 'title q2' in lnk_html_dct[so_url + '/questions/q2']
    assert 'title q3' in lnk_html_dct[so_url + '/questions/q3']
    assert 'title q4' in lnk_html_dct[so_url + '/questions/q4']
    assert 'title q5' in lnk_html_dct[so_url + '/questions/q5']

def test_get_question_links():
    with open('tests/testdata/so.html', 'r', encoding='utf-8') as f:
        stack_overflow_resp = f.read()
    links = get_question_links(stack_overflow_resp)
    assert links == [
        crawler.stack_overflow_url + '/questions/20428627/wordpress-jetpack-tiled-gallery-loading-full-size-images-then-resizing-them-down',
        crawler.stack_overflow_url + '/questions/22026871/wordpress-jetpack-post-by-email-controlling-image-size',
        crawler.stack_overflow_url + '/questions/19882102/wordpress-twenty-eleven-php-forcing-php-code-to-skip-first-post-on-homepage',
        crawler.stack_overflow_url + '/questions/23630871/how-to-enlarge-all-featured-images-in-wordpress',
        crawler.stack_overflow_url + '/questions/8651149/wordpress-feaured-images-into-menu',
        crawler.stack_overflow_url + '/questions/12132829/re-process-all-images-in-wordpress',
        crawler.stack_overflow_url + '/questions/23427834/show-featured-imageif-it-exist-from-wordpress-json-feed-using-handlebars-js',
        crawler.stack_overflow_url + '/questions/17353100/get-images-from-wordpress-post-post-content',
        crawler.stack_overflow_url + '/questions/59280265/bulk-replace-missing-images-in-wordpress',
        crawler.stack_overflow_url + '/questions/16127152/how-to-create-resized-versions-of-images-programatically-uploaded-with-wp-insert',
    ]

def test_get_answers():
    with open('tests/testdata/so.html', 'r', encoding='utf-8') as f:
        stack_overflow_resp = f.read()
    answers = get_answers(stack_overflow_resp)
    assert answers == [
        ""
    ]