import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs     #Для обработки HTML

# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы
# получаем должность) с сайтов HH и/или Superjob. Приложение должно анализировать несколько страниц сайта
# (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.

def lesson_02():
    name_job = input('Введите вакансию:')
    url = "https://hh.ru"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/82.0.4227.33'}

    params = { 'area': '1',
               'text': name_job
    }

    # response = requests.get('https://hh.ru/search/vacancy?area=1&text=SAP').text
    link_next = url+'/search/vacancy/'
    job_list = []

    while link_next is not None:
        response = requests.get(link_next, params=params, headers=headers)
        link_next = None
        if response.ok:

            dom = bs(response.text, 'html.parser')
            dom_list_job = dom.find_all('div', {'class': 'vacancy-serp-item'})

            for obj in dom_list_job:
                job_data = {}

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
                    money_row = None

                job_data['job_name'] = job_name
                job_data['link'] = job_link
                job_data['money_min'] = money_min
                job_data['money_max'] = money_max
                job_data['money_type'] = money_type
                job_data['site'] = url

                job_list.append(job_data)

                job_name = None
                job_link = None
                money_min = None
                money_max = None
                money_type = None

            try:
                next_list = dom.find('a', {'data-qa': 'pager-next'})
                link_next = url + next_list.get('href')
            except:
                link_next = None

    pprint(job_list)
