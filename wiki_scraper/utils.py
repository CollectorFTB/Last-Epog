from selenium.webdriver.common.by import By

from driver import *

obj = lambda **kwargs: type('obj', (object,), kwargs)()

def has_class(element, cls):
    return cls in element.get_attribute('class').split()

def click_if_selected(elements):
    for element in elements:
        if has_class(element, 'selected'):
            click_elem(element)

def get_divs(element, count=999):
    for i in range(1, count+1):
        try:
            yield element.find_element(By.CSS_SELECTOR, f'div:nth-child({i})')
        except: 
            return
