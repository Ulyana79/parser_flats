
import requests 
from bs4 import BeautifulSoup
import csv

#URL = 'https://www.avito.ru/balashiha/kvartiry/prodam/2-komnatnye-ASgBAQICAUSSA8YQAUDKCBSCWQ?i=1'
URL = 'https://www.avito.ru/balashiha/kvartiry/prodam/2-komnatnye-ASgBAQICAUSSA8YQAUDKCBSCWQ?cd=1'
#HEADERS = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 'accept':'*/*'}
#HEADERS = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36', 'accept':'*/*'}


def get_html(url, page_num=1, params=None):
    '''
    Функция, которая по урлу и номеру страницы возвращает объект html web страницы
    '''
    real_url = f'{url}&p={page_num}'
    print(real_url)
    r = requests.get(real_url, 
        # headers=HEADERS, 
        params=params)
    return r
    

def get_all_flats(url):
    '''
    По url возвращает все ссылки на квартиры со всех страниц
    '''
    max_page_num = 20
    page_part = '&p='
    all_flats = []
    for i in range(1, max_page_num):
        html = get_html(url, page_num)
        all_flats += get_section(html)

    write_csv(all_flats)


def parse_search_page(html):
    '''
    Принимает html и возвращает список ссылок на квартиры в этом html
    '''
    print(html)
    if html.status_code == 200:
        print(html.text)
    else:
        print('Error')
        #return[] 


def write_csv(data_list):
    with open('avito.csv', 'w') as f:
        writer = csv.writer(f)
        for data in data_list:
        	writer.writerow( (data['title'],
                          data['price'],
                          data['address'],
                          data['url_ad']) )


def get_section(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    section_ads = soup.find('div', class_='items-items-38oUm').find_all('div', class_='iva-item-root-G3n7v')
    #print(section_ads, len(section_ads))
    all_flats = []
    for ad in section_ads:
        try:
            title = ad.find('div', class_='iva-item-titleStep-2bjuh').get_text()
        except:
            title = ''

        try:
            url_ad = 'https://www.avito.ru/' + ad.find('div', class_='iva-item-titleStep-2bjuh').find('a').get('href')
        except:
            url_ad = ''

        try:
            price = ad.find('span', class_='price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo').text.replace('\xa0', '')
        except:
            price = ''

        try:
            address = ad.find('span', class_='geo-address-9QndR text-text-1PdBw text-size-s-1PUdo').get_text()
        except:
            address = ''

        try:
            date_p = ad.find('div', class_='date-text-2jSvU text-text-1PdBw text-size-s-1PUdo text-color-noaccent-bzEdI').get_text()
        except:
            date_p = ''

        data = {'title': title,
                 'price': price,
                 'address': address,
                 'date_p': date_p,
                 'url_ad': url_ad}                                    
        all_flats.append(data)

    return all_flats

res_html = get_html(URL)
res_flat_list = get_section(res_html)   
print(res_flat_list)