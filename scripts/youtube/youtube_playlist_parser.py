import requests
from bs4 import BeautifulSoup

query_url = "https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ/featured"
r = requests.get(query_url)
print(r.status_code)
data = BeautifulSoup(r.text, 'html.parser')
playlist_titles = data.find_all('span',{'class':'branded-page-module-title-text'})
print(playlist_titles)
print(playlist_titles[0].find_all('span')[0].get_text())
li = data.find_all('li',{'class':'feed-item-container yt-section-hover-container browse-list-item-container branded-page-box vve-check '})
print(len(li))
h2 = li[0].find_all('h2',{'class':'branded-page-module-title'})
print(len(h2))
li_internal = li[0].find_all('li', {'class':'channels-content-item yt-shelf-grid-item yt-uix-shelfslider-item '})
print(len(li_internal))
h3_yt_lockup_title = li_internal[0].find_all('h3', {'class':'yt-lockup-title'})[0].find_all('a')[0].get('href')
print(h3_yt_lockup_title)
