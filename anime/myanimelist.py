from bs4 import BeautifulSoup
import requests
import json
import os

#Function to get url and return the data to scrape from it

ANIME_URL = "https://myanimelist.net/anime/"
JSON_PATH = os.path.join(os.path.dirname(__file__),"anime.json")

def make_soup(source):
	soupdata=BeautifulSoup(source.content,'lxml')
	return soupdata

def info_anime(soup):

	'''
	Returns the information about an anime from its soup
	'''
	anime_list = {}

	# Extracting the name of the anime
	anime=soup.find(name="span",attrs={"itemprop":"name"})
	name=anime.text
	anime_list["name"]=name
	
	# Extracting the rating 
	rating=soup.find(name="div",attrs={"class":"fl-l score"})
	anime_list["rating"]=float(rating.text.strip())

	# Extracting the description
	des=soup.find(name="span",attrs={"itemprop":"description"})
	description=des.text
	anime_list["description"]=description

	# Extracting the Rank
	rank=soup.find(name="span",attrs={"class":"numbers ranked"})
	num = rank.text.find("#")+1
	anime_list["rank"]=int(rank.text[num:])

	# Extracting number of episodes
	ep=soup.find(name="div",attrs={"class":"spaceit"})
	num=ep.text.find(" ")+2
	anime_list["episodes"]=int(ep.text[num:-3])

	return anime_list

def gen_list(start,end):

	"""
	Function that generates a list of anime and its detail from start to end
	"""

	anime_ind = {}
	for index in range(start,end):
		print("Index",index)
		try:
			# Handling the exception when page is not found
			
			r=requests.get(ANIME_URL+str(index)+"/")		
			r.raise_for_status()
			soup = make_soup(r)
			anime_ind[index]=info_anime(soup)

		except requests.exceptions.HTTPError:
			continue

	return anime_ind	

if __name__ == '__main__':
	
	with open(JSON_PATH,'w') as json_file:
		json.dump(gen_list(1,20),json_file)
		json_file.close()
	

