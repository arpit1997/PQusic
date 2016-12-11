import requests
from bs4 import BeautifulSoup


class YtPlaylist:
	"""
	creates a dictionary for playlist
	key: playlist title
	value: an array containing list of YtVideo objects
	"""
	def __init__(self):
		self.yt_playlist = dict()
		self.yt_playlist_url = "https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ/featured"
		self.page = self.get_page()
		self.playlist_titles = []
		self.fetch_videos()

	def get_page(self):
		# r = requests.get(self.yt_playlist_url)
		# print(r.status_code)
		f = open('/home/arpit/Desktop/youtube.html', 'r')
		c = f.read()
		page = BeautifulSoup(c, 'html.parser')
		return page

	def fetch_videos(self):
		playlist_titles_span_elements = self.page.find_all('span', {'class': 'branded-page-module-title-text'})
		for span_element in playlist_titles_span_elements:
			self.playlist_titles.append(span_element.find_all('span')[0].get_text())

		playlist_list = []
		playlist_data_li_elements = self.page.find_all('li', {
			'class': 'feed-item-container yt-section-hover-container browse-list-item-container branded-page-box vve-check '})
		for playlist_li_element in playlist_data_li_elements:
			li_elements = playlist_li_element.find_all('li', {
				'class': 'channels-content-item yt-shelf-grid-item yt-uix-shelfslider-item '})
			video_list = []
			for li_element in li_elements:
				h3_yt_lockup_title = li_element.find_all('h3', {'class': 'yt-lockup-title'})
				video_object = YtVideo()
				video_object.yt_href = h3_yt_lockup_title[0].find_all('a')[0].get('href')
				video_object.yt_id = video_object.yt_href[9:]
				video_object.yt_title = h3_yt_lockup_title[0].find_all('a')[0].get('title')
				video_object.yt_thumbnail = "http://img.youtube.com/vi/%s/default.jpg" % video_object.yt_href[9:]
				video_object.yt_duration = li_element.find_all('span', {'class': 'video-time'})[0].find_all('span')[
					0].get_text()
				video_object.yt_views = li_element.find_all('ul', {'class': 'yt-lockup-meta-info'})[0].find_all('li')[
					0].get_text()
				video_object.yt_artist = li_element.find_all('div', {'class': 'yt-lockup-byline'})[0].find_all('a')[
					0].get_text()
				video_list.append(video_object)
			playlist_list.append(video_list[:4])
		self.yt_playlist = dict(zip(self.playlist_titles, playlist_list))
		"""
		just for debugging
		"""
		# x = self.yt_playlist['R&B']
		# print(x[0].yt_title)
		# print(x[0].yt_href)
		# print(x[0].yt_thumbnail)


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


# if __name__ == "__main__":
# 	x = YtPlaylist()
# 	print(x.playlist_titles)
