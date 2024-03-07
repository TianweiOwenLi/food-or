import time, pickle
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

permitted_list = ['produce','dairy','beverages','meat-and-seafood','frozen',
  'baked-goods','3089-deli','3095-prepared-foods','dry-goods-pasta',
  'canned-goods','breakfast-foods']

items_raw = []

driver = webdriver.Firefox()

driver.get('https://www.instacart.com')

login_button = None
while not login_button:
  for button in driver.find_elements_by_tag_name('button'):
    if button.text == 'Log in':
      login_button = button

login_button.click()

time.sleep(1)

driver.find_element_by_name('email').send_keys(input("email: "))
pswd_field = driver.find_element_by_name('password')
pswd_field.send_keys(getpass('password: ') + Keys.TAB + Keys.TAB + Keys.ENTER)

_ = input("Press ENTER when bypassed reCAPTCHA and loaded store")

for cat in permitted_list:
  driver.get("https://www.instacart.com/store/aldi/collections/" + cat)

  time.sleep(2.5)

  # scroll main page to the bottom to load all entries
  store_wrap = driver.find_element_by_id('store-wrapper')
  old_y, new_y = -9, driver.execute_script('return document.body.scrollHeight')
  while old_y != new_y:
    old_y = new_y
    store_wrap.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    new_y = driver.execute_script('return document.body.scrollHeight')

  # find entries with price tag
  for entry in driver.find_elements_by_tag_name('a'):
    et: str = entry.text
    if '$' in et:
      items_raw.append(et)
    
  print(f"Finished scraping {cat}")

with open('items_raw.pkl', 'wb') as f:
  pickle.dump(items_raw, f)

# lines: list[str] = [line.strip() for line in et.split('\n')]
#   name, price = None, None
#   for i, line in enumerate(lines):
#     if (not name) and price and line.isalpha():
#       name = line
#     if '$' in line and '.' in line:
#       price = float(line[1:])
#     if line.startswith('About')
