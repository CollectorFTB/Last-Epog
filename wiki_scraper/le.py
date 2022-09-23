from webbrowser import BaseBrowser, Chrome
from driver import *
from utils import *

affix_to_form = lambda x: ' '.join(x.split('\n')[::-1])


DOMAIN = 'www.lastepochtools.com'
WIKI_URL = f'http://{DOMAIN}/db'
WIKI_FORMAT = f'{WIKI_URL}/category/{{slot}}/{{category}}'

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class Wiki:
    @staticmethod
    @needs_driver
    def open_wiki(browser, slot=None, category=None):
        if slot and category:
            browser.get(WIKI_FORMAT.format(slot=slot, category=category))
            wait_for_element('item-card', By.CLASS_NAME)

            rarity_selector = browser.find_element(By.CLASS_NAME, 'rarity-selector')
            basic, *others = get_divs(rarity_selector, 3)
            click_if_selected(others)


    @staticmethod
    @needs_driver
    def scrape_items(browser: Chrome):
        output = []

        for element in browser.find_elements(By.CLASS_NAME, 'item-card'):
            description = element.find_element(By.CLASS_NAME, 'item-description')
            item_name, item_type, mods = get_divs(description, 3)
            
            if item_type.text in ['Helmet', 'Body Armour']:
                *implicits, level_req, class_req = get_divs(mods)
            else:
                (*implicits, level_req), class_req = get_divs(mods), obj(text=None)
            
            if level_req.text == "Can't drop":
                continue

            item = {
                'item_name': item_name.text,
                'level_requirement': level_req.text,
                'class': class_req.text,
                'implicits': [
                    implicit.text for implicit in implicits
                ]
            }

            output.append(item)

        return output


    @staticmethod
    @needs_driver
    def scrape_blessings(browser: Chrome):
        item_names = browser.find_elements(By.CLASS_NAME, 'item-name')
        implicits = browser.find_elements(By.CLASS_NAME, 'item-implicit')
        dropped_from = browser.find_elements(By.CLASS_NAME, 'dropped-from')

        return [
            {
                'blessing_name': item_name.text,
                'implicit': implicit.text,
                'timeline': (timeline_data := drop.text.split('\n')[1].split(' (level: '))[0],
                'level': int(timeline_data[1][:-1])
            } for item_name, implicit, drop in zip(item_names, implicits, dropped_from)
        ]


    def scrape_idols(browser: Chrome):
        item_names = browser.find_elements(By.CLASS_NAME, 'item-name')
        implicits = browser.find_elements(By.CLASS_NAME, 'item-implicit')
        dropped_from = browser.find_elements(By.CLASS_NAME, 'dropped-from')

        return [
            {
                'blessing_name': item_name.text,
                'implicit': implicit.text,
                'timeline': (timeline_data := drop.text.split('\n')[1].split(' (level: '))[0],
                'level': int(timeline_data[1][:-1])
            } for item_name, implicit, drop in zip(item_names, implicits, dropped_from)
        ]

    @staticmethod
    @needs_driver
    def scrape_affixes(browser: Chrome, slot_name):
        output = []
        for element in browser.find_elements(By.CLASS_NAME, 'item-card'):
            description = element.find_element(By.CLASS_NAME, 'item-description')
            mod_name, flavored_name, mods = get_divs(description, 3)
            
            level_req = mods.find_element(By.CLASS_NAME, 'item-req')
            rarity = mods.find_element(By.CLASS_NAME, 'rarity_tier')

            try:
                class_req = mods.find_element(By.CLASS_NAME, 'item-req2')
            except NoSuchElementException:
                class_req = obj(text=None)

            affix, *affix_tier_list = mods.find_elements(By.CLASS_NAME, 'affix')
            
            _, *affix_names = get_divs(affix)
            affix_names = [affix_to_form(affix_name.text) for affix_name in affix_names]
            
            tiers_values = []
            
            for tier in affix_tier_list:
                _, *values = get_divs(tier)
                numerical_values = [value.text for value in values]
                tiers_values.append(numerical_values)

            affix = {
                'affix_name': mod_name.text,
                'affix_form': affix_names,
                'affix_values': tiers_values,
                'level_requirement': level_req.text,
                'class_requirement': class_req.text,
                'rarity': rarity.text
            }

            output.append(affix)
        return output