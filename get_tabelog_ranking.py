#!/usr/bin/env python

import json
import argparse
from selenium import webdriver
from time import sleep

profile = ""
driver = ""
timeout = 30

TABELOG_URL = 'https://tabelog.com'
AREA_FORM_XPATH = '//*[@id="sa"]'
KEYWORD_FORM_XPATH = '//*[@id="sk"]'
SEARCH_BTN_XPATH = '//*[@id="js-global-search-btn"]'
RANKING_BTN_CSS = 'navi-rstlst__tab--rank'
RANKING_LIST_CSS = 'list-rst__rst-name-target'
RANKING_STAR_LIST_CSS = 'list-rst__rating-val'


class ShopInfo:
    def __init__(self):
        self.name = ''
        self.star = 0
        self.address = ''
        self.rank = 0


def get_tabelog_ranking(driver: webdriver, area: str, keyword: str):
    result = list()

    driver.get(TABELOG_URL)
    driver.set_page_load_timeout(timeout)
    sleep(1)

    driver.find_element_by_xpath(AREA_FORM_XPATH).send_keys(area)
    driver.find_element_by_xpath(KEYWORD_FORM_XPATH).send_keys(keyword)
    driver.find_element_by_xpath(SEARCH_BTN_XPATH).click()
    driver.set_page_load_timeout(timeout)
    sleep(1)

    driver.find_elements_by_class_name(RANKING_BTN_CSS)[0].click()
    driver.set_page_load_timeout(timeout)
    sleep(1)

    ranking = driver.find_elements_by_class_name(RANKING_LIST_CSS)
    ranking_star = driver.find_elements_by_class_name(RANKING_STAR_LIST_CSS)
    for index, shop in enumerate(ranking):
        if hasattr(shop, "text"):
            newShop = ShopInfo()
            newShop.name = shop.text
            newShop.rank = index + 1
            newShop.star = ranking_star[index].text
            result.append(newShop)

    return result


def default_method(item):
    if isinstance(item, object) and hasattr(item, '__dict__'):
        return item.__dict__
    else:
        raise TypeError


if __name__ == "__main__":
    # Setup commandline
    parser = argparse.ArgumentParser(description="Get tabelog ranking(top 20)")
    parser.add_argument('--area', type=str, help='search area')
    parser.add_argument('--keyword', type=str, help='search keyword')
    args = parser.parse_args()

    # Setup webdriver
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy-type", 4)
    driver = webdriver.Firefox(
        firefox_profile=profile, executable_path='./geckodriver')

    ranking = get_tabelog_ranking(driver, args.area, args.keyword)
    driver.quit()

    print(json.dumps(ranking, default=default_method, indent=2, ensure_ascii=False))
