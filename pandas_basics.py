import csv
import pandas as pd
# from datetime import datetime
import requests
import http.cookiejar
import urllib.request
from bs4 import BeautifulSoup as soup

df = pd.DataFrame(columns=['user_id', 'user_url', 'image', 'post_text', 'post_url'])
df.to_csv('facebook.csv', index= False)
# timenow = str(datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3])

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

payload = {
    'email': 'angel.raj.01992@gmail.com',
    'pass': '13/06/91',
    'login': 'Log In'
}

authentication_url = 'https://mbasic.facebook.com/login/'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

data = urllib.parse.urlencode(payload).encode('utf-8')
req = urllib.request.Request(authentication_url, data, headers)

resp = urllib.request.urlopen(req)
content = resp.read()
#print(content)

page = 0
for page in range (1, 6):
    try:
        if page>1:
            debug = ''
        url = 'https://mbasic.facebook.com/emobiles.jsr/?refid=46&__xts__%5B0%5D=12.%7B%22unit_id_click_type%22%3A%22graph_search_results_item_tapped%22%2C%22click_type%22%3A%22result%22%2C%22module_id%22%3A1%2C%22result_id%22%3A138038606354844%2C%22session_id%22%3A%22e33204d8139e5813ca1ba36f80999aeb%22%2C%22module_role%22%3A%22ENTITY_PAGES%22%2C%22unit_id%22%3A%22browse_rl%3Acbd219d7-816d-4ec8-b6a9-9be51dc656af%22%2C%22browse_result_type%22%3A%22browse_type_page%22%2C%22unit_id_result_id%22%3A138038606354844%2C%22module_result_position%22%3A0%7D'
        data = requests.get(url, cookies=cj)
        page_soup = soup(data.content, 'html.parser')
  #      print(page_soup.prettify())

        table = page_soup.find_all('div')  #soup.find_all('h3')[1].find('span').find('a').attrs['href']

  #      print(len(table))
        #print(bs4.BeautifulSoup.prettify(table[0]))
        user_id = 'id'  # row.find('strong').text
        user_url = 'url'  # row.find('strong').a['href']

        for row in table:
           try:
               image = page_soup.find_all('div', {'class': "fk fl"})[row].contents[row].contents[row].attrs['src']
           except Exception:
               image = "No"
               pass
           print("image  :  " +image)
           try:
               post_text = page_soup.find_all('div', {'class':'fh'})[row].contents[row].contents[row].text
           except Exception:
               post_text = 'No'
               pass
           print("post_text  :  " + post_text)
           try:
               post_url = page_soup.find_all('h3', {'class':'fe y ff fg'})[row].contents[row].contents[row].attrs['href']
           except Exception:
               post_url = 'No'
               pass
           print("post_url  :  " + post_url)
           print("Row completed  :  " + str(row))

           df = df.append(
           {'user_id': user_id, 'user_url': user_url, 'image' : image, 'post_text' : post_text, 'post_url' : post_url}, ignore_index=True)

           df.to_csv('facebook.csv', index = False)
           print("Done")


    except Exception :
        print('Page level ERROR  no.   :  ' +str(page))
        pass




"""
###################
z=0
#for i in soup.find_all('a'):
for i in table:
    #if i.text.lower() == 'see more friends': break
    #if z>5 and i.text.lower() == 'add friend':
    print(i.text)
    z = z+1
   # pass



################

import pandas as pd

df = pd.DataFrame([[0, 1], [2, 3]])

df.append([4, 5])
print(df)

############################

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime


def main(sellername):
    dfObj = pd.DataFrame(
        columns=['ebay_main_url', 'ebay_upc', 'ebay_seller_url', 'ebay_product_url', 'ebay_item_number', 'ebay_title',
                 'ebay_product_condition', 'ebay_price', 'ebay_seller', 'ebay_mpn', 'ebay_brand'])
    timenow = str(datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3])
    _pgn = 0
    for i in range(0, 800, 50):
        _pgn = _pgn + 1
        print("Page Number : "+str(_pgn))
        ebay_main_url = "https://www.ebay.com/sch/m.html?_nkw=&_armrs=1&_from=&_ssn="+sellername+"&_pgn=" + str(
            _pgn) + "&_skc=" + str(i) + "&rt=nc"
        result = requests.get(ebay_main_url)
        ebay_page = result.content
        soup = BeautifulSoup(ebay_page, 'html.parser')

        # Container with all featured items
        items = soup.find_all('h3', 'lvtitle')
        if items.__len__() == 0:
            print("All pages done!!")
            break

        for index, item in enumerate(items):
            try:
                product_url = item.find('a').attrs['href']
                product_result = requests.get(product_url)
                product_ebay_page = product_result.content
                product_soup = BeautifulSoup(product_ebay_page, 'html.parser')

                ebay_title = item.text.strip()
                ebay_url = product_url
                try:
                    ebay_upc = product_soup.find('h2', {'itemprop': 'gtin13'}).text.strip()
                except Exception:
                    table_item = product_soup.findAll('div', {'class', 'prodDetailSec'})
                    if len(table_item) > 0:
                        for row_item in table_item:
                            a = row_item.findAll('td')
                            for i in range(0, len(a)):
                                if row_item.findAll('td')[i].text.strip().upper() == 'UPC':
                                    ebay_upc = (row_item.findAll('td')[i + 1].text.strip())
                    if ebay_upc is None:
                        ebay_upc = 'NA'
                    pass

                try:
                    ebay_seller_url = product_soup.find('div', {'class', 'mbg vi-VR-margBtm3'}).a['href']
                except Exception:
                    ebay_seller_url = 'NA'
                    pass

                try:
                    ebay_item_number = product_soup.find('div', {'id': 'descItemNumber'}).text.strip()
                except Exception:
                    ebay_item_number = 'NA'
                    pass

                try:
                    ebay_product_condition = product_soup.find('div', {'id': 'vi-itm-cond'}).text.strip()
                except Exception:
                    ebay_product_condition = 'NA'
                    pass

                try:
                    ebay_price = product_soup.find('span', {'id': 'prcIsum'}).text.strip()
                except Exception:
                    ebay_price = 'NA'
                    pass

                try:
                    ebay_seller = product_soup.find('span', {'class': 'mbg-nw'}).text.strip()
                except Exception:
                    ebay_seller = 'NA'
                    pass

                try:
                    ebay_mpn = product_soup.find('h2', {'itemprop': 'mpn'}).text.strip()
                except Exception:
                    table_item = product_soup.findAll('div', {'class', 'prodDetailSec'})
                    if len(table_item) > 0:
                        for row_item in table_item:
                            a = row_item.findAll('td')
                            #    print('a.row size  :  ' + str(len(a)))
                            for i in range(0, len(a)):
                                if row_item.findAll('td')[i].text.strip().upper() == 'MPN':
                                    ebay_mpn = (row_item.findAll('td')[i + 1].text.strip())
                    if ebay_mpn is None:
                        ebay_mpn = 'NA'
                    pass

                try:
                    ebay_brand = product_soup.find('h2', {'itemprop': 'brand'}).find('span').text.strip()
                except Exception:
                    table_item = product_soup.findAll('div', {'class', 'prodDetailSec'})
                    if len(table_item) > 0:
                        for row_table in table_item:
                            a = row_table.findAll('td')
                            for i in range(0, len(a)):
                                if row_table.findAll('td')[i].text.strip().upper() == 'BRAND':
                                    ebay_brand = (row_table.findAll('td')[i + 1].text.strip())
                    if ebay_brand is None:
                        ebay_brand = 'NA'
                    pass

                dfObj = dfObj.append(
                    {'ebay_main_url': ebay_main_url, 'ebay_upc': ebay_upc, 'ebay_seller_url': ebay_seller_url,
                     'ebay_product_url': ebay_url, 'ebay_item_number': ebay_item_number,
                     'ebay_title': ebay_title, 'ebay_product_condition': ebay_product_condition, 'ebay_price': ebay_price,
                     'ebay_seller': ebay_seller, 'ebay_mpn': ebay_mpn, 'ebay_brand': ebay_brand}, ignore_index=True)
            except Exception:
                pass

    # dfObj.sort_values("ebay_product_url", inplace=True)
    #
    # # dropping ALL duplicte values
    # dfObj.drop_duplicates(subset="ebay_product_url",
    #                      keep=False, inplace=True)
    dfObj.to_csv(sellername + '_' + timenow + '.csv')
    print("Done")


if __name__ == "__main__":
    sellername = "waverlyhills1"
    main(sellername)
    
"""