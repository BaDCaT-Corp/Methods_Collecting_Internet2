import requests
import json
import uuid
from pymongo import MongoClient
from pprint import pprint
from bs4 import BeautifulSoup as bs     # Для обработки HTML
from bs4 import BeautifulStoneSoup      # Для обработки XML
import bs4                              # Для обработки и того и другого
from pymongo.errors import DuplicateKeyError as dke
import hashlib
import datetime

# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет добавлять
# только новые вакансии/продукты в вашу базу.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты).

def lesson_03():
    client = MongoClient('127.0.0.1', 27017)
    db = client['new_DB_job']
    job_hh = db.Jobs_hh

    dt_now = datetime.datetime.now()
    insert_count = 0
    count = 0

    name_job = input('Введите вакансию:')
    url = "https://hh.ru"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/82.0.4227.33'}

    params = {'area': '1',
              'text': name_job
              #'items_on_page': 20
              }

    #response = requests.get('https://hh.ru/search/vacancy?area=1&text=SAP').text
    link_next = url + '/search/vacancy/'

    while link_next is not None:
        response = requests.get(link_next, params=params, headers=headers)
        link_next = None
        if response.ok:

            dom = bs(response.text, 'html.parser')
            dom_list_job = dom.find_all('div', {'class': 'vacancy-serp-item'})

            for obj in dom_list_job:
                job_name = None
                job_link = None
                money_min = None
                money_max = None
                money_type = None

                job_data = {}
                job_data_r = {}

                info = obj.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
                job_name = info.text
                job_link = info.get('href')

                try:
                    money_row = obj.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                    lst = ''
                    lst = money_row.split(' ')
                    if len(lst) == 3:
                        if lst[0] == 'до':
                            money_min = None
                            money_max = lst[1]
                            money_type = lst[2]
                        elif lst[0] == 'от':
                            money_min = lst[1]
                            money_max = None
                            money_type = lst[2]
                    elif len(lst) == 4:
                        money_min = lst[0]
                        money_max = lst[2]
                        money_type = lst[3]
                except:
                    pass

                money_min = str(money_min).replace('\u202f', '')
                money_max = str(money_max).replace('\u202f', '')

                job_data['job_name'] = job_name
                job_data['link'] = job_link
                job_data['money_min'] = money_min
                job_data['money_max'] = money_max
                job_data['money_type'] = money_type
                job_data['site'] = url
                job_data['create_date'] = str(dt_now)

                row = str(job_name) + str(money_min) + str(money_max) + str(money_type)
                job_data['_id'] = str(hashlib.md5(row.encode('utf-8')).hexdigest())

                count = count + 1
                try:
                    job_hh.insert_one(job_data)
                    insert_count = insert_count + 1
                except dke:
                    pass

            try:
                next_list = dom.find('a', {'data-qa': 'pager-next'})
                link_next = url + next_list.get('href')
            except:
                link_next = None

    print('Добавлено:_' + str(insert_count) + '/' + str(count) + '_строк в MongoDB')
    # 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
    # (необходимо анализировать оба поля зарплаты).

    search_money = input('Введите минимальную ЗП вакансии:')

    for doc in job_hh.find({'$and':
                                [{'money_min': {'$gte': search_money}},
                                 {'money_min': {'$ne': 'None'} }]}):
        pprint(doc)

    for doc in job_hh.find({'$and':
                                [{"money_max": {'$gte': search_money}},
                                 {"money_max": {"$ne": "None"} }]}):
        pprint(doc)