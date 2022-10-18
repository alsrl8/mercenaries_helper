from urllib import request
import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import json


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
    if not os.path.exists('./mercenaries/'):
        os.mkdir('./mercenaries/')
    if not os.path.exists('./mercenaries/All.txt'):
        with open('./mercenaries/All.txt', 'w', encoding='UTF-8') as file:
            for name in mercenary_names:
                file.write(name + '\n')


def read_mercenary_from_wiki(mercenary_name):
    url = "https://hearthstone.fandom.com/wiki/Mercenaries/" + mercenary_name
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
        'mercenaryId': None,
    }

    for info in mercenary_info:
        for d in info.find_all('li'):
            key, val = d.text.strip().split(': ')
            if key in data:
                data[key] = val

        # download image of mercenary from wiki
        filepath = f"./static/images/mercenaries/{data['Name']}.png"
        # skip downloading image if there is already image in the directory
        if not os.path.exists(filepath):
            for d in info.find_all('a', class_='image'):
                url = d['href']
                request.urlretrieve(url, filepath)

    return data


def read_ability_names_from_wiki(mercenary_name):
    url = "https://hearthstone.fandom.com/wiki/Mercenaries/" + mercenary_name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    ability_info = soup.find_all(class_='ability-infobox-flex')

    ability_names = []
    for info in ability_info:
        ability_name = info.find('div', class_='title').text
        ability_names.append(ability_name)
    return ability_names


def read_ability_from_wiki(ability_name):
    url = "https://hearthstone.fandom.com/wiki/Mercenaries/" + ability_name.replace('?', '%3F')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    ability_info = soup.find_all(class_='ability-infobox-flex')

    data = {
        'Name': ability_name,
        'Card type': None,
        'Speed': None,
        'Cooldown': None,
        'Spell school': None,
        'Text': None
    }

    assert len(ability_info) > 0, f'ability_name: {ability_name}, ability_info: {ability_info}'

    for d in ability_info[0].find_all('li'):
        key, val = d.text.strip().split(': ')
        if key in data:
            data[key] = val
    data['Text'] = ability_info[0].find('div', class_='text').text.split('\n')[0]

    if data['Card type'] == 'Equipment':
        data = {
            'Name': data['Name'],
            'Card type': data['Card type'],
            'Text': data['Text']
        }

    filepath = './static/images/abilities/' if data['Card type'] == 'Ability' else './static/images/equipments/'
    filepath += f'{validate_filename(ability_name)}.png'
    if not os.path.exists(filepath):
        for url in ability_info[0].find('div', class_='card-image').find_all('a'):
            request.urlretrieve(url['href'], filepath)

    return data


def read_mercenary_from_local(mercenary_name):
    data = {
        'Name': mercenary_name,
        'Card type': None,
        'Role': None,
        'Rarity': None,
        'Minion type': None,
        'Faction': None,
        'mercenaryId': None,
        # 'equipments': None,
        # 'abilities': None
    }
    with open(f'./mercenaries/{mercenary_name}.txt', 'r') as file:
        while True:
            s = file.readline()
            if not s:
                break
            s = s.split(': ')
            key = s[0]
            if key in data:
                data[key] = s[1].rstrip()
    return data


def write_mercenary_info(mercenary_name, info_filename=None):
    if not info_filename:
        info_filename = mercenary_name + '.txt'
    mercenary_data = read_mercenary_from_wiki(mercenary_name)
    ability_names = read_ability_names_from_wiki(mercenary_name)
    equipments, abilities = [], []
    for ability_name in ability_names:
        ability_data = read_ability_from_wiki(ability_name)
        if ability_data['Card type'] == 'Equipment':
            equipments.append(ability_data)
        elif ability_data['Card type'] == 'Ability':
            abilities.append(ability_data)

    if not os.path.exists('./mercenaries/'):
        os.mkdir('./mercenaries/')
    if not os.path.exists('./mercenaries/' + info_filename):
        with open('./mercenaries/' + info_filename, 'w', encoding='UTF-8') as file:
            for col, val in mercenary_data.items():
                file.write(f'{col}: {val}\n')
            file.write(f'equipments: {equipments}\n')
            file.write(f'abilities: {abilities}\n')


def write_all_mercenaries():
    write_all_mercenary_names()
    mercenary_names = read_all_mercenary_names_from_local()
    for name in tqdm(mercenary_names):
        write_mercenary_info(name)
        print(f'mercenary: {name}')


def validate_filename(filename):
    s = convert_colon_to_modifier_colon(filename)
    s = s.replace('?', '')
    s = s.replace('"', '')
    return s


def convert_colon_to_modifier_colon(s: str):
    return s.replace(':', '꞉').replace('?', '')


def convert_modifier_colon_to_colon(s: str):
    return s.replace('꞉', ':')
