import time, pickle
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def scroll_to_end(driver, elt):
  script = 'return document.body.scrollHeight'
  old_y, new_y = -9, driver.execute_script(script)
  while old_y != new_y:
    old_y = new_y
    elt.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    new_y = driver.execute_script(script)


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

driver.find_element_by_name('email').send_keys(input("✉: "))
pswd_field = driver.find_element_by_name('password')
pswd_field.send_keys(getpass('🔑: ') + Keys.TAB + Keys.TAB + Keys.ENTER)

_ = input("Press ENTER after bypassing reCAPTCHA and loading store")

for cat in permitted_list:
  driver.get("https://www.instacart.com/store/aldi/collections/" + cat)

  time.sleep(2.5)

  # scroll main page to the bottom to load all entries
  scroll_to_end(driver, driver.find_element_by_id('store-wrapper'))

  # find entries with price tag
  for entry in driver.find_elements_by_tag_name('a'):
    et: str = entry.text
    if '$' in et:
      items_raw.append(et)
    
  print(f"Finished scraping {cat}")

with open('items_raw.pkl', 'wb') as f:
  pickle.dump(items_raw, f)

