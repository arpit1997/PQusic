import requests
from bs4 import BeautifulSoup


class YtQueryParser:
	"""
	parses youtube page with search query
	parses all the attrbutes for a search query results
	"""

	def __init__(self, query):
		self.yt_query_url = "http://youtube.com/results?search_query=" + query
		print(self.yt_query_url)
		self.yt_links_duration = []
		self.yt_links_href = []
		self.yt_links_title = []
		self.yt_links_views = []
		self.yt_links_age = []
		self.yt_links_thumbs = []
		self.yt_links_artist = []
		self.yt_search_list = []
		self.yt_search_json = []
		self.page = self.get_page()
		try:
			self.get_duration()
			self.get_links_title()
			self.get_views_age()
			# self.get_thumbnail()
			self.get_artist()
			self.create_search_object()
		except IndexError:
			pass
		print(len(self.yt_search_list))
		a = self.create_json()

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
			try:
				self.yt_links_age.append(data.find_all('li')[0].get_text())
				self.yt_links_views.append(data.find_all('li')[1].get_text())
			except IndexError:
				self.yt_links_age.append('0')
				self.yt_links_views.append('0')

	# def get_thumbnail(self):
	# 	thumbs = self.page.find_all('span', {'class': 'yt-thumb-simple'})
	# 	for thumb in thumbs:
	# 		img = thumb.find_all('img')[0].get('src')
	# 		self.yt_links_thumbs.append(img)

	def get_duration(self):
		video_time_list = self.page.find_all('span', {'class': 'video-time'})
		for video_time in video_time_list:
			self.yt_links_duration.append(video_time.get_text())

	def get_artist(self):
		div = self.page.find_all('div', {'class': 'yt-lockup-content'})
		for artist in div:
			a = artist.find_all('a')[0].get_text()
			self.yt_links_artist.append(a)

	def create_search_object(self):
		i = 0
		for x in self.yt_links_title:
			if self.yt_links_age[i] == '0' or self.yt_links_views[i] == '0':
				i += 1
			else:
				video_object = YtVideo()
				video_object.yt_title = self.yt_links_title[i]
				video_object.yt_href = self.yt_links_href[i]
				video_object.yt_duration = self.yt_links_duration[i]
				video_object.yt_artist = self.yt_links_artist[i]
				video_object.yt_views = self.yt_links_views[i]
				video_object.yt_thumbnail = "http://img.youtube.com/vi/%s/default.jpg" % video_object.yt_href[9:]
				video_object.yt_id = self.yt_links_href[i][9:]
				self.yt_search_list.append(video_object)
				i += 1

	def create_json(self):
		for video in self.yt_search_list:
			dictionary = dict()
			dictionary["id"] = video.yt_id
			dictionary["title"] = video.yt_title
			dictionary["href"] = video.yt_href
			dictionary["duration"] = video.yt_duration
			dictionary["artist"] = video.yt_artist
			dictionary["views"] = video.yt_views
			dictionary["thumbnail"] = video.yt_thumbnail
			self.yt_search_json.append(dictionary)
		return 1


class YtVideo:
	"""
	video object containing properties of a video
	"""

	def __init__(self):
		self.yt_title = ""
		self.yt_href = ""
		self.yt_duration = ""
		self.yt_artist = ""
		self.yt_views = ""
		self.yt_thumbnail = ""
		self.yt_id = ""


"""
just for some debugging purposes
"""
# if __name__ == "__main__":
# 	x = YtQueryParser("hello")
# 	print(len(x.yt_links_title))
# 	for i in x.yt_links_thumbs:
# 		print(i)
# 		print("\n")
