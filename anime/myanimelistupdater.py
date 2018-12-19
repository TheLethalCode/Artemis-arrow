from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
#	For creation of the Headless Webdriver
def setUp():
    opts = Options()
    opts.set_headless()
    assert opts.headless
    driver = webdriver.Firefox(options=opts)
    return driver

#	This function can be called to log in the user
def loginMAL(driver, Username, Password):
    driver.get("https://myanimelist.net/login.php?from=%2F")
    assert "MyAnimeList.net" in driver.title

    #	This is to deal with the privacy policy update popup
    driver.find_element_by_xpath("//div[@class='modal-container']//button").click()

    #	Account for Wait Time on slow connection
    try:
        ele = WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.ID, "loginUserName")))
    except:
        print("Please check your Internet Connection")
        closeDown(driver)

    user_name = driver.find_element_by_id("loginUserName")
    user_name.send_keys(Username)
    password = driver.find_element_by_id("login-password")
    password.send_keys(Password)
    password.send_keys(Keys.RETURN)

#	This Function can be called to add the anime to the user's anime list
#	Before adding the anime be sure to login first
def addAnime(driver, Anime_name):
    driver.get("https://myanimelist.net/addtolist.php?hidenav=1")
    assert "MyAnimeList" in driver.title

    #	Account for wait time in slow connections
    try:
        ele = WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.ID, "maSearchText")))
    except:
        print("Please check your Internet Connection")
        closeDown(driver)
    #	This is filling the search box
    inputBox = driver.find_element_by_id("maSearchText")
    inputBox.send_keys(Anime_name)
    inputBox.send_keys(Keys.RETURN)

    #	Here I was trying search the search results but could not get it to work
    #	As the searching usually takes a few seconds
    time.sleep(3)

    try:
        addButton = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/table/tbody/tr/td[4]/a")
        addButton.click()
    except:
        print("The Anime is not on MyAnimeList or Some fatal error has occurred!")
        closeDown(driver)
    #	This is for the option to appear, this function will give a time out error after 60 seconds
    try:
    	ele = WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/div[2]/div/table/tbody/tr[1]/td[2]/select")))
    except:
    	print("Please check your Internet Connection")
        closeDown(driver)
    
    #	Filling the status drop down menu
    dropDown = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div/table/tbody/tr[1]/td[2]/select")
    Select(dropDown).select_by_value('6')  # Selecting Plan to Watch option

    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div/table/tbody/tr[6]/td[2]/div/table/tbody/tr/td/input[1]").click()

    #	Should I print or pop out some message?
    print("The Anime was added successfully")


def closeDown(driver):
    driver.close()

