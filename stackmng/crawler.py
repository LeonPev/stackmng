import aiohttp
from bs4 import BeautifulSoup


stack_overflow_url = "https://stackoverflow.com"

def get_question_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        q_link = link.get('href')
        if q_link and q_link.startswith('/questions/'):
            links.append(stack_overflow_url + q_link)
    return links

async def fetch_html(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            return await response.text()
        
class Crawler:
    def __init__(self, max_depth):
        self.max_depth = max_depth

    async def walk(self, root_link):
        links = [root_link]
        depth = 0
        while links and depth <= self.max_depth:
            next_links = []
            for link in links:
                html = await fetch_html(link)
                yield link, html
                next_links.extend(get_question_links(html))
            links = next_links
            depth += 1
        
        
        