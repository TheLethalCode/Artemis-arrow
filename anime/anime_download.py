import os
from bs4 import BeautifulSoup                               
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

usernameStr="vjs22334"
passwordStr="wildmutt"

# a function to load chromedriver onto path
def SetupSelenium():

    options = Options()
    options.set_headless(True)
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['pageLoadStrategy'] = "eager"
    geckodriver = "/home/jeyasurya/Documents/bots/" # change this according to the location of your chromedriver
    os.environ["webdriver.firefox.driver"] = geckodriver
    # capa = DesiredCapabilities.CHROME
    # capa["pageLoadStrategy"] = "none"
    browser = webdriver.Firefox(geckodriver,options = options)
    return browser

# searches the string in kissanime and returns results
def SearchAnime(searchstring):
    browser = SetupSelenium()
    browser.get("https://kissanime.ru/")
    wait = WebDriverWait(browser, 30)
	# Save the window opener (current window, do not mistaken with tab... not the same)
    main_window = browser.current_window_handle
    # wait until the page loads and locate the search bar
    wait.until(EC.presence_of_element_located((By.ID,"keyword")))
    wait.until(EC.visibility_of_element_located((By.ID,"keyword")))
    searchInput = browser.find_element_by_id("keyword")
    searchInput.send_keys(searchstring)
    searchButton = browser.find_element_by_id("imgSearch")
    searchButton.click()

	# Put focus on current window which will, in fact, put focus on the current visible tab
    browser.switch_to_window(main_window)
    # browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + Keys.TAB)
    while browser.current_url!="https://kissanime.ru/Search/Anime":
        browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

    soup = BeautifulSoup(browser.page_source, 'html.parser')
	
    if len(soup.find_all('table')) == 0:
        return None
    table = soup.find_all('table')[0]
	#print(table)
    links = table.find_all('a')
    print(links)
    Anime_list = []
    for link in links:
        Anime = {
        "url": link['href'],
        "name": link.getText().strip()
        }
        Anime_list.append(Anime)
    browser.quit()
    return Anime_list

def login(browser):
    main_window = browser.current_window_handle
    browser.get("https://kissanime.ru/login")
    wait = WebDriverWait(browser, 30)
    wait.until(EC.presence_of_element_located((By.ID,"username")))
    wait.until(EC.visibility_of_element_located((By.ID,"username")))
    usernameInput = browser.find_element_by_id("username")
    usernameInput.send_keys(usernameStr)
    passwordInput = browser.find_element_by_id("password")
    passwordInput.send_keys(passwordStr)
    loginButton = browser.find_element_by_id("btnSubmit")
    loginButton.click()
    browser.switch_to_window(main_window)
    

def StopPageLoad(driver):
    driver.execute_script("window.stop();")
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def getDownloadlinks(link):
    browser = SetupSelenium()
    wait = WebDriverWait(browser, 30)
    login(browser)
    print("link:"+link)
    browser.implicitly_wait(10)
    browser.get("https://kissanime.ru"+link)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    if len(soup.find_all('table')) == 0:
        return None
    table = soup.find_all('table')[0]
    links = table.find_all('a')
    print(links)
    episode_list = []
    for link in links:
        episode = {
        "url": link['href'],
        "name": link.getText().strip()
        }
        episode_list.append(episode)
    print(episode_list)
    for ep in episode_list:
        print("fetching : "+"https://kissanime.ru"+ep["url"])
        browser.get("https://kissanime.ru"+ep["url"])
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".specialButton")))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".specialButton")))
        # browser.set_page_load_timeout(10)
        try:
            browser.find_element_by_css_selector(".specialButton").click()
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#divDownload a")))
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div#divDownload a")))
            ep["url"] = browser.find_element_by_css_selector("div#divDownload a").get_attribute('href')
            print(ep)
        except TimeoutException as e
    browser.quit()

if __name__ =="__main__":
    Anime_list = SearchAnime("goblin slayer")
    print(Anime_list)
    getDownloadlinks(Anime_list[0]['url'])
    # getDownloadlinks("/Anime/Goblin-Slayer-Dub")
    # Anime_list2 = SearchAnime("hfgafush")
	# print(Anime_list2)
    

