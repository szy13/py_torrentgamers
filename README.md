# torrentgamers
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

The torrent-gamers web scraping module

![license](https://img.shields.io/github/license/szy13/py_torrentgamers)
[![telegram](https://img.shields.io/badge/telegram-szyxiii-blue)](https://t.me/szyxiii)

## Requirements
* [requests](https://pypi.org/project/requests/) - http(s) library
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) - web scraping library


## Installation
Legacy setup
```
$ python3 setup.py install
```
Pip
```
No pip installation for now
```

## Usage
Get torrents categories
```python
from torrentgamers import TorrentGamers

tg = TorrentGamers()

print(tg.categories)
```

Get torrent category pages count
```python
from torrentgamers import TorrentGamers

tg = TorrentGamers()

for category in tg.categories:
	print('{} - {} page(s)'.format(category, category.pages_count))
```

Get torrent category games
```python
from torrentgamers import TorrentGamers

tg = TorrentGamers()

category = tg.categories[0]

for game in category.get_games():
	print(game)
```

From desired page
```python
from torrentgamers import TorrentGamers

tg = TorrentGamers()

category = tg.categories[0]

for game in category.get_games(page=10):
	print(game)
```

From all pages
```python
from torrentgamers import TorrentGamers

tg = TorrentGamers()

category = tg.categories[0]

for page in range(category.pages_count):
	for game in category.get_games(page):
		print(game)
```