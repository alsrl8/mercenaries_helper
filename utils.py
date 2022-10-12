import requests
from bs4 import BeautifulSoup


def read_all_mercenary_names_from_wiki():
    url = 'https://hearthstone.fandom.com/wiki/Special:RunQuery?form=Mercs%2FMerc&target=&pfRunQueryFormName=Mercs%2FMerc&wpRunQuery=Run%2Bquery&MMQ%5Blayout%5D=Image&MMQ%5Bcollectible%5D=Yes&MMQ%5Bshows4%5D=SQL+Order+by&MMQ%5Bis_mercenary%5D=Yes&MMQ%5BmercenaryDefaultVariation%5D=Yes&MMQ%5BorderBy%5D=mercenaryId&MMQ%5Blevel%5D=max&MMQ%5Blimit%5D=500&MMQ%5Boffset%5D=0&pf_free_text='
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    mercenary_info = soup.find_all('div', class_='card-hover card-div')

    mercenary_names = []
    for info in mercenary_info:
        s = str(info.find('a'))
        offset = 'title="'
        i = s.find(offset)
        j = s.find('"', i + len(offset))
        mercenary_name = s[i + len(offset):j]
        mercenary_names.append(mercenary_name)
    return mercenary_names


def read_all_mercenary_names_from_local():
    mercenary_names = []
    with open('./mercenaries/All.txt', 'r') as file:
        while True:
            name = file.readline()
            if not name:
                break
            mercenary_names.append(name.rstrip())
    return mercenary_names


def write_all_mercenary_names():
    mercenary_names = read_all_mercenary_names_from_wiki()
    with open('./mercenaries/All.txt', 'w') as file:
        for name in mercenary_names:
            file.write(name + '\n')


def read_mercenary_from_wiki(mercenary_name):
    BASE_URL = "https://hearthstone.fandom.com/wiki/Mercenaries/"
    url = BASE_URL + mercenary_name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    mercenary_info = soup.find_all(class_='merc-infobox-flex')

    data = {
        'Name': mercenary_name,
        'Card type': None,
        'Role': None,
        'Rarity': None,
        'Minion type': None,
        'Faction': None,
        'mercenaryId': None
    }

    for info in mercenary_info:
        for d in info.find_all('li'):
            key, val = d.text.strip().split(': ')
            if key in data:
                data[key] = val
    return data


def read_mercenary_from_local(mercenary_name):
    data = {
        'Name': mercenary_name,
        'Card type': None,
        'Role': None,
        'Rarity': None,
        'Minion type': None,
        'Faction': None,
        'mercenaryId': None
    }
    with open(f'./mercenaries/{mercenary_name}.txt', 'r') as file:
        while True:
            s = file.readline()
            if not s:
                break
            key, val = s.split(": ")
            if key in data:
                data[key] = val
    return data


def write_mercenary_info(mercenary_name, info_filename=None):
    if not info_filename:
        info_filename = mercenary_name + '.txt'

    data = read_mercenary_from_wiki(mercenary_name)
    with open('./mercenaries/' + info_filename, 'w') as file:
        for col, val in data.items():
            file.write(f'{col}: {val}\n')
