from selenium import webdriver
from user_agent import generate_user_agent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.options import Options
#from bs4 import BeautifulSoup as bs
import os,sys,time

keyword = "my hero academia" #default keyword

def login(browser):
	usernameBox = browser.find_element_by_xpath('//*[@id="username"]')
	passwordBox = browser.find_element_by_xpath('//*[@id="password"]')
	time.sleep(1)
	usernameBox.send_keys('artemis.arrow')
	passwordBox.send_keys('strongpassword')
	loginButton = browser.find_element_by_xpath('//*[@id="btnSubmit"]')
	loginButton.click()
	return browser

def searchResults(browser):
	searchBox = browser.find_element_by_css_selector('#keyword')
	searchBox.send_keys(keyword)
	searchButton = browser.find_element_by_css_selector('#imgSearch')
	time.sleep(3)
	searchButton.click()
	i = 2
	elements = []
	logic = True
	while(True):
		i += 1
		try:
			searchResult = browser.find_element_by_css_selector('#leftside > div > div.barContent > div:nth-child(2) > table > tbody > tr:nth-child({}) > td:nth-child(1) > a'.format(str(i)))
			elements.append(searchResult)
			#runs only once which checks if the anime page is directly opened instead of search results
			if logic:
				if 'pisode' in searchResult.text.strip():
					return browser 
				logic = False	
			print("{}. {}".format((i-2),searchResult.text.strip()))
			if i == 20:
				break
		except:
			break
	#input shouold be valid one : correction needed	for error handling if results are none	
	if i != 3:
		index = int(input("enter the index of the search results :"))
		elements[index-1].click()	
	else:
		print("keyword error.Try again ")
		#instead we can again ask for the keyword and run the program
		browser.close()
		exit()
	return browser

def grabDownloadPages(browser,start,end,totalEpisodes):
	#f = open('download_links.txt','w')
	#comment if u dont wanna display the total episodes
	f = open('rapid_links.txt','w')
	download_links = []
	for i in range(start,end+1):
		episode = browser.find_element_by_css_selector('#leftside > div:nth-child(4) > div.barContent.episodeList > div:nth-child(2) > table > tbody > tr:nth-child({}) > td:nth-child(1) > a'.format(str(totalEpisodes+3-i)))
		tempBrowserLink = browser.current_url
		time.sleep(2)
		episode.click()
		rapidvideoButton = browser.find_element_by_css_selector('#formVerify1 > div:nth-child(3) > p:nth-child(1) > a')
		time.sleep(2)
		rapidvideoButton.click()
		#the following line can be used to raise timeout exception if internet's too slow
		#WebDriverWait(browser,30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#divDownload > a')))
		downloadButton = browser.find_element_by_css_selector('#divDownload > a')
		f.write(downloadButton.get_attribute('href')+'\n')
		time.sleep(2)
		browser.get(tempBrowserLink)
	f.close()
	browser.close()
	grabDownloadLinks(start)

def getTotalEpisodes(string):
	number = (int(string[0])*100)+(int(str(string[1]))*10)+int(str(string[2]))
	return number 	

def grabDownloadLinks(start):
	f = open('download_links.txt','w')
	g = open('rapid_links.txt','r')
	url = (g.readline())[:-1]
	while url != '':
		browser = webdriver.Chrome('/usr/local/bin/chromedriver')
		browser.get(url)
		rapidDownloadButton = browser.find_element_by_id('button-download')
		downloadLink = rapidDownloadButton.get_attribute('href')
		f.write(downloadLink+'\n')
		# download_links.append(downloadLink)   u can create a list download_links and use them in the code
		browser.close()
		url = (g.readline())[:-1]
	f.close()
	g.close()	


# def downloadVideos(links,start):
# 	index = start
# 	# correction needed : check if directory exists and if we can write data in that location
# 	directory = input("Enter the directory in which u wish to download :")
# 	if directory != "" and not os.path.exists(directory):
#             os.makedirs(directory)
# 	if directory[-1] != '/':
# 		directory += '/'
# 	for link in links:
# 		r = requests.get(link,stream = True)
# 		name = keyword+'-'+str(index)+'.mp4'
# 		f = open('name','wb')
# 		# here one can show the status of the download : correction
# 		print("Downloading episode {} ...".format(index))
# 		count = 0
# 		for chunk in r.iter_content(chunk_size = 1024):
# 			if chunk:
# 				f.write(chunk)
# 			count += 1
# 			downloadProgress(count,index)
# 		print("")			
# 		f.close()	
# 		index += 1		

# def downloadProgress(num,episode):
# 	num = num/1024 #in mb cuz num is in kb
# 	sys.stdout.write("episode %s : downloaded ... [ %s ]MB\r"%s(episode,num))
# 	sys.stdout.flush()

if __name__ == '__main__':
	#to speedup the program try reducing time.sleep duration but remember doing so may overload the website
	loginPageUrl = 'https://kissanime.ru/Login/'
	#download chrome driver and keep it in the same directory as this program
	#change the directory of chrome driver if needed : change at line 138 and also 92
	browser = webdriver.Chrome('/usr/local/bin/chromedriver')
	browser.get(loginPageUrl)
	WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, 'username')))
	browser = login(browser)
	keyword = input("enter the keyword to search : ")
	browser = searchResults(browser)
	#total number of episodes can be computed and printed here instead
	# here assuming the largest episode is 3 digits or less only :correction needed
	totalEpisodes = getTotalEpisodes((browser.find_element_by_css_selector('#leftside > div:nth-child(4) > div.barContent.episodeList > div:nth-child(2) > table > tbody > tr:nth-child(3) > td:nth-child(1) > a').text.strip()[-3:]))
	print("total number of episodes : {}".format(totalEpisodes))
	inp = input("Enter range of episodes u wish to download (in the format ---> start:end): ")
	start = int(inp.split(':')[0])
	end = int(inp.split(':')[1])
	browser = grabDownloadPages(browser,start,end,totalEpisodes) #also stores links in a file called download_links.txt in the same directory as this program
	print(' DONE !!! Thanks for using ... ')


	
