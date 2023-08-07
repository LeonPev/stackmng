from flask import Flask, request
from stackmng.crawler import Crawler

crl = Crawler(max_depth=2)
app = Flask(__name__)


@app.route('/find_best_answer', methods=['POST'])
async def find_best_answer():
    link = request.json['link']
    links = []
    for link in crl.walk():
        links.append(link)
        
    return {
        'links': links
    }
