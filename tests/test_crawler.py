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

    expected = {
    so_url + '/questions/q1': '<!DOCTYPE html>\n'
                                                '\n'
                                                '<html>\n'
                                                '    <head>\n'
                                                '        <title>Root</title>\n'
                                                '    </head>\n'
                                                '</html>',
  so_url + '/foobar/questions/q2': '<!DOCTYPE html>\n'
                                                '\n'
                                                '<html>\n'
                                                '    <head>\n'
                                                '        <title>Root</title>\n'
                                                '    </head>\n'
                                                '    <a '
                                                'href="/questions/q1">q1</a>\n'
                                                '    <a '
                                                'href="/questions/q3">q3</a>\n'
                                                '</html>',
  so_url + '/foobar/questions/q3': '<!DOCTYPE html>\n'
                                                '\n'
                                                '<html>\n'
                                                '    <head>\n'
                                                '        <title>Root</title>\n'
                                                '    </head>\n'
                                                '</html>',
  so_url + '/foobar/root': '<!DOCTYPE html>\n'
                                        '\n'
                                        '<html>\n'
                                        '    <head>\n'
                                        '        <title>Root</title>\n'
                                        '    </head>\n'
                                        '    <a href="/questions/q1">q1</a>\n'
                                        '    <a href="/questions/q2">q2</a>\n'
                                        '</html>',
}
    assert lnk_html == expected


def test_get_question_links():
    with open('tests/testdata/so.html', 'r') as f:
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