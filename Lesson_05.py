import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

# Вариант I
# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах
# в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#
#
# Вариант II
# 2) Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД. Сайт можно
# выбрать и свой. Главный критерий выбора: динамически загружаемые товары

def lesson_05():
    client = MongoClient('127.0.0.1', 27017)
    db = client['DB_mailru']
    emails = db.emails
    emails.delete_many({})

    chrome_option = Options()
    chrome_option.add_argument('start-maximized')
    chrome_option.add_argument("--headless")  # Режим без интерфейса

    driver = webdriver.Chrome(options=chrome_option)

    driver.get('https://account.mail.ru/login')
    driver.implicitly_wait(10)

    elem = driver.find_element(By.XPATH, "//input[@name='username']")
    elem.send_keys("study.ai_172")

    elem = driver.find_element(By.XPATH, "//div[@class='login-row']/div/div/div/button")
    elem.send_keys(Keys.ENTER)

    elem = driver.find_element(By.XPATH, "//input[@name='password']")
    elem.send_keys("NextPassword172#")

    elem = driver.find_element(By.XPATH, "//div[@class='login-row']/div/div/div/div/button")
    elem.send_keys(Keys.ENTER)
    driver.implicitly_wait(3)

    emails_set = set()

    for i in range(10):
        rows = driver.find_elements(By.XPATH, "//a[contains(@class, 'js-letter-list-item')]")
        for obj in rows:
            emails_set.add(obj.get_attribute('href'))
        actions = ActionChains(driver)
        actions.move_to_element(rows[-1])
        actions.perform()
        time.sleep(4)

    for link in emails_set:
        driver.get(link)
        author = driver.find_element(By.XPATH, "//div[contains(@class, 'letter__author')]/span[contains(@class, 'letter-contact')]").text
        date = driver.find_element(By.XPATH, "//div[contains(@class, 'letter__author')]/div[contains(@class, 'letter__date')]").text
        subject = driver.find_element(By.XPATH, "//h2[contains(@class, 'thread-subject')]").text
        text = driver.find_element(By.XPATH, "//div[contains(@class, 'letter-body__body-content')]").text

        email = {
            'author': author,
            'datetime': date.replace('Сегодня,', datetime.now().strftime("%Y-%m-%d")),
            'subject': subject,
            'text': text
        }
        emails.insert_one(email)

    driver.close()