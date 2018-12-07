import requests
from bs4 import BeautifulSoup
import os

def generate_search_url(search):
    """
    Generates and returns a valid url when the book is searched on gen.lib.rus.ec
    """
    url = "http://gen.lib.rus.ec/search.php"
    parameters = {'req':search, 'lg_topic':'libgen', 'open':'0', 'view':'simple', 'res':'100', 'phrase':'1', 'column':'def'}
    r = requests.get(url, params=parameters)
    return r.url

def find_md5(url):
    """
    Finds the md5 value of the book from the search page.
    """
    r = requests.get(url)
    page = str(BeautifulSoup(r.content, features="html.parser"))
    author = include_author()
    start_author = 0
    if author:
        start_author = page.lower().find(author.lower())
    if start_author == -1:
        start_author = 0
    start_md5 = page.find("md5=", start_author)
    if start_md5 == -1:
        print("\nNo similar book(s) available. Program exiting.")
        exit()
    end_md5 = page.find('"', start_md5 + 1)
    md5 = page[start_md5 + 4: end_md5]
    return md5, author

def include_author():
    """
    Gives a choice whether the name of the author is to be considered for generating download link.
    Returns the name of the author.
    """
    choice = input("\nDo you wish to enter the name of the author? [y/n] (Default: n): ")
    choice = choice.lower()
    if choice == 'n':
        return ""
    elif choice == 'y':
        author = input("Enter the author's name (avoid using abbreviations): ")
        return author
    else:
        print("Invalid choice, not searching for author...")
        return ""

def generate_download_url(md5):
    """
    Generates and returns the url through which the file can be downloaded
    """
    url = "http://library1.org/_ads/" + md5
    r = requests.get(url)
    page = str(BeautifulSoup(r.content, features="html.parser"))
    get = page.find("GET")
    start_url = page.find("http://download.library1.org", 0, get)
    end_url = page.find('"', start_url, get)
    url = page[start_url:end_url]
    return url

def downloader(url, author):
    """
    Downloads the appropriate file through the terminal itself.
    """
    reverse_url = ""
    for i in url:
        reverse_url = i + reverse_url
    end_extension = reverse_url.find('.')
    extension = '.' + url[len(url) - end_extension:]
    if author:
        name = author.capitalize() + ' ' + search.capitalize() + extension
    else:
        name = search.capitalize() + extension
    choice = input("\nDo you want the file to be downloaded in the current directory (that of book.py) [y/n]: ")
    directory = ""
    choice = choice.lower()
    if choice == "n":
        directory = input("Enter the path of the directory (not inclusive of file name) you want to download to (default: current directory): ")
        if directory != "" and not os.path.exists(directory):
            os.makedirs(directory)
    elif choice != "y":
        print("Entered choice invalid. Downloading to the current directory.")
    if directory == "":
        directory = "."
    if directory[len(directory) - 1:] != '/':
        directory = directory + '/'
    print("Downloading your book as " + name)
    r = requests.get(url)
    open(directory + name, 'wb').write(r.content)
    print("\nDone.")

if __name__ == '__main__':
    
    search = (input("Enter the name of the book: "))
    search_url = generate_search_url(search)
    md5, author = find_md5(search_url)
    download_url = generate_download_url(md5)
    print("\nThe url for downloading the book is as follows:\n", download_url)
    choice = input("\nDo you also wish to download the file using this program? [y/n] (Default: y): ")
    if choice == 'n':
        print("Okay. Exiting the program.")
        exit()
    elif choice == 'y':
        downloader(download_url, author)
    else:
        print("Invalid choice, proceeding to download the book...")
        downloader(download_url, author)
