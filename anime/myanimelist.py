from bs4 import BeautifulSoup
import requests
import json


json_file=open('anime_scrape.json','w')

#Function to get url and return the data to scrape from it
def make_soup(url):
	source=requests.get(url)
	soupdata=BeautifulSoup(source.content,'lxml')
	return soupdata

'''
Function to store the major information about a anime
and storing the data in anime_scrape.json file
'''

def info_anime(soup):

	#Extracting the name of the anime

	anime=soup.find(name="span",attrs={"itemprop":"name"})
	name=anime.text
	print ("Anime : "+name)
	json.dump(name,json_file)



	#Extracting the rating 

	rating=soup.find(name="div",attrs={"class":"fl-l score"})
	print ("Rating : "+(rating.text.strip()))
	json.dump(rating.text.strip(),json_file)


	#extracting the description

	des=soup.find(name="span",attrs={"itemprop":"description"})
	description=des.text
	print ("Description : "+description)
	json.dump(description,json_file)

	#Extracting the Rank

	rank=soup.find(name="span",attrs={"class":"numbers ranked"})
	print (rank.text)

	#Extracting number of episodes

	ep=soup.find(name="div",attrs={"class":"spaceit"})
	print (ep.text)


if __name__ == '__main__':
	'''
	Iterating the loop from 1 to 30000 to store data from myanimelist
	where the url is  https://myanimelist.net/anime/(some number)/
	'''
	for index in range(1,30000):
		try:
			#Handling the exception when page is not found
			r=requests.get("https://myanimelist.net/anime/"+str(index)+"/")		
			r.raise_for_status()
		except requests.exceptions.HTTPError as err:
			continue
		soup=make_soup("https://myanimelist.net/anime/"+str(index)+"/")
		info_anime(soup)

