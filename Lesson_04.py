from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
import hashlib
from lxml import html
import requests
from pprint import pprint

# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД
# Минимум один сайт, максимум - все три

def lesson_04():
    client = MongoClient('127.0.0.1', 27017)
    db = client['DB_news_20220107']
    db_news = db.news

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/82.0.4227.33'}
    url = "https://news.mail.ru"

    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)

    list_news = []

    items = dom.xpath("//div[contains(@class ,'daynews__item')]")
    for item in items:
        news={}
        name_news = item.xpath(".//span[contains(@class,'photo__title_new_hidden')]/text()")
        link_news = item.xpath(".//span[contains(@class,'photo__title_new_hidden')]/../../@href")

        row = str(name_news)
        news['_id'] = str(hashlib.md5(row.encode('utf-8')).hexdigest())
        news['name'] = name_news
        news['link'] = link_news
        news['source'] = None
        news['datetime'] = None

        for link in link_news:
            sub_response = requests.get(link, headers=headers)
            sub_dom = html.fromstring(sub_response.text)
            datetime_dom = sub_dom.xpath("//div[contains(@class,'breadcrumbs')]")
            for subdom in datetime_dom:
                datetime = subdom.xpath(".//span[contains(@class,'js-ago')]/@datetime")
                source = subdom.xpath(".//span[contains(@class,'link__text')]/text()")
            news['datetime'] = datetime
            news['source'] = source

        try:
            pass
            db_news.insert_one(news)
        except dke:
            pass
        list_news.append(news)


    items = dom.xpath("//ul[@class='list list_type_square list_half js-module']")
    items = items[0].xpath(".//li[@class='list__item']")
    for item in items:
        news = {}
        name_news = item.xpath(".//a[@class='list__text']/text()")
        link_news = item.xpath(".//a[@class='list__text']/@href")

        row = str(name_news)
        news['_id'] = str(hashlib.md5(row.encode('utf-8')).hexdigest())
        news['name'] = name_news
        news['link'] = link_news
        news['source'] = None
        news['datetime'] = None

        for link in link_news:
            sub_response = requests.get(link, headers=headers)
            sub_dom = html.fromstring(sub_response.text)
            datetime_dom = sub_dom.xpath("//div[contains(@class,'breadcrumbs')]")
            for subdom in datetime_dom:
                datetime = subdom.xpath(".//span[contains(@class,'js-ago')]/@datetime")
                source = subdom.xpath(".//span[contains(@class,'link__text')]/text()")
            news['datetime'] = datetime
            news['source'] = source

        try:
            pass
            db_news.insert_one(news)
        except dke:
            pass
        list_news.append(news)

    items = dom.xpath("//div[@class='cols__inner']")
    for item in items:
        news = {}
        link_news = item.xpath(".//a[contains(@class,'newsitem__title')]/@href")
        name_news = item.xpath(".//a[contains(@class,'newsitem__title')]/span/text()")
        row = str(name_news)
        news['_id'] = str(hashlib.md5(row.encode('utf-8')).hexdigest())
        news['name'] = name_news
        news['link'] = link_news
        news['source'] = None
        news['datetime'] = None

        for link in link_news:
            sub_response = requests.get(link, headers=headers)
            sub_dom = html.fromstring(sub_response.text)
            datetime_dom = sub_dom.xpath("//div[contains(@class,'breadcrumbs')]")
            for subdom in datetime_dom:
                datetime = subdom.xpath(".//span[contains(@class,'js-ago')]/@datetime")
                source = subdom.xpath(".//span[contains(@class,'link__text')]/text()")
            news['datetime'] = datetime
            news['source'] = source
        try:
            pass
            db_news.insert_one(news)
        except dke:
            pass
        list_news.append(news)

        subitems = item.xpath(".//li[@class='list__item']")
        for subitem in subitems:
            news = {}
            link_news = subitem.xpath(".//a[contains(@class,'link link_flex')]/@href")
            name_news = subitem.xpath(".//a[contains(@class,'link link_flex')]/span/text()")

            row = str(name_news)
            news['_id'] = str(hashlib.md5(row.encode('utf-8')).hexdigest())
            news['name'] = name_news
            news['link'] = link_news
            news['source'] = None
            news['datetime'] = None

            for link in link_news:
                sub_response = requests.get(link, headers=headers)
                sub_dom = html.fromstring(sub_response.text)
                datetime_dom = sub_dom.xpath("//div[contains(@class,'breadcrumbs')]")
                for subdom in datetime_dom:
                    datetime = subdom.xpath(".//span[contains(@class,'js-ago')]/@datetime")
                    source = subdom.xpath(".//span[contains(@class,'link__text')]/text()")
                news['datetime'] = datetime
                news['source'] = source

            try:
                pass
                db_news.insert_one(news)
            except dke:
                pass
            list_news.append(news)

    pprint(list_news)

    pass