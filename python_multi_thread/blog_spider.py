import requests
from bs4 import BeautifulSoup

urls = [
    f"https://www.cnblogs.com/#p{page}"
    for page in range(1, 50 + 1)
]


def crawler(url):
    response = requests.get(url)
    # print(url, len(response.text))
    return response.text


def parse(html):
    # soup = BeautifulSoup(html, 'lxml')
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a", class_="post-item-title")
    return [(link['href'], link.get_text()) for link in links]

if __name__ == '__main__':
    for result in parse(crawler(urls[1])):
        print(result)