# berlinstartupjobs.com 웹사이트용 스크래퍼를 만듭니다.
# 스크래퍼는 다음 URL을 스크랩할 수 있어야 합니다:
# https://berlinstartupjobs.com/engineering/
# https://berlinstartupjobs.com/skill-areas/python/
# https://berlinstartupjobs.com/skill-areas/typescript/
# https://berlinstartupjobs.com/skill-areas/javascript/
# 첫 번째 URL에는 페이지가 있으므로 pagination 을 처리해야 합니다.
# 나머지 URL은 특정 스킬에 대한 것입니다. URL의 구조에 스킬 이름이 있으므로 모든 스킬을 스크래핑할 수 있는 스크래퍼를 만드세요.
# 회사 이름, 직무 제목, 설명 및 직무 링크를 추출하세요.


from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from pprint import pprint


URL = "https://berlinstartupjobs.com"
jobs_db = []

def activate_page(url):
	p = sync_playwright().start()
	browser = p.chromium.launch(headless=False)
	page = browser.new_page()
	page.goto(url)
	content = page.content()
	soup = BeautifulSoup(content, 'html.parser')
	p.stop()
	return (page, soup)

def get_info_of_engineering_jobs():
	active_page_soup = activate_page(f"{URL}/engineering/")
	page = active_page_soup[0]
	soup = active_page_soup[1]
	engineering_jobs = get_skill_db(page, soup)
	return engineering_jobs

def collecting_skill_areas_jobs_db(url):
	active_page_soup = activate_page(f"{URL}/engineering/")
	# page = active_page_soup[0]
	soup = active_page_soup[1]
	skill_sets = get_skillset_dict(soup)
	for (skill_area, link) in skill_sets.items():
		job_db = get_skill_db(link)
		job_db_dict = {skill_area: job_db}
		jobs_db.append(job_db_dict)
	return jobs_db


def get_skillset_dict(soup):
	skill_dict = {}
	popular_skills = soup.find_all("a", class_="bjs-bl--dolphin")
	for skill in popular_skills:
		skill_name = re.sub("\n|\t", "", skill.text.split(" ")[0])
		skill_dict[skill_name] = skill['href']
	return skill_dict

def get_skill_db(url):
	jobs_according_to_skills = activate_page(url)
	page = jobs_according_to_skills[0]
	soup = jobs_according_to_skills[1]
	job_db = []
	job_pages = soup.find_all(class_="page-numbers")
	number_of_ages = 0
	if job_pages:
		number_of_pages = len(job_pages)
	else:
		number_of_pages = 2

	for i in range(1, number_of_pages):
		if i != 1:
			page.goto(f"{URL}/engineering/page/{i}/")
			newContent = page.content()
			soup = BeautifulSoup(newContent, 'html.parser')
		jobs = soup.find_all("li", class_="bjs-jlid")
		for job in jobs:
			first_link = job.find("a")
			title = first_link.text
			company = job.find("a", class_="bjs-jlid__b").text
			job_description = re.sub("\n|\t", "", job.find("div", class_="bjs-jlid__description").text)
			link = first_link["href"]
			job_data = dict(
				company=company,
				job_title=title,
				job_description=job_description,
				link=link
			)
			job_db.append(job_data)
		return job_db

pprint(collecting_skill_areas_jobs_db(URL))