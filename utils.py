from urllib import request
import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import json
from collections import defaultdict


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
    with open('./mercenaries/All.json', 'r') as file:
        mercenary_names = json.load(file)
    return mercenary_names


def read_all_bounty_names_with_links_from_wiki():
    url = 'https://hearthstone.fandom.com/wiki/Special:RunQuery/Mercs/Bounty?pfRunQueryFormName=Mercs%2FBounty&MBQ%5Bcollapsed%5D=False&MBQ%5BoriginalPage%5D=&MBQ%5Bis_heroic%5D=&MBQ%5BbountySetNames%5D=&MBQ%5BbountyNames%5D=&MBQ%5BmercenaryNames%5D=&MBQ%5BmercenaryRarities%5D=&MBQ%5Blimit%5D=&MBQ%5Blayout%5D=layout2&wpRunQuery=&pf_free_text='
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    bounty_info = soup.find_all('div', class_='mw-parser-output')
    info = bounty_info[1]  # skip basic setting information
    info = info.find_all('tr')
    bounty_names, links = [], []
    for idx in range(1, len(info)):  # skip column information
        tag = info[idx].find('a')
        bounty = tag.text
        bounty_names.append(bounty)
        s = str(tag)
        offset = 'href="'
        i = s.find(offset)
        j = s.find('"', i + len(offset))
        link = s[i + len(offset):j]
        links.append(link)
    return bounty_names, links


def read_all_bounty_names_with_links_from_local():
    with open('./bounties/All.json', 'r') as file:
        data = json.load(file)
    return data


def write_all_mercenary_names():
    if os.path.exists('./bounties/All.json'):
        return

    mercenary_names = read_all_mercenary_names_from_wiki()

    if not os.path.exists('./mercenaries/'):
        os.mkdir('./mercenaries/')
    with open('./mercenaries/All.json', 'w', encoding='UTF-8') as file:
        json.dump(mercenary_names, file, indent=4)


def write_all_bounty_names():
    if os.path.exists('./bounties/All.json'):
        return

    bounty_names, links = read_all_bounty_names_with_links_from_wiki()
    bounties = defaultdict(dict)
    for name, link in zip(bounty_names, links):
        if link.endswith('(Heroic)'):
            bounties[name]['Heroic'] = link
        else:
            bounties[name]['Normal'] = link

    # Incorrect link information is entered in wiki, so correct it manually
    bounties['Neeru_Fireblade']['Normal'] = '/wiki/Mercenaries/Neeru_Fireblade_(Normal)'

    if not os.path.exists('./bounties/'):
        os.mkdir('./bounties/')
    with open('./bounties/All.json', 'w', encoding='UTF-8') as file:
        json.dump(bounties, file, indent=4)


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


def read_all_abilities_from_wiki(ability_names):
    equipments, abilities = [], []
    for ability_name in ability_names:
        ability_data = read_ability_from_wiki(ability_name)
        if ability_data['Card type'] == 'Equipment':
            equipments.append(ability_data)
        elif ability_data['Card type'] == 'Ability':
            abilities.append(ability_data)
    return equipments, abilities


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
    with open(f'./mercenaries/{mercenary_name}.json', 'r') as file:
        data = json.load(file)
    return data


def read_bounty_from_wiki(bounty_name, link):
    url = 'https://hearthstone.fandom.com/' + link
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    bounty_info = soup.find_all('div', class_='card-hover card-div')
    boss_info_link = bounty_info[0].find('a')['href']

    data = {
        'Name': bounty_name,
        'Boss Link': boss_info_link,
        'Zone': None,
        'Coin Loots': []
    }

    coin_loots = soup.find_all('div', class_='list-cards')[0].find_all('div', class_='card-hover card-div')
    for coin_loot in coin_loots:
        coin_name = coin_loot.find('a')['title']
        data['Coin Loots'].append(coin_name)

    zone = soup.find_all('span', class_='new')[0].text
    data['Zone'] = zone

    return data


def write_mercenary_info(mercenary_name):
    info_filename = mercenary_name + '.json'
    mercenary_data = read_mercenary_from_wiki(mercenary_name)
    ability_names = read_ability_names_from_wiki(mercenary_name)
    equipments, abilities = read_all_abilities_from_wiki(ability_names)
    mercenary_data['Equipments'] = equipments
    mercenary_data['Abilities'] = abilities

    if not os.path.exists('./mercenaries/'):
        os.mkdir('./mercenaries/')
    if not os.path.exists('./mercenaries/' + info_filename):
        with open('./mercenaries/' + info_filename, 'w', encoding='UTF-8') as file:
            json.dump(mercenary_data, file, indent=4)


def write_all_mercenaries():
    write_all_mercenary_names()
    mercenary_names = read_all_mercenary_names_from_local()
    for name in tqdm(mercenary_names):
        write_mercenary_info(name)
        print(f'mercenary: {name}')


def write_bounty_info(bounty_name, links):
    info_filename = bounty_name + '.json'
    info_filename = convert_colon_to_modifier_colon(info_filename)
    bounty_data = dict()
    for difficulty in ['Normal', 'Heroic']:
        if difficulty not in links:
            continue
        data = read_bounty_from_wiki(bounty_name, links[difficulty])
        bounty_data[difficulty] = data

    if not os.path.exists('./bounties'):
        os.mkdir('./bounties')
    if not os.path.exists('./bounties/' + info_filename):
        with open('./bounties/' + info_filename, 'w', encoding='UTF-8') as file:
            json.dump(bounty_data, file, indent=4)


def write_all_bounties():
    write_all_bounty_names()
    data = read_all_bounty_names_with_links_from_local()
    for name, links in data.items():
        write_bounty_info(name, links)


def validate_filename(filename):
    s = convert_colon_to_modifier_colon(filename)
    s = s.replace('?', '')
    s = s.replace('"', '')
    return s


def convert_colon_to_modifier_colon(s: str):
    return s.replace(':', '꞉').replace('?', '')


def convert_modifier_colon_to_colon(s: str):
    return s.replace('꞉', ':')
