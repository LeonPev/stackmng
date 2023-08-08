import aiohttp
from bs4 import BeautifulSoup
import re


class Crawler:
    @classmethod
    def create(cls, max_depth, stackoverflow_url):
        regex = re.compile(r'^' + stackoverflow_url + '/questions/\d+')
        return cls(max_depth=max_depth, regex_q_url=regex)

    def __init__(self, max_depth, regex_q_url):
        self.max_depth = max_depth
        self.regex_q_url = regex_q_url

    async def walk(self, root_link):
        depth = 0
        history = {root_link}
        next_links = {root_link}
        while next_links and depth <= self.max_depth:
            current_links = set()
            current_links = current_links.union(next_links)
            for link in current_links:
                html = await self.fetch_html(link)
                yield link, html
                next_links.update(self.get_question_links(html))
            next_links = next_links - history
            history = history.union(next_links)
            depth += 1

    async def fetch_html(self, link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                return await response.text()

    def get_question_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            q_link = link.get('href')
            if q_link and self.regex_q_url.match(q_link):
                links.append(q_link)
        return links

    def get_answers(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        answers = []
        for answer in soup.find_all('div', class_='s-prose js-post-body'):
            answers.append(str(answer))
        if answers:
            return answers[1:]
        return answers

