import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re
import json

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
headers = Headers(browser='firefox', os='win').generate()
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, features='html.parser')
vacancyes_list = soup.find(id="a11y-main-content")
vacancyes = vacancyes_list.find_all(class_='serp-item')

glob_list = []
data = {}


def get_vacancy():
    for vacancy in vacancyes:
        vacancy_title = vacancy.find('a', class_='serp-item__title').text
        vacancy_url = vacancy.find('a', class_='serp-item__title')['href']
        try:
            vacancy_salary = vacancy.find('span', class_="bloko-header-section-3").text.replace('\u202f', '')
        except:
            vacancy_salary = 'не указана'
        company_name = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', ' ')
        city = \
        vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'}).text.split(', ')[
            0]
        # print(vacancy_title, vacancy_url, vacancy_salary, company_name, city)
        vacancy_description_html = requests.get(vacancy_url, headers=headers).text
        vacancy_body = BeautifulSoup(vacancy_description_html, features='lxml').find('div',
                                                                                     class_='g-user-content').text
        key_words = re.findall('Django|Flask', vacancy_body, flags=re.I)
        if not key_words:
            print('Нет ключевых слов поиска')
        else:
            list_elem = {'Вакансия': vacancy_title, 'Ссылка': vacancy_url, 'Зарплата': vacancy_salary,
                         'Компания': company_name, 'Город': city}
            glob_list.append(list_elem)
        data['vacancyes'] = glob_list
        with open('vacancyes.json', 'w') as f:
            json.dump(data, f)
    print(data)


if __name__ == '__main__':
    get_vacancy()
