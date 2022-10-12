import requests
from bs4 import BeautifulSoup


def read_wiki_sources(wiki_source_filename, data_filename):
    print('Scraping wiki page sources')
    mercenary_names = []
    with open(wiki_source_filename, 'r') as wiki:
        while True:
            s = wiki.readline()
            if not s:
                print(f'Finished scraping wiki page sources. number of cards: {len(mercenary_names)}')
                with open(data_filename, 'w') as w_data:
                    for name in mercenary_names:
                        w_data.write(name + '\n')
                break
            else:
                i = s.find('alt=')
                if i == -1:
                    continue
                j = s.find('"', i + len('alt="'))
                name = s[i + 5:j]
                name = name.replace('&#39;', '\'')  # fix apostrophe correctly
                mercenary_names.append(name)


def read_all_mercenary_names_from_wiki():
    url = 'https://hearthstone.fandom.com/wiki/Special:RunQuery?form=Mercs%2FMerc&target=&pfRunQueryFormName=Mercs%2FMerc&wpRunQuery=Run%2Bquery&MMQ%5Blayout%5D=Image&MMQ%5Bcollectible%5D=Yes&MMQ%5Bshows4%5D=SQL+Order+by&MMQ%5Bis_mercenary%5D=Yes&MMQ%5BmercenaryDefaultVariation%5D=Yes&MMQ%5BorderBy%5D=mercenaryId&MMQ%5Blevel%5D=max&MMQ%5Blimit%5D=500&MMQ%5Boffset%5D=0&pf_free_text='
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    mercenary_info = soup.find_all('div', class_='card-hover card-div')

    mercenary_names = []
    for info in mercenary_info:
        s = str(info.find('a'))
        i = s.find('title="')
        j = s.find('"', i + 7)
        mercenary_name = s[i + 7:j]
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


def read_wiki_mercenary(mercenary_name):
    BASE_URL = "https://hearthstone.fandom.com/wiki/Mercenaries/"
    url = BASE_URL + mercenary_name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    mercenary_info = soup.find_all(class_='merc-infobox-flex')

    data = {
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


def write_mercenary_info(mercenary_name, info_filename=None):
    if not info_filename:
        info_filename = mercenary_name + '.txt'

    data = read_wiki_mercenary(mercenary_name)
    with open('./mercenaries/' + info_filename, 'w') as file:
        file.write(f'Name: {mercenary_name}\n')
        for col, val in data.items():
            file.write(f'{col}: {val}\n')
