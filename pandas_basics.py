import csv
import pandas as pd
# from datetime import datetime
import requests
import http.cookiejar
import urllib.request
from bs4 import BeautifulSoup as soup

df = pd.DataFrame(columns=['user_id', 'user_url', 'image', 'post_text', 'post_url'])
df.to_csv('facebook.csv', index= False)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

payload = {
    'email': 'user id',
    'pass': 'password',
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
