from selenium import webdriver
import time
import csv
import random
import array as url

# ---------- LOG INTO LINKEDIN ACCOUNT ----------

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

username = driver.find_element_by_name('session_key')
username.send_keys('trevorsealing384@yahoo.com')

time.sleep(0.5)

password = driver.find_element_by_name('session_password')
password.send_keys('Tripletriple38')

time.sleep(0.5)

log_in_button = driver.find_element_by_class_name('login__form_action_container')
log_in_button.click()


# ---------- NAV TO COMPANY PAGES & SCRAPE ----------

# List of all company URL links
companyLinks = []

# Add all company URLs to companyLinks list, convert to strings
csvFile = open('company-LinkedIn-URLs.csv', encoding = 'utf-8-sig')
readCSV = csv.reader(csvFile, delimiter = ',')
for row in readCSV:
	hold = ''.join(row)
	companyLinks.append(hold)
csvFile.close()

csvHeader = ['Name', 'Website', 'LinkedIn', 'Followers', 'Employees']
outputFile = open('Scraped-Information.csv', 'w')
writer = csv.writer(outputFile)
writer.writerow(csvHeader)

linkIndex = 0;

for index in companyLinks:

	delay = random.randint(11, 15)

	time.sleep(delay)

	driver.get(companyLinks[linkIndex])

	companyLinkedInURL = companyLinks[linkIndex]

	validLinkedInURL = False

	# Get company name, saved in "companyName"
	# Try/Except: if the company name can't be found, we assume the page is invalid
	# Followed by an if/else to move past invalid pages
	# Consider restructuring to check for elements on the invalid page instead
	# of assuming if you can't find company name the page is invalid
	try:
		getCompanyNameElem = driver.find_element_by_xpath('//*[@class= "org-top-card-summary__title t-24 t-black  truncate"]')
		companyName = getCompanyNameElem.get_attribute("title")
		validLinkedInURL = True
	except:
		validLinkedInURL = False
		companyName = "Invalid"

	if validLinkedInURL:

		# Check if company has a Website on LinkedIn page, records website if present
		try:
			getCompanyWebElem = driver.find_element_by_xpath('//*[@data-control-name= "top_card_view_website_custom_cta_btn"]')
			companyWebsite = getCompanyWebElem.get_attribute("href")
		except:
			companyWebsite = "No Website"

		try:
			# Get Company's follower count, strip extra WS & NL
			getFollowerCtElem = driver.find_element_by_xpath('(//*[@class= "org-top-card-summary-info-list__info-item"]) [3]')
			followerCountToStrip = getFollowerCtElem.get_attribute('innerHTML')
			stripWS = followerCountToStrip.replace(" ", "")
			stripFollowerText = stripWS.replace("followers", "")
			companyFollowerCount = stripFollowerText.replace("\n", "")
		except:
			companyFollowerCount = "N/A"

		try:
			# Get Company's Employee Count
			getEmployeeCtElem = driver.find_element_by_xpath('//*[@class= "v-align-middle"]')
			employeeCountToStrip = getEmployeeCtElem.get_attribute('innerHTML')
			strip1 = employeeCountToStrip.replace("See", "")
			strip2 = strip1.replace("all", "")
			strip3 = strip2.replace("employee", "")
			strip4 = strip3.replace("s", "")
			strip5 =  strip4.replace("on LinkedIn", "")
			employeeCount = strip5.replace(" ", "")
		except:
			employeeCount = "N/A"

		# Write company info to CSV file
		storeCompanyInfo = [companyName, companyWebsite, companyLinkedInURL, companyFollowerCount, employeeCount]
		writer.writerow(storeCompanyInfo)

		linkIndex = linkIndex + 1

	else:
		storeCompanyInfo = [companyName, companyLinkedInURL]
		writer.writerow(storeCompanyInfo)

		linkIndex = linkIndex + 1

outputFile.close()
