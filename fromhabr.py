"""Some beautifulsoup testing."""
import requests
from bs4 import BeautifulSoup

raw = requests.get('https://habr.com/all')
posts = BeautifulSoup(raw.text, 'html.parser')
# for br in quotes.find_all('br'):
#     br.replace_with('\n')
# print(posts.prettify())
# print('_________________________________________________________')

postlist = {}


def posting(data):
    for value in data.find_all(
            'a', class_='post-info__title post-info__title_large'):
        # print(post['href'])
        # print(post.getText())
        return postlist
