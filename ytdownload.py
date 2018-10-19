from __future__ import unicode_literals
import youtube_dl 
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config
import os


class vals(object):
	q = ''
	max_results = 0




DEVELOPER_KEY = config.KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def init():
	os.system('clear')
	print('Download a song from Youtube!\n')
	print('\nEnter a search term: ')
	search = input()
	maxres = 5
	
	args = vals()
	args.q= search
	args.max_results = maxres
	try:
		youtube_search(args)
	except HttpError as e:
		print('A HTTP error %d has occured:\n%s' % (e.resp.status,e.content))

    


def youtube_search(options):
	youtube = build(YOUTUBE_API_SERVICE_NAME,
	YOUTUBE_API_VERSION,
	developerKey=DEVELOPER_KEY)

	search_response = youtube.search().list(
		q=options.q,
		part='id,snippet',
		maxResults=options.max_results
	).execute()

	videos = []
	videoID = []
	i=0;
	for search_result in search_response.get('items', []):
		i = i+1
		if search_result['id']['kind'] == 'youtube#video':
			videos.append('%s.%s (%s)' % (i,search_result['snippet']['title'],
									   search_result['id']['videoId']))
			videoID.append('%s' % (search_result['id']['videoId']))



	print('\nVideos: \n','\n'.join(videos), '\n')
	downloadOption(videoID)


def downloadOption(vid):

	print('\n\nWhich video\'s audio do you want to download? (1-5): ')

	choice = input()
	choice = (int)(choice)
	choice-=1
	vidId = vid[choice]
	downloadAudio(vidId)
	
def downloadAudio(vidId):
	url = 'https://www.youtube.com/watch?v='+vidId
	ydl_opts = {
	'format': 'bestaudio/best',
	'postprocessors': [{
	    'key': 'FFmpegExtractAudio',
	    'preferredcodec': 'mp3',
	    'preferredquality': '320',
	}],}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])
    

   
    


	    
if __name__ == '__main__':
	init()




