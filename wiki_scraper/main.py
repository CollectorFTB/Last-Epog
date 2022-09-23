import os
import sys
from pprint import pprint as pp
from selenium import webdriver

from driver import driver
from le import Wiki

SLOTS = ['helms', 'chest', 'gloves', 'boots', 'belts', 'rings', 'amulets']
AFFIXES = ['prefixes', 'suffixes']

SLOT_TO_SLOT_NAME = {
    'helms': 'Helmet',
    'chest': 'Body Armour',
    'gloves': 'Gloves',
    'boots': 'Boots',
    'rings': 'Ring',
    'belts': 'Belt',
    'amulets': 'Amulet',
}

import json

DIR_NAME = 'output/'

def d(data, name):
    with open(f'{name}.json', 'w') as f:
        json.dump(data, f)



def items_main():
    if not os.path.isdir(DIR_NAME):
        os.mkdir(DIR_NAME)

    for slot in SLOTS:
        
        Wiki.open_wiki(slot=slot, category='items')
        items = Wiki.scrape_items()
        
        slot_dir_name = f'{DIR_NAME}/{slot}'
        if not os.path.isdir(slot_dir_name):
            os.mkdir(slot_dir_name)
        d(items, f'{slot_dir_name}/bases')

        for affix in AFFIXES:
            Wiki.open_wiki(slot=slot, category=affix)       
            affix_mods = Wiki.scrape_affixes(SLOT_TO_SLOT_NAME[slot])
            d(affix_mods, f'{slot_dir_name}/{affix}')

def blessings_main():
    if not os.path.isdir(DIR_NAME):
        os.mkdir(DIR_NAME)

    slot = 'blessings'        
    Wiki.open_wiki(slot=slot, category='items')
    items = Wiki.scrape_blessings()
        
    slot_dir_name = f'{DIR_NAME}/{slot}'
    if not os.path.isdir(slot_dir_name):
        os.mkdir(slot_dir_name)
    d(items, f'{slot_dir_name}/bases')


mains = {
    'blessings': blessings_main,
    'items': items_main
}

if __name__ == '__main__':
    if sys.platform == 'NT':
        browser = webdriver.Chrome
        executable_path = './driver/chromedriver.exe' 
    else:
        browser = webdriver.Firefox  
        executable_path = './driver/geckodriver'
    
    with driver(browser, executable_path):
        mains[sys.argv[1]]()