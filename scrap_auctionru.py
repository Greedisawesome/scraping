import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool


def get_html(url):
  r = requests.get(url)
  return r.text

def get_all_categories(url):
    all_categories = []
    max_categories = []
    add= 'https://auction.ru'
    soup = BeautifulSoup(url, 'lxml')
    categories_links = soup.find_all('li', class_='side-categories__item')
    for each in categories_links:
      category_url = each.find ('a', class_='side-categories__link').get('href')
      all_categories.append(add + category_url)
      for element in all_categories:
            soup = BeautifulSoup(requests.get(element).text, 'lxml')
            expanded_categories_links = soup.find_all('li', class_='side-categories__item')
            for ecl in expanded_categories_links:
                try:
                    ecl_url = ecl.find('a', class_='side-categories__link').get('href')
                    max_categories.append(add + ecl_url)
                except:
                    max_categories.append('0')
    while '0' in max_categories: max_categories.remove('0')
    return max_categories

def get_total_pages(url):
      #for each in url:
          soup = BeautifulSoup(url, 'html.parser')
          pages = soup.find('ul', class_="listing__pager").find_all('li', class_='listing__pager__page')[-2].find('a').get('href')
          total_pages = pages.split('=')[1]
          all_pages = []
          #base_url = 'https://auction.ru/listing/offer/'
          #category_part = ['gazety_zhurnaly-123562','antikvarnye_religioznye_knigi-100412','voennoe_delo_voennaja_istorija-126685368818347','detskie_knigi_i_zhurnaly-126685386434057','estestvoznanie_medicina-126685409640999','iskusstvo-126685426360672', 'istorija_filosofija_religija-126685437464168', 'knigi_izdatelstva_academia-126685454152047','literaturovedenie_knigovedenie-126685467879798','originaly_avtografov_dokumentov_rukopisej-126685479591188','promyshlennost_i_tekhnika-126685491314117','khudozhestvennaja_literatura_proza-126685515111820','drugoe_v_bukinistike-100340'    ]
          b = int(total_pages)
          #for x in max_categories:
          for i in range(1, b):
              url_gen = url + '?pg=' + str(i)
              all_pages.append(url)
              all_pages.append(url_gen)
          return all_pages


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    listings = soup.find('div', class_='listing').find_all('div', class_='public_offer_snippet_container')
    links = []
    for  listing in listings:
        a = 'https://auction.ru/' + listing.find('a', class_='offers__item__title').get('href')
        links.append(a)
    return links

def get_page_data(html):
    soup = BeautifulSoup (html, 'lxml')
    try:
        name = soup.find('h1', class_='title').text.strip().replace('\n', '').replace('\r', '').replace('\xa0','')
    except:
        name = ''
    try:
        current_price = soup.find('span', itemprop ='price').text.strip().replace('\n', '').replace('\r', '').replace('\xa0','')
    except:
        current_price = ''
    try:
        reserve_price = soup.find('div', class_= 'offer__price__rur').text.strip().replace('\n', '').replace('\r', '').replace('\xa0','')
    except:
        reserve_price = ''
    try:
        description = soup.find('div', id="description_tab").text.strip().replace('\n', '').replace('\r', '').replace('\xa0','')
    except:
        description = ''
    try:
        original_listing = soup.find('link', rel='canonical').get('href')
    except:
        original_listing = ''
    try:
        seller = soup.find('a', class_='login').get('title').strip()
    except:
        seller = ''
    try:
        images = soup.find('link', rel="image_src").get('href')
    except:
        images =''
    data = {'name':name,
          'current_price':current_price,
          'reserve_price':reserve_price,
          'description':description,
          'original_listing':original_listing,
          'seller':seller,
          'images':images}
    return data



def write_csv(data):
  with open('auctionru.csv', 'a', encoding='utf-8') as f:
      writer = csv.writer(f)
      writer.writerow( (data['name'], data['current_price'],data['reserve_price'], data['description'], data['original_listing'], data['seller'], data['images']) )
      print (data['name'], 'parsed')

def make_all(url):
  html = get_html(url)
  data = get_page_data(html)
  write_csv(data)

def main():
  url = 'https://auction.ru/listing/offer/knigi_bukinistika-108682'
  tbs = get_all_categories(get_html(url))
  for x in tbs:
    full_pages = get_total_pages(get_html(x))
    all_links = get_all_links(get_html(x))
    with Pool (50) as p:
        p.map(make_all,all_links)

if __name__ == '__main__':
    main()
