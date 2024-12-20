import requests
import sqlite3
from bs4 import BeautifulSoup


# install git
# create repository in github

# go to git bash
# git config --global user.name "Ramesh Pradhan"
# git config --global user.email "pyrameshpradhan@gmail.com"

# git init
# git status => if you want to check what are the status of files
# git diff => if you want to check what are the changes
# git add .
# git commit -m "Your message"
# copy paste git code from github


############ after code change ############
# 1. git add .
# 2. git commit -m "Your message"
# 3. git push origin


NO_OF_PAGES = 50

page = 1
URL = f"https://books.toscrape.com/catalogue/page-{page}.html"

def create_database():
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            currency TEXT,
            price REAL
        )
    """
    )
    conn.commit()
    conn.close()


def insert_book(title, currency, price):
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO books (title, currency,price) VALUES (?, ?, ?)
    """,
        (title, currency, price),
    )
    conn.commit()
    conn.close()


def scrape_book(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page, status code: {response.status_code}")
        return

    # Set encoding explicitly to handle special characters
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text
        currency = price_text[0]
        price = price_text[1:]

        insert_book(title, currency, price)


create_database()

while page <= NO_OF_PAGES:
    scrape_book(URL)
    page = page + 1
    URL = f"https://books.toscrape.com/catalogue/page-{page}.html"
