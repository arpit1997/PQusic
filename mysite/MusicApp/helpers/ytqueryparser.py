import requests
from bs4 import BeautifulSoup


class YtQueryParser:
	"""
	parses youtube page with search query
	parses all the attrbutes for a search query results
	"""

	def __init__(self, query):
		self.yt_query_url = "http://youtube.com/results?search_query="+query
		self.yt_links_duration = []
		self.yt_links_href = []
		self.yt_links_title = []
		self.yt_links_views = []
		self.yt_links_age = []
		self.yt_links_thumbs = []
		self.yt_links_duration = []
		self.page = self.get_page()
		self.get_duration()
		self.get_links_title()
		self.get_views_age()
		self.get_thumbnail()


	def get_page(self):
		r = requests.get(self.yt_query_url)
		html_doc = r.text
		page = BeautifulSoup(html_doc, 'html.parser')
		return page

	def get_links_title(self):
		h3_tags_class = self.page.find_all('h3', {'class': 'yt-lockup-title'})
		for h3_tag in h3_tags_class:
			self.yt_links_href.append(h3_tag.find_all('a')[0].get('href'))
			self.yt_links_title.append(h3_tag.find_all('a')[0].get('title'))

	def get_views_age(self):
		meta_data = self.page.find_all('ul', {'class': 'yt-lockup-meta-info'})
		for data in meta_data:
			self.yt_links_age.append(data.find_all('li')[0].get_text())
			self.yt_links_views.append(data.find_all('li')[1].get_text())

	def get_thumbnail(self):
		for i in self.yt_links_href:
			url = "http://img.youtube.com/vi/%s/default.jpg" % i[9:]
			self.yt_links_thumbs.append(url)

	def get_duration(self):
		video_time_list = self.page.find_all('span', {'class': 'video-time'})
		for video_time in video_time_list:
			self.yt_links_duration.append(video_time.get_text())

"""
just for some debugging purposes
"""
# if __name__ == "__main__":
# 	x = YtQueryParser("hello")
# 	print(len(x.yt_links_title))
# 	for i in x.yt_links_thumbs:
# 		print(i)
# 		print("\n")
