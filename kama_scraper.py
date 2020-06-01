import json
from urllib.request import urlopen

from bs4 import BeautifulSoup


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls


@auto_str
class Postura:
    def __init__(self, url, title, img, description):
        self.url = url
        self.title = title
        self.img = img
        self.description = description

    def as_dict(self):
        return vars(self)


def parse_urls(urls):
    objects = []
    for url in urls:
        html = urlopen(url)
        soup = BeautifulSoup(html.read(), "html.parser")
        soup.encode("utf-8")
        title = soup.find('div', {'class': 'title-holder'}).text.strip()
        img = soup.find('img')['src']
        description = soup.find('p', {'id': 'chapo'}).text.strip().replace(
            u'\u200b', '')
        print(title, description)
        p = Postura(url, title, img, description).as_dict()
        print(p)
        objects.append(p)

    return objects


def get_urls():
    urls = []
    for i in range(1, 6):
        html = urlopen(
            'https://www.enfemenino.com/sexualidad/100-posiciones-del-kamasutra-tp122366.html?p={}'.format(
                i))
        soup = BeautifulSoup(html.read(), "html.parser")
        urls += [a['href'] for a in
                 soup.find_all('a', {'class': 'title'}, href=True)]

    return urls


def main():
    urls = get_urls()
    postures = parse_urls(urls)
    print(json.dumps(postures, indent=4, ensure_ascii=False))
    with open('kama.json', 'w') as fout:
        json.dump(postures, fout, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
