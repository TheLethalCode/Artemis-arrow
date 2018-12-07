from bs4 import BeautifulSoup
import requests
import json

url="https://myanimelist.net/topanime.php?type=bypopularity"
source=requests.get(url)


soup=BeautifulSoup(source.content,'lxml')
json_file=open('anime_scrape.json','w')


#Extracting the name of the anime
for anime in soup.find_all('div',class_='di-ib clearfix'):
	name=anime.a.text
	print name
	
	json.dump(name,json_file)
	print(' ')

#Extracting the rating 
rating=soup.find_all('span',class_='text on')
for val in rating:
	print val.text.strip()
	json.dump(val.text.strip(),json_file)


#extracting the description

for des in soup.find_all('div',style='margin-top: 8px;margin-bottom: 10px;'):
	description=des.div.text
	print description
	json.dump(description,json_file)

json_file.close()

