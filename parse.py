import urllib.parse
from bs4 import BeautifulSoup as bs4
import pandas as pd
import requests
from fuzzywuzzy import fuzz


#selen = mos, spb, mord, 24, orenburg
from selenium import webdriver

mos_url = 'https://mos-sud.ru/search?formType=shortForm&uid=&caseNumber={number}&participant={fio}' #selen

rf_url = '{url}/modules.php?name=sud_delo&g1_case__CASE_NUMBERSS={number}&G1_PARTS__NAMESS={fio}&delo_id=1540005&op=sf'
hm_url = 'http://mirsud86.ru/activity/regions/?year={year}&sf0=&sf1={number}&sf2=&sf2_d=&sf3=&sf4=&sf5=&sf8={fio}&sf12=&sf17=' #.encode('1251')
pskov_url = 'http://mirsud.pskov.ru/courtsst/activity/caselistcs/?sf0=&sf1={number}&sf2=&sf3=&sf3_d=&sf7=&sf9=&sf10={fio}&ms=0' #.encode('1251')
stav_url = 'https://stavmirsud.ru/officework/caselistcs/?sf0=&sf11=&sf1={number}&sf2=&sf3={fio}&sf4=&sf5=&sf5_d=&sf7=&sf9=&sf10=' #.encode('1251')
tatar_url = 'http://mirsud.tatar.ru/courtservices/sz/cs/?sf0=&sf11=47&sf1={number}&sf2=&sf3={fio}&sf4=&sf5=&sf5_d=&sf7=&sf9=&sf10=' #.encode('1251')
mordovia_url = 'https://mirsud.e-mordovia.ru/Home/Records/{id}'


def get_sites(pattern_region, pattern_uch=None):
    df = pd.read_excel('msud.xlsx')  # can also index sheet by name or fetch all sheets
    names = df['Мировой суд'].tolist()
    sites = df['Сайт'].tolist()
    sites_dict = dict(zip(names, sites))
    sites = []

    for name, site in sites_dict.items():
        if pattern_region in site:
            if pattern_uch:
                if fuzz.WRatio(pattern_uch, name) > 64:
                    sites.append(site)
    return sites


def parse_requests(url):
    resp = requests.get(url)
    soup = bs4(resp, 'html.parser')

    return is_result(url, soup)


def init_chromedriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("start-maximized")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    return driver


def parse_mord(urls):
    for url in urls:
        uch_id = url.split('/')[-1]
        url_2 = mordovia_url.format(id=uch_id)
        driver = init_chromedriver()

        driver.get(url)
        resp = driver.page_source
        soup = bs4(resp, 'html.parser')



def parse_rf(urls, number='', fio=''):
    for url in urls:
        url_2 = rf_url.format(url=url, number=number, fio=fio)
        if parse_requests(url_2):
            return True, url_2


def main(region, number, fio, keys):
    if region == 'Москва':
        pass
    elif region == 'Санкт-Петербург':
        pass
    elif region == 'Татарстан':
        pass
    elif region == 'Красноярский край':
        pass
    elif region == 'Ставропольский край':
        pass
    elif region == 'Оренбургская область':
        pass
    elif region == 'Мордовия':
        pass
    elif region == 'Ханты-Мансийский АО':
        pass
    elif region == 'Псковская область':
        pass
    elif region == 'Другое':
        pass


def check_results(soup, value, elem='table'):
    table = soup.find(elem, class_=value)
    if table is not None:
        return True
    else:
        return False


def is_result(url, soup):
    if 'mirsud86' in url or 'pskov' in url or 'stavmirsud' in url or 'tatar' in url:
        result = check_results(soup, 'decision_table')

    elif 'msudrf.ru' in url:
        result = check_results(soup, 'tablcont')

    elif 'mos-sud.ru' in url:
        result = check_results(soup, 'custom_table')

    elif 'mirsud.spb.ru' in url:
        not_found = soup.find('table', class_='rwd-table')
        if 'Судебные дела, удовлетворяющие запросу, не найдены' in not_found.text:
            result = False
        else:
            result = True

    elif 'mirsud24.ru' in url:
        result = check_results(soup, 'table')

    elif 'mirsud.e-mordovia.ru' in url:
        count = int(soup.find('span', {'data-bind': 'text: RecordsCount'}).text)
        if count > 1000:
            result = False
        else:
            result = True

    elif 'kodms.ru' in url:
        divs = soup.find('div', class_='case_cases-cards__bV5uR').find_all('div', class_='case_case-card__2u6zk')
        if not divs:
            result = False
        else:
            result = True

    return result

# print(urllib.parse.quote_plus('Бело'.encode('1251')))