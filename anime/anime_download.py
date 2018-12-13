from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

def SetupSelenium():
	chromedriver = "/home/jeyasurya/Downloads/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	browser = webdriver.Chrome(chromedriver)
	return browser


def SearchAnime(searchstring):
	browser = SetupSelenium()
	wait = WebDriverWait(browser, 30)
	browser.get("https://kissanime.ru/")

	# Save the window opener (current window, do not mistaken with tab... not the same)
	main_window = browser.current_window_handle


	wait.until(EC.presence_of_element_located((By.ID,"keyword")))
	wait.until(EC.visibility_of_element_located((By.ID,"keyword")))
	searchInput = browser.find_element_by_id("keyword")
	searchInput.send_keys(searchstring)
	searchButton = browser.find_element_by_id("imgSearch")
	searchButton.click()

	# Put focus on current window which will, in fact, put focus on the current visible tab
	browser.switch_to_window(main_window)
	while browser.current_url!="https://kissanime.ru/Search/Anime":
		browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

	soup = BeautifulSoup(browser.page_source, 'html.parser')
	
	if len(soup.find_all('table')) == 0:
		return None;
	table = soup.find_all('table')[0];
	#print(table)
	links = table.find_all('a')
	print(links)
	
	Anime_list = []
	for link in links:
		Anime = {
		"url": link['href'],
		"name": link.getText()
		}
		Anime_list.append(Anime)
	browser.quit()
	return Anime_list


if __name__ =="__main__":
	Anime_list = SearchAnime("goblin slayer")
	print(Anime_list)
	Anime_list = SearchAnime("hfgafush")
	print(Anime_list)

