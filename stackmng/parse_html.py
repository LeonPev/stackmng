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

