from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import requests
from functions import *
import img2pdf 
from PIL import Image
from io import BytesIO

options = Options()
options.set_headless(True)



class KissMangaDownloader():

	#class variables
	SITE_URL = 'https://kissmanga.com/'
	chapter_list = []
	manga_name = ''
	queue = set()
	downloaded = set()
	browser = webdriver.Firefox(options=options)


	def __init__(self):
		self.get_manga()
		#self.download_chapters(chapter_list,manga_name)



	def get_manga(self):
		manga_name = input("Enter the manga name to be searched ")

		#Enter the site
		self.browser.get(self.SITE_URL)
		print("Wait a few seconds while we fetch data....")

		if True:
			element = WebDriverWait(self.browser, 50).until(EC.presence_of_element_located((By.ID, "keyword")))
			element.send_keys(manga_name)
			search_btn = self.browser.find_element_by_id('imgSearch')
			search_btn.click()
			
			print("retreiving search results on kissmanga....")
			#retrieve the manga names
			
			heading = self.browser.find_element_by_css_selector("th")


			if(heading.text!='Chapter Name'):
				manga_list = self.browser.find_elements_by_css_selector('tr td:first-child a')

				while len(manga_list) == 0:
					manga_name = input("The manga was not found please enter another name")
					element.send_keys(manga_name)
					search_btn = self.browser.find_element_by_id('imgSearch')
					search_btn.click()
					manga_list = self.browser.find_elements_by_css_selector('tr td:first-child a')

				for i in range(len(manga_list)):
					print("   "+str(i+1)+"."+manga_list[i].text)
				n = int(input("Enter the manga serial number: "))-1;
				print("You selected "+manga_list[n].text)
				manga_name = manga_list[n].text
				manga_list[n].click()
			else:
				manga_name = self.browser.find_element_by_css_selector('div .bigChar').text

			#make the manga directory

			print("Downloading manga "+manga_name)
			make_directory('downloads/'+manga_name)

			
			chapters = self.browser.find_elements_by_css_selector("tbody tr td:first-child a")
			chapter_name = []

			for i in chapters:
				chapter_name.append(i.text)

			chapter_name = sorted(chapter_name)

			for i in range(len(chapter_name)):
				print("  " + str(i+1)+"."+chapter_name[i])

			a = list(input("give the index ").split())
			x = 0
			y = 0
			if(a[0]) == 'all':
				x = len(chapters)-1
				y = 0
				print("Downloading all chapters.....")
			elif (len(a)==1):
				x = len(chapters)-int(a[0])
				y = x
				print("Dowloading the chapter "+ a[0])
			else:
				x = len(chapters)-int(a[0])
				y = len(chapters)-int(a[1])
				print("Dowloading the chapter from "+a[0] + " to "+a[1])
				




			#select the first chapter
			i =x
			chapters[i].click()
			while i>=y:

				pdf_path ='downloads/'+ manga_name+'/'+'chapter '+str(len(chapters)-i)+'.pdf'

				#select the images
				print("Downloading chapter " + str(len(chapters)-i))
				images = self.browser.find_elements_by_css_selector("#divImage p img")
				imagelist = []
				page = 1
				for image in images:
					print("retrieving page "+ str(page))
					page=page+1
					img_src = image.get_attribute('src')
					res = requests.get(img_src)
					img = Image.open(BytesIO(res.content))
					imagelist.append(img)
				if(len(imagelist)==0):
					print("Oops no chapter found....")
				else:
					temp = imagelist[1:]
					imagelist[0].save(pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=temp)
					if(i!=y):
						next_btn= self.browser.find_element_by_css_selector('.btnNext')
						next_btn.click()
				i-=1

		print("done....")



			







KissMangaDownloader()