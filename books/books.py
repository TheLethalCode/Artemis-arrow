import requests
from bs4 import BeautifulSoup
import os

url = "http://gen.lib.rus.ec/search.php"
search = (input("Enter the name of the book: "))
r = requests.get(url, {'req':search})
url = r.url + "&lg_topic=libgen&open=0&view=simple&res=100&phrase=1&column=def"
r = requests.get(url)
page = str(BeautifulSoup(r.content, features="html.parser"))

author = input("Enter the author's name (avoid using abbreviations, enter only that part of the name which is fully known): ")
start_author = 0
if author:
    start_author = page.lower().find(author.lower())
if start_author == -1:
    start_author = 0
start_md5 = page.find("md5=", start_author)
if start_md5 == -1:
    print("No similar book(s) available. Program exiting.")
    exit()
end_md5 = page.find('"', start_md5 + 1)
md5 = page[start_md5 + 4: end_md5]

url = "http://library1.org/_ads/"+md5
r = requests.get(url)
page = str(BeautifulSoup(r.content, features="html.parser"))
get = page.find("GET")
start_url = page.find("http://download.library1.org", 0, get)
end_url = page.find('"', start_url, get)
url = page[start_url:end_url]
reverse_url = ""
for i in url:
    reverse_url = i + reverse_url
end_extension = reverse_url.find('.')
extension = '.' + url[len(url) - end_extension:]
name = author.capitalize() + ' ' + search.capitalize() + extension
choice = input("Do you want the file to be downloaded in the current directory (that of book.py) [y/n]: ")
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
print("Done.")
