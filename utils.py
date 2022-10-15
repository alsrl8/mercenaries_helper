import requests
from bs4 import BeautifulSoup
import os


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

def read_equipment_from_wiki_by_mercenary_id(mercenary_id):
    url = 'https://hearthstone.fandom.com/wiki/Special:RunQuery/Mercs/Equipment?pfRunQueryFormName=Mercs%2FEquipment&MEQ%5Bname%5D=&MEQ%5BdbfId%5D=&MEQ%5Bid%5D=&MEQ%5Btext%5D=&MEQ%5BtextAdvanced%5D%5Bis_checkbox%5D=true&MEQ%5Bcollapsed%5D=False&MEQ%5BoriginalPage%5D=&MEQ%5Blayout%5D=Image&MEQ%5Bwidth%5D=&MEQ%5Bsorts%5D%5Bis_list%5D=1&MEQ%5Bmap_field%5D%5Bsorts%5D=true&MEQ%5Blimit%5D=500&MEQ%5Bshows%5D%5B1%5D=Tier&MEQ%5Bshows%5D%5Bis_list%5D=1&MEQ%5Bshows2%5D%5Bis_list%5D=1&MEQ%5Bshows3%5D%5Bis_list%5D=1&MEQ%5Bshows4%5D%5B0%5D=SQL+Where&MEQ%5Bshows4%5D%5Bis_list%5D=1&MEQ%5Btier%5D%5B4%5D=4&MEQ%5Btier%5D%5Bis_list%5D=1&MEQ%5Bwhere%5D=cargo__MercenaryEquipment.mercenaryId+%3D+' + f'{mercenary_id}' + '&wpRunQuery=&pf_free_text='
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)

    pass


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
    if not os.path.exists('./mercenaries/'):
        os.mkdir('./mercenaries/')
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
            key, val = s.rstrip().split(": ")
            if key in data:
                data[key] = val
    return data


def write_mercenary_info(mercenary_name, info_filename=None):
    if not info_filename:
        info_filename = mercenary_name + '.txt'

    data = read_mercenary_from_wiki(mercenary_name)

    if not os.path.exists('./mercenaries/'):
        os.mkdir('./mercenaries/')
    with open('./mercenaries/' + info_filename, 'w') as file:
        for col, val in data.items():
            file.write(f'{col}: {val}\n')


def write_all_mercenaries():
    write_all_mercenary_names()
    mercenary_names = read_all_mercenary_names_from_local()
    for name in mercenary_names:
        write_mercenary_info(name)
