import aiohttp
from bs4 import BeautifulSoup


stack_overflow_url = "https://stackoverflow.com"

class Crawler:
    def __init__(self, max_depth):
        self.max_depth = max_depth

    async def walk(self, root_link):
        depth = 0
        history = {root_link}
        next_links = {root_link}
        while next_links and depth <= self.max_depth:
            current_links = set()
            current_links = current_links.union(next_links)
            for link in current_links:
                html = await fetch_html(link)
                yield link, html
                next_links.update(get_question_links(html))
            next_links = next_links - history
            history = history.union(next_links)
            depth += 1

async def fetch_html(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            return await response.text()

def get_question_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        q_link = link.get('href')
        if q_link and q_link.startswith('/questions/'):
            links.append(stack_overflow_url + q_link)
    return links

def get_answers(html):
    soup = BeautifulSoup(html, 'html.parser')
    answers = []
    for answer in soup.find_all('div', class_='s-prose js-post-body'):
        answers.append(answer)
    return answers

