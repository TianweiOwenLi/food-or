import requests
from bs4 import BeautifulSoup

url = "https://www.instacart.com/store/aldi/storefront"
response = requests.get(url)

permitted_list = ['produce','dairy','beverages','meat-and-seafood','frozen',
  'baked-goods','3089-deli','3095-prepared-foods','dry-goods-pasta',
  'canned-goods','breakfast-foods']

product_link_list = []

for cat in permitted_list:
  url = "https://www.instacart.com/store/aldi/collections/" + cat


  response = requests.get(url)
  # payload = {"uname": "test", "pass": "test"} 
  # s = requests.session() 
  # response = s.post(url, data=payload) 

  print(url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    for a_elt in soup.find_all('a'):
      href = a_elt.get('href')
      print(f"  {href}")
      if '/store/aldi/products/' in href:
        product_link_list.append(href)
  else:
    print(f"Failed to retrieve the webpage {url}")

print(len(product_link_list))