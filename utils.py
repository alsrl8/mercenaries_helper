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
