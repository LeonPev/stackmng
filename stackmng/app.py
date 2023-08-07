from flask import Flask, request
import aiohttp


app = Flask(__name__)

@app.route('/find_best_answer', methods=['POST'])
async def find_best_answer():
    link = request.json['link']
    return {
        'html': await fetch_html(link)
    }

async def fetch_html(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            res =  await response.text()
            return res