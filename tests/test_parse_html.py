# import pytest
# from stackmng import parse_html

# def test_parse_html():
#     with open('tests/testdata/so.html', 'r', encoding='utf-8') as f:
#         stack_overflow_resp = f.read()
#     links = parse_html.get_question_links(stack_overflow_resp)
#     assert links == [
#         parse_html.stack_overflow_url + '/questions/20428627/wordpress-jetpack-tiled-gallery-loading-full-size-images-then-resizing-them-down',
#         parse_html.stack_overflow_url + '/questions/22026871/wordpress-jetpack-post-by-email-controlling-image-size',
#         parse_html.stack_overflow_url + '/questions/19882102/wordpress-twenty-eleven-php-forcing-php-code-to-skip-first-post-on-homepage',
#         parse_html.stack_overflow_url + '/questions/23630871/how-to-enlarge-all-featured-images-in-wordpress',
#         parse_html.stack_overflow_url + '/questions/8651149/wordpress-feaured-images-into-menu',
#         parse_html.stack_overflow_url + '/questions/12132829/re-process-all-images-in-wordpress',
#         parse_html.stack_overflow_url + '/questions/23427834/show-featured-imageif-it-exist-from-wordpress-json-feed-using-handlebars-js',
#         parse_html.stack_overflow_url + '/questions/17353100/get-images-from-wordpress-post-post-content',
#         parse_html.stack_overflow_url + '/questions/59280265/bulk-replace-missing-images-in-wordpress',
#         parse_html.stack_overflow_url + '/questions/16127152/how-to-create-resized-versions-of-images-programatically-uploaded-with-wp-insert',
#     ]
