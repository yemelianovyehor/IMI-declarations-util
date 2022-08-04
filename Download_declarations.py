from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC	


import shutil
import os
import time


DIR = input("Directory to save files to (homepath if empty) :")
if DIR == "":
	DIR = os.path.expanduser('~')


PROGRESS = 0 #How Much Done
TO_DOWNLOAD = 1*11 #11 per driver. 0 - download all


def wait_to_load(filename, max_seconds = 0):
	i=0;
	while True:
		if (os.path.isfile(f"{DIR}\\{filename}")):
			return True;
		elif (max_seconds!=0 and i>max_seconds):
			return False;
		time.sleep(1)
		i+=1


profile = Options()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", DIR)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
profile.set_preference("pdfjs.disabled", True)

driver = webdriver.Firefox(options = profile)
#Вход на стриницу
driver.get("https://www.postingdeclaration.eu/account/select")
#Ожидание входа
print('Log in, select firm, then press "Enter" in command line to continue')
input()

actions = ActionChains(driver)

wait = WebDriverWait(driver, 20)



#Выбор фирмы
#print("firm select")
#wait.until(EC.element_to_be_clickable((By.XPATH,'//button[1]')))
#actions.click(driver.find_element(By.XPATH,'//button[1]')).perform()

#Вкладка деклараций
print("home page")
wait.until(EC.element_to_be_clickable((By.XPATH,'//eui-menu-item[2]')))
time.sleep(1)#KOSTYL NO MNIE MOZHNO
actions.click(driver.find_element(By.XPATH,'//eui-menu-item[2]')).perform()
print("declarations table")

wait.until(EC.presence_of_element_located((By.XPATH,'//rtpd-declarations-table/div/div/strong')))
time.sleep(2)#skyrim
number_of_declarations = TO_DOWNLOAD #int(driver.find_elements(By.XPATH,'//strong')[0].text.split(' ')[0])
print(f"declarations to download: {number_of_declarations}")

for i in range(PROGRESS+1,number_of_declarations+1):
	wait.until(EC.presence_of_element_located((By.XPATH, f'//table/tbody/tr[{i}]')))
	time.sleep(1) # lA koSTIL, kak skyrim
	wait.until(EC.element_to_be_clickable((By.XPATH, f'//table/tbody/tr[{i}]')))
	row = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]')

	#print(f"{i} table is clickable")

	if (row.find_element(By.XPATH,'descendant::ux-badge').text == 'Submitted'):
		
		print(f'{i} - Submitted')

		file = row.find_element(By.XPATH, 'td[1]').text+'.pdf'
		country = row.find_element(By.XPATH, 'td[2]').text
		driv = '_'.join(row.find_element(By.XPATH, 'td[3]').text.split(' '))
		
		#time.sleep(1)
		actions.click(row).perform()


		wait.until(EC.element_to_be_clickable((By.XPATH, '//button[4]')))
		print(f"Can download {file}")
		actions.click(driver.find_element(By.XPATH, '//button[4]')).perform();

		if not wait_to_load(file, 20):
			print(f'{driv} - {country} not downloaded')
			input();
		else:
			print(f"{driv} - {country} downloaded")
		os.renames(f'{DIR}\\{file}', f'{DIR}\\{driv}\\{country}.pdf')
		#else:
		driver.back()
	#actions.click(driver.find_element(By.LINK_TEXT,'Delcarations')
	

