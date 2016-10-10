import requests
from lxml import html
SEARCH_URL = "https://www.youtube.com/results?search_query=closer"
r = requests.get(SEARCH_URL)
print(r.status_code)
tree = html.fromstring(r.content)
expression = '//body[@id="body"]/div[@id="body-container"]/div[@id="page-container"]/div[@id="page"]/div[@id="content"]/div[@class="branded-page-v2-container branded-page-base-bold-titles branded-page-v2-container-flex-width"]/div[@class="branded-page-v2-col-container"]/div[@class="branded-page-v2-col-container-inner"]/div[@class="branded-page-v2-primary-col"]/div[@class="   yt-card  clearfix"]/div[@class="branded-page-v2-body branded-page-v2-primary-column-content"]/div[@id="results"]/ol/*'
s = tree.xpath(expression)
print(s[1])
# tree_n = s[1]
# print(tree_n.text)
# expression_one = '//div[@class="yt-lockup yt-lockup-tile yt-lockup-video clearfix"]'#/div[@class="yt-lockup-dismissable yt-uix-tile"]/div[@class="yt-lockup-content"]/h3[@class="yt-lockup-title"]'
# a = tree_n.xpath(expression_one)
# print(a)
expression_one = '//ol/li'
a = s[1].xpath(expression_one)
print(a[0])
expression_two = '//div/div/div[@class="yt-lockup-content"]/h3[@class="yt-lockup-title "]/a'
b = a[0].xpath(expression_two)
print(b)
print(b[0].attrib['href'])
print(b[0].attrib['title'])
print(b[1].attrib['href'])
print(b[1].attrib['title'])
# expression_three = '//a'
# c = b[0].xpath(expression_three)
# print(c)
"""
upto this we have url and title
"""
# general for thumbnail and video duration
expression_three = '//div/div[@class="yt-lockup-dismissable yt-uix-tile"]/div[@class="yt-lockup-thumbnail contains-addto"]/a/div[@class="yt-thumb video-thumb"]'
c = a[0].xpath(expression_three)
print(c)
# image src
expression_four = '//span["yt-thumb-simple"]/img'
d = c[0].xpath(expression_four)
print(d)
print(d[0].attrib['src'])
# after index 9 images will be started
print(d[9].attrib['src'])
print(d[10].attrib['src'])
print(len(d))
# video duration
expression_five = '//div/div[@class="yt-lockup-dismissable yt-uix-tile"]/div[@class="yt-lockup-thumbnail contains-addto"]/a/span[@class="video-time"]'
e = c[0].xpath(expression_five)
print(e)
print(e[0].text)
# artist name/link
expression_six = '//div/div/div[@class="yt-lockup-content"]/div[@class="yt-lockup-byline"]/a'
f = a[0].xpath(expression_six)
print(f[0].attrib['href'])
print(f[0].text)
print(len(f))
expression_seven = '//div[@class="yt-lockup-meta"]/ul[@class="yt-lockup-meta-info"]/li'
g = a[0].xpath(expression_seven)
print(len(g))
print(g[0].text)
print(g[1].text)
zx = g[0].text
print(zx)
