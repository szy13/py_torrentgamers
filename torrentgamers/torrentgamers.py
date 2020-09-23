import requests
from urllib.parse import urljoin

from bs4 import BeautifulSoup


BASE_URL = 'https://torrent-gamers.net'
PARSE_MODE = 'html.parser'


class TorrentGamers:
    """TorrentGamers class provides interaction with torrent-gamers site"""

    @property
    def categories(self):
        """Get categories list

        :return: list of categories represented in TorrentCategory objects
        :rtype: list
        """
        result = []

        response = requests.get(BASE_URL)
        bs = BeautifulSoup(response.text, PARSE_MODE)

        menu = bs.find('div', {'class': 'list-col menu'})
        for cat in menu.find_all('li'):
            url = cat.find('a').get('href')
            result.append(TorrentCategory(cat.text, url))

        return result


class TorrentCategory:
    """TorrentCategory class that represents torrent-gamers site categories

    :param name: category name
    :type name: str

    :param url: category url
    :type url: str
    """
    __slots__ = ('name', 'url')

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f'<{self.__class__.__name__}:{self.name}>'

    def __str__(self):
        return self.name

    @property
    def pages_count(self):
        response = requests.get(self.url)
        bs = BeautifulSoup(response.text, PARSE_MODE)

        try:
            div = bs.find('div', {'id': 'bottom-nav', 'class': 'navigation'})
            links = div.find('div', {'class': 'links'})

            return int(links.find_all('a')[-1].text)
        except AttributeError:
            return 1

    def get_games(self, page=1):
        """Get list of cames from category

        :param page: category page
        :type page: int

        :return: list of found games represented in TorrentGame objects
        :rtype: list
        """
        response = requests.get(urljoin(self.url, f'page/{page}'))
        bs = BeautifulSoup(response.text, PARSE_MODE)

        block = bs.find('div', {'id': 'dle-content'})
        for game in block.find_all_next('a', {'class': 'shortstory'}):
            game = TorrentGame.parse(game.get('href'))
            yield game


class TorrentGame:
    """TorrentGame class that represents torrent-gamers game or software

    :param url: torrent-gamers url
    :type url: str

    :param cover_url: cover url
    :type cover_url: str

    :param download_url: download url
    :type download_url: str

    :param title: title
    :type title: str

    :param desc: desciption
    :type desc: str

    :param size: size
    :type size: str

    :param info: info
    :type info: dict

    :param system: system info
    :type system: dict

    :param screens: screenshots
    :type screens: list

    :param videos: videos
    :type videos: list
    """
    __slots__ = (
        'url', 'cover_url', 'download_url',
        'title', 'desc', 'size',
        'info', 'system',
        'screens', 'videos'
    )

    def __init__(
        self,
        url, cover_url, download_url,
        title, desc, size,
        info, system,
        screens, videos
    ):
        self.url = url
        self.cover_url = cover_url
        self.download_url = download_url

        self.title = title
        self.desc = desc
        self.size = size

        self.info = info
        self.system = system

        self.screens = screens
        self.videos = videos

    def __repr__(self):
        return f'<{self.__class__.__name__}:{self.title}> {self.size}'

    def parse(url):
        """Get game data from url

        :param url: game url
        :type url: str

        :return: game object
        :rtype: TorrentGame
        """
        response = requests.get(url)
        bs = BeautifulSoup(response.text, PARSE_MODE)

        cover_url = TorrentGame._parse_cover_url(bs)
        download_url = TorrentGame._parse_download_url(bs)
        title = TorrentGame._parse_title(bs)
        desc = TorrentGame._parse_description(bs)
        size = TorrentGame._parse_size(bs)
        info = TorrentGame._parse_info(bs)
        system = TorrentGame._parse_system(bs)
        screens = TorrentGame._parse_screens(bs)
        videos = TorrentGame._parse_videos(bs)

        return TorrentGame(
            url, cover_url, download_url,
            title, desc, size,
            info, system,
            screens, videos
        )

    def _parse_cover_url(bs):
        try:
            cover_url = bs.find('div', {'class': 'img-box'}).find('img')['src']
            return BASE_URL + cover_url
        except AttributeError:
            return None

    def _parse_download_url(bs):
        try:
            return bs.find('div', {'class': 'title ps-link'}).get('href')
        except AttributeError:
            return None

    def _parse_title(bs):
        try:
            return bs.find('div', {'class': 'title-box'}).text.strip()
        except AttributeError:
            return None

    def _parse_description(bs):
        try:
            fullstory = bs.find('div', {'class': 'fullstory'})
            return fullstory.find('div', {'class': 'content'}).text
        except AttributeError:
            return None

    def _parse_size(bs):
        try:
            download_box = bs.find('div', {'class': 'download-box flex'})
            size_box = download_box.find('div', {'class': 'size-box'})
            return size_box.find('span').text
        except AttributeError:
            return None

    def _parse_info(bs):
        try:
            info = {}

            for li in bs.find('ul', {'class': 'game-info'}).find_all('li'):
                name = li.find_all('p')[0].text[:-1]
                val = li.find_all('p')[1]

                if name == 'Жанр':
                    val = [(a.get('href'), a.text) for a in val.find_all('a')]
                else:
                    val = val.text

                info[name] = val

            return info
        except AttributeError:
            return None

    def _parse_system(bs):
        try:
            system = {}

            for div in bs.find_all('div', {'class': 'system'}):
                title = div.find('div', {'class': 'title'}).text[:-2]
                content = div.find('div', {'class': 'content'})
                content = [li.text for li in content.find('ul').find_all('li')]

                system[title] = content

            return system
        except AttributeError:
            return None

    def _parse_screens(bs):
        try:
            screens = bs.find('div', {'class': 'screens'})
            return [a.get('href') for a in screens.find_all('a')]
        except AttributeError:
            return None

    def _parse_videos(bs):
        try:
            return [v['src'] for v in bs.find_all('iframe')]
        except AttributeError:
            return None
