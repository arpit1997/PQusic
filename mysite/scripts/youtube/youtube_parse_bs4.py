import requests
from bs4 import BeautifulSoup

query = "hello"
r = requests.get("http://youtube.com/results?search_query=hello")
print(r.status_code)
html_doc = r.text

page = BeautifulSoup(html_doc, 'html.parser')
h3_tags_class = page.find_all('h3', {'class':'yt-lockup-title'})

"""
link and title
"""
yt_links_duration = []
yt_links_href = []
yt_links_title = []
for h3_tag in h3_tags_class:
	yt_links_href.append(h3_tag.find_all('a')[0].get('href'))
	yt_links_title.append(h3_tag.find_all('a')[0].get('title'))

"""
views and age
"""
yt_links_views = []
yt_links_age = []
meta_data = page.find_all('ul',{'class':'yt-lockup-meta-info'})
for data in meta_data:
	yt_links_age.append(data.find_all('li')[0].get_text())
	yt_links_views.append(data.find_all('li')[1].get_text())

"""
thumbnail
"""
yt_links_thumbs = []
yt_links_duration = []
thumb_nail = page.find_all('div', {'class':'yt-thumb video-thumb'})
for thumbs in thumb_nail:
	yt_links_thumbs.append(thumbs.find_all('span',{'class':'yt-thumb-simple'})[0].find_all('img')[0].get('src'))

print(yt_links_duration)

yt_links_duration.append(page.findAll('span':'video-time'))