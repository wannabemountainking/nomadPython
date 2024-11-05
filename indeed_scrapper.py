
# from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright
# from pprint import pprint
# import time
#
# def extract_indeed_jobs(search_text):
# 	URL = "https://kr.indeed.com"
#
# 	p = sync_playwright().start()
# 	browser = p.chromium.launch(headless=False)
# 	page = browser.new_page()
# 	page.goto(URL)
# 	time.sleep(2)
# 	page.locator("input#text-input-what").fill(search_text)
# 	time.sleep(2)
# 	page.keyboard.down("Enter")
# 	time.sleep(2)
# 	content = page.content()
# 	time.sleep(2)
#
# 	soup = BeautifulSoup(content, "html.parser")
# 	job_cards = soup.find_all("td", class_="resultContent")
#
# 	jobs_db = []
# 	for job_card in job_cards:
# 		main_info = job_card.find("h2", class_="jobTitle")
# 		secondary_info = job_card.find("div", class_="company_location")
#
# 		website = f'{URL}{main_info.find("a")["href"]}'
# 		title = main_info.find("span")["title"]
# 		company = secondary_info.find("span", class_="css-1h7lukg").text
# 		location = secondary_info.find("div", class_="css-1restlb").text
# 		if salary:
# 			salary = salary.text
# 		job_data = dict(
# 			title=title,
# 			website=website,
# 			company=company,
# 			location=location,
# 		)
# 		jobs_db.append(job_data)
# 	pprint(jobs_db)
# 	p.stop()

#
from playwright.sync_api import sync_playwright
import time
from pprint import pprint
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword, is_headless=False, sleep_time=2):
	URL = "https://www.wanted.co.kr/"
	JOB_CARD_CLASS_NAME = "JobCard_container__REty8"
	JOB_TITLE_CLASS_NAME = "JobHeader_JobHeader__PositionName__kfauc"
	COMPANY_CLASS_NAME = "JobHeader_JobHeader__Tools__Company__Link__zAvYv"
	WORKPLACE_CAREER_CLASS_NAME = "JobHeader_JobHeader__Tools__Company__Info__yT4OD"

	result = get_search_result(search_text=keyword,
								is_headless=is_headless,
								sleep_time=sleep_time,
								url=URL,
								job_card=JOB_CARD_CLASS_NAME,
								job_title=JOB_TITLE_CLASS_NAME,
								company_name=COMPANY_CLASS_NAME,
								workplace=WORKPLACE_CAREER_CLASS_NAME
								)
	return result

def get_search_result(search_text, is_headless, sleep_time, url, job_card, job_title, company_name, workplace):
	p = sync_playwright().start()
	browser = p.chromium.launch(headless=is_headless)
	page = browser.new_page()
	page.goto(f"{url}search?query={search_text}&tab=position")
	for _ in range(2):
		page.keyboard.down("PageDown")
		time.sleep(sleep_time)
	content = page.content()

	soup = BeautifulSoup(content, 'html.parser')
	jobs_db = goto_static_html(soup, page, sleep_time, url, job_card, job_title, company_name, workplace)

	p.stop()
	return jobs_db

def goto_static_html(soup, page, sleep_time, url, job_card, job_title, company_name, workplace):
	jobs_db = []
	job_cards = soup.find_all("div", class_=job_card)
	for i in range(0, len(job_cards)):
		job_card_url = f'{url}{job_cards[i].find("a")["href"]}'
		page.goto(job_card_url)
		time.sleep(sleep_time)
		newContent = page.content()
		new_soup = BeautifulSoup(newContent, 'html.parser')
		job = search_static_html(new_soup, job_card_url, job_title, company_name, workplace)
		jobs_db.append(job)
	return jobs_db

def search_static_html(soup, url, job_title, company_name, workplace):
	title = soup.find("h1", class_=job_title).text
	company = soup.find("a", class_=company_name).text
	work_place, career = soup.find_all("span", class_=workplace)
	work_place, career = [element.text for element in [work_place, career]]

	job = {
		"title": title,
		"company": company,
		"website": url,
		"location": work_place,
	}
	return job

pprint(extract_wwr_jobs("ios"))

