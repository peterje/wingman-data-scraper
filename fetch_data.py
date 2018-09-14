from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys

choice = sys.argv[1]

if choice == '0':
	url = "https://steamcommunity.com/my/gcpd/730/?tab=matchhistorycompetitive"
	mode = 'comp'
elif choice == '1':
	url = "https://steamcommunity.com/my/gcpd/730/?tab=matchhistorywingman"
	mode = 'wm'
else:
	print("unknown choice: " ,sys.argv[1], ", default to comp")
	url = "https://steamcommunity.com/id/peterjedmonds/gcpd/730/?tab=matchhistorycompetitive"
	mode = 'comp'

def check_element_visible(element_path):
	try:
		elem = driver.find_element_by_xpath(element_path)
		if elem.is_displayed():
			return True
		else:
			return False
	except Exception:
		return False


driver = webdriver.Chrome()
driver.get(url)
input("Press enter once logged in.")

button_path = '//*[@id="load_more_button"]'
more_buttons = check_element_visible(button_path)

# sometimes the page needs to be refreshed
if not more_buttons:
	driver.get(url)
	more_buttons = check_element_visible(button_path)
	

# timeout if there isnt another load more button within 5 seconds
wait = WebDriverWait(driver, 5)
while more_buttons:
		print("looking for button")
		button = driver.find_element_by_xpath(button_path)
		button.click()
		try:
			wait.until(EC.visibility_of_element_located((By.XPATH, button_path)))
		except TimeoutException as e:
			print("loaded all matches")
			more_buttons = False


cont = driver.page_source
f = open('out-' + mode + '.html', 'wb')
f.write(cont.encode('utf8'))
f.close()