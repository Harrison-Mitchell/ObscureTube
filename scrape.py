from sys import argv, stderr
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Spin up firefox geckodriver headlessly
print("Spinning up a browser > ", end="", file=stderr, flush=True)
options = FirefoxOptions()
options.add_argument("--headless")
profile = webdriver.FirefoxProfile()
# Use a mobile user agent for more scrape friendly page
profile.set_preference("general.useragent.override", "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36")
driver = webdriver.Firefox(profile, options=options)
print("Searching...", file=stderr, flush=True)
driver.get(f'https://m.youtube.com/results?search_query={argv[1].replace(" ", "+")}')
sleep(0.2)
# Open search settings
driver.find_element_by_css_selector("button[aria-label='Search filters']").click()
sleep(0.2)
# Find "released" dropdown
x = driver.find_elements_by_tag_name('ytm-select')[1].find_element_by_tag_name("select")
sleep(0.2)
# Select "today"
x.send_keys("t")

# Every 2 seconds, scroll to the bottom of the page, get new results
for i in range(25):
	print(f"Page {i+1} of 25...", end="\r", file=stderr, flush=True)
	sleep(2)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Get the DOM and split it by video
search = driver.execute_script("return document.documentElement.outerHTML;")
titles = search.split('</ytm-compact-video-renderer>')
users = []

# For each video
for i in titles:
	# Try pull info, but don't die if error
	try:
		title = i.split("</span>")[1].split(">")[-1]
		length = i.split("</span>")[0].split(">")[-1]
		id = i.split("watch?v=")[1].split('"')[0]
		user = i.split("small-text\">")[1].split("<")[0]
		views = int(i.split("small-text\">")[2].split(" ")[0].replace(",",""))
		# If video < 3 minutes and this is the first video from this user and less than 50 views
		if int(length.split(":")[0]) < 4 and length.count(":") != 2 and user not in users and views < 50:
			print(id)
			users.append(user)
	except:
		pass

driver.quit()