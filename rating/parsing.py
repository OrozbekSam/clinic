from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://bishkek.adresa-telefony.ru/%D0%B3%D0%B4%D0%B5/%D0%B4%D0%B5%D1%88%D0%B5%D0%B2%D1%8B%D0%B5%20%D0%B0%D0%BF%D1%82%D0%B5%D0%BA%D0%B8/%D0%B2-%D0%91%D0%B8%D1%88%D0%BA%D0%B5%D0%BA%D0%B5'
def get_html(url):
    response = requests.get(url)
    return response.text


list1 = []


def get_info(html):
    soup = BeautifulSoup(html, 'lxml')
    info = soup.find_all("div", class_="feed")
    for i in info:
        span = i.find('span').text
        # print(span)
        a = i.find('a').get('href')
        # print(a)
        all = f"📍 {span} *** 🏥 click here👉 {a}"
        list1.append(all)
    # print(list1)
    return list1


get_info(get_html(BASE_URL))