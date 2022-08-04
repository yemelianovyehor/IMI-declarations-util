from tkinter import W
from tkinter.ttk import Progressbar
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC	

#import shutil
import os
import time
from datetime import datetime, timedelta

### FUNCTIONS

def wait_file_to_download(filename, max_seconds = 0):
	i=0
	while True:
		if (os.path.isfile(f"{DIR}\\{filename}")):
			return True
		elif (max_seconds!=0 and i>max_seconds):
			return False
		time.sleep(1)
		i+=1

def wait_row_to_load(line):
	wait.until(EC.presence_of_element_located((By.XPATH, f'//table/tbody/tr[{line}]')))
	time.sleep(1) # lA koSTIL, kak skyrim
	wait.until(EC.element_to_be_clickable((By.XPATH, f'//table/tbody/tr[{line}]')))
	# new_log("row found")
	return (driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]'))


def convert_att_max_date_to_input(date_time):
	date_arr = date_time.split("T")[0].split("-")
	return f"{date_arr[2]}/{date_arr[1]}/{date_arr[0]}"

def new_log(message, wait_for_input = False, end_with="\n"):
	print(F"{datetime.now().strftime('%H:%M:%S')} : {message}", end=end_with)
	if wait_for_input:
		input()

def next_page():
	try:
		# new_log("need to open next page")
		time.sleep(1)
		driver.execute_script("window.scroll(0,document.body.scrollHeight);")
		# wait.until(EC.presence_of_element_located(driver.find_element(By.XPATH, "//uxlayouthorizontalright")))
		# new_log("Button is locatesd")
		wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, "//uxlayouthorizontalright")))
		time.sleep(0.5)
		# new_log("button is clickable")
		actions.click(driver.find_element(By.XPATH, "//uxlayouthorizontalright/button")).perform()
		# new_log("is clicked")
	except Exception as e:
		new_log(e)
		new_log("just open next page yourself", True)


def copy_declaration(i):
	try:
		row = wait_row_to_load(i)
		driver.execute_script("arguments[0].scrollIntoView(); window.scroll(0,370);", row)
		# new_log("scrolled to row")
		end_date = datetime.strptime(row.find_element(By.XPATH, "./td[5]").text, "%Y-%m-%d")
	except:
		new_log("Error on finding the row, press enter to try again", True)
		row = wait_row_to_load(i)
		driver.execute_script("arguments[0].scrollIntoView(); window.scroll(0,370);", row)
		end_date = datetime.strptime(row.find_element(By.XPATH, "./td[5]").text, "%Y-%m-%d")

	new_start_date = (end_date + timedelta(days = 1)).strftime("%d/%m/%Y")
	actions.click(row.find_element(By.XPATH, ".//button[1]")).perform()
	# new_log("row-copy clicked")
	time.sleep(0.5)

	try:
		wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, "//div[@class = 'ux-datepicker__input-wrapper']/input")))
		# new_log("copy page loaded")
		date_inputs= driver.find_elements(By.XPATH, "//div[@class = 'ux-datepicker__input-wrapper']/input")
		start_date_input = date_inputs[0]
		end_date_input = date_inputs[1]
		wait.until(EC.element_to_be_clickable(start_date_input))

		# driver.execute_script(f"document.getElementById('{start_date_input.get_attribute('id')}').value = '';")
		actions.click(start_date_input).click(start_date_input).perform()
		start_date_input.send_keys("\ue009"+'a'+"\ue017")
		start_date_input.send_keys(new_start_date)
		# new_log("new start date inputed")

		time.sleep(0.5)
		max_date_time = end_date_input.get_attribute('max')
		new_end_date = convert_att_max_date_to_input(max_date_time)
		# new_log("got new end date")

		# driver.execute_script(f"document.getElementById('{end_date_input.get_attribute('id')}').value = '';")
		actions.click(end_date_input).click(end_date_input).perform()
		end_date_input.send_keys("\ue009"+'a'+"\ue017")
		end_date_input.send_keys(new_end_date)

		# new_log("new end date inputed")
		# actions.click()
	except:
		new_log("Error on dates input", True)

	try:
		submit_button = driver.find_element(By.XPATH, "//rtpd-declaration-create-actions/button[2]")
		driver.execute_script("arguments[0].scrollIntoView();", submit_button)
		actions.click(submit_button).perform()
		# new_log("submit")
		# wait(1)
		confirm_save_button = driver.find_element(By.XPATH, "//uxdynamicmodalfooter//ux-button[2]/button")
		wait.until(EC.element_to_be_clickable(confirm_save_button))
		actions.click(confirm_save_button).perform()
		# new_log("confirm")
	except:
		new_log("Error on submit-save", True)
	new_log("Done")





### Save profile

DIR = input("Directory to save files to (homepath if empty) :")
if DIR == "":
	DIR = os.path.expanduser('~')

profile = Options()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", DIR)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
profile.set_preference("pdfjs.disabled", True)

### init bowser

driver = webdriver.Firefox(options = profile)
#Tab open
driver.get("https://www.postingdeclaration.eu/account/select")
# waiting for user log-in
print('Log in, select firm, set language to english then press "Enter" in command line to continue')
input()

actions = ActionChains(driver)

wait = WebDriverWait(driver, 20)

###LOGED IN



### COPY the SOON TO EXPIRE ###

exp_decl_tab = driver.find_element(By.XPATH, "//div[@class='eui-u-flex']//h2[text()=' Declarations ']")

wait.until(EC.element_to_be_clickable(exp_decl_tab))
time.sleep(1)#KOSTYL NO MNIE MOZHNO

## COPY NUMBER
declarations_to_copy = int(driver.find_element(By.XPATH, "//div[@class='eui-u-flex'][.//h2[text()=' Declarations ']]//eui-badge").text)

## TAB: FILTERED DECLARATIONS
actions.click(exp_decl_tab).perform()

PROGRESS = input("If creashed ealier, how much done already?:")
if PROGRESS == "":
	PROGRESS = 0

pages_done = 0
start_at= PROGRESS % 250
while(PROGRESS>=250):
	declarations_to_copy -=250
	pages_done+=1
	PROGRESS -= 250
while(declarations_to_copy > 250):
	for i in range(start_at+1 ,251):
		pages_to_scroll = pages_done
		while(pages_to_scroll>0):
			next_page()
			pages_to_scroll -=1
		new_log(f"Start row No{pages_done*250+i}", end_with=" - ")
		copy_declaration(i)
	declarations_to_copy -= 250

if(declarations_to_copy>0):
	for i in range(start_at+1,declarations_to_copy+1):
		pages_to_scroll = pages_done
		while(pages_to_scroll>0):
			next_page()
			pages_to_scroll -=1
		new_log(f"Start row No{pages_done*250+i}", end_with=" - ")
		copy_declaration(i)


###

#TODO:
# - copying -DONE
# - modes 
# - options of what to download
