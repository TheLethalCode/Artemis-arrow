import os
from decouple import config
from bs4 import BeautifulSoup                               
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

usernameStr=config("KISSANIME_USERNAME")
passwordStr=config("KISSANIME_PASSWORD")

# a function to load chromedriver onto path
def SetupSelenium():

    options = Options()
    # to execute without launching browser. comment this if you are debugging
    options.set_headless(True)
    firefox_capabilities = DesiredCapabilities.FIREFOX
    # to load just the dom elements
    firefox_capabilities['pageLoadStrategy'] = "eager"
    geckodriver = "/home/jeyasurya/Documents/bots/" # change this according to the location of your gecko driver
    os.environ["webdriver.firefox.driver"] = geckodriver
    browser = webdriver.Firefox(geckodriver,options = options)
    return browser

# searches the string in kissanime and returns results
# {status:indicates sucess or failure, links:[]}    
def SearchAnime(searchstring):
    browser = SetupSelenium()
    resp = {
        "status" : "",
        "links" : []
    }
    try:
        browser.get("https://kissanime.ru/")
        wait = WebDriverWait(browser, 30)
        # Save the window opener (current window, do not mistaken with tab... not the same)
        main_window = browser.current_window_handle
        # wait until the page loads and locate the search bar and search
        wait.until(EC.presence_of_element_located((By.ID,"keyword")))
        wait.until(EC.visibility_of_element_located((By.ID,"keyword")))
        searchInput = browser.find_element_by_id("keyword")
        searchInput.send_keys(searchstring)
        searchButton = browser.find_element_by_id("imgSearch")
        searchButton.click()

        # Put focus on current window which will, in fact, put focus on the current visible tab
        browser.switch_to_window(main_window)
        # close any ads
        while browser.current_url!="https://kissanime.ru/Search/Anime":
            ActionChains(browser).send_keys(Keys.CONTROL + 'w').perform()

        soup = BeautifulSoup(browser.page_source, 'html.parser')
        
        if len(soup.find_all('table')) == 0:
            return None
        table = soup.find_all('table')[0]
        links = table.find_all('a')
        print(links)
        Anime_list = []
        for link in links:
            if "episode" not in link.getText().strip().lower():
                Anime = {
                "url": link['href'],
                "name": link.getText().strip()
                }
                Anime_list.append(Anime)
        browser.quit()
        if len(Anime_list)!=0:
            resp["status"]="success"
            resp["links"] = Anime_list
            return resp
        else:
            resp["status"]="not found"
            resp["links"] = []
            return resp
    except TimeoutException as e:
        print("search timed out")
        resp["status"] = "timed out"
        return resp
    
# function to login into kissanime
def login(browser):
    try:
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
    except TimeoutException:
        print("login timed out")
        return False
    browser.implicitly_wait(5)
    # Put focus on current window which will put focus on the current visible tab
    browser.switch_to_window(main_window)
    #confirm login was successful
    print(browser.current_url)
    if browser.current_url=="https://kissanime.ru/":
        return True
    else:
        return False

# returns the rapidvideo download links of the given link in a dictionary
# {status:indicates sucess or failure, links:[]}     
def getDownloadlinks(link):
    browser = SetupSelenium()
    resp = {
            "status": "",
            "links": []
        }
    wait = WebDriverWait(browser, 30)
    if login(browser):
        print("link:"+link)
        try:
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

        
            episode_download_list = []
            for ep in episode_list:
                e = {}
                print("fetching : "+"https://kissanime.ru"+ep["url"])
            
                browser.get("https://kissanime.ru"+ep["url"])
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".specialButton")))
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".specialButton")))
                browser.find_element_by_css_selector(".specialButton").click()
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#divDownload a")))
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div#divDownload a")))
                e["url"] = browser.find_element_by_css_selector("div#divDownload a").get_attribute('href')
                e["name"] = ep["name"]
                episode_download_list.append(e)
            browser.quit()
            resp["status"] = "sucess"
            resp["links"] = episode_download_list
            return resp
        except TimeoutException as e:
            browser.quit()
            resp["status"] = "sucess"
            resp["links"] = episode_download_list
            return resp
        except WebDriverException as e:
            browser.quit
            print("wrong url")
            resp["status"] = "wrong url"
            return resp

    else:
        browser.quit()
        resp["status"] = "login failed"
        return resp

if __name__ =="__main__":
    Anime_list = SearchAnime("goblin slayer")
    print(Anime_list)
    download_links = getDownloadlinks(Anime_list['links'][0]['url'])
    # download_links = getDownloadlinks("abcd")
    print(download_links)
    # getDownloadlinks("/Anime/Goblin-Slayer-Dub")
    # Anime_list2 = SearchAnime("hfgafush")
	# print(Anime_list2)
    

