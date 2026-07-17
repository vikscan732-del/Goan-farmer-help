import requests
from bs4 import BeautifulSoup

url = "https://goabagayatdar.com/pricing/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers)

print("Status:", r.status_code)
print("Length:", len(r.text))

soup = BeautifulSoup(r.text, "lxml")

tables = soup.find_all("table")
print("Tables found:", len(tables))

for i, table in enumerate(tables):
    print("Table", i)
    print(table.get_text(" ", strip=True)[:500])
