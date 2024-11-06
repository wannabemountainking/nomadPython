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


class BerlinStartupScrapper:

	def __init__(self):
		self.url = "https://berlinstartupjobs.com"
		self.jobs_db = []


	def total_jobs(self):

		# 전체 구직 정보를 리턴함
		# 모든 결과는 이 함수를 통해 확보

		engineering = dict(engineering=self.get_info_of_engineering_jobs())
		skill_areas_jobs = self.collecting_skill_areas_jobs_db()
		skill_areas_jobs.append(engineering)
		return skill_areas_jobs

	def get_info_of_engineering_jobs(self):

		# engineering 분야의 구직 정보를 리턴한다.
		# return : dict => {'company': 회사명, ...}
		engineering_jobs = self.get_skill_db(f"{self.url}/engineering")
		return engineering_jobs

	def collecting_skill_areas_jobs_db(self):

		# skill_areas의 구직정보 데이터를 skill별로 모아 리턴
		# parameter: url
		# return: [{skill_area 명: [{구직정보}, ...]}, ...]

		active_page_soup = self.activate_page(f"{self.url}/engineering/")
		soup = active_page_soup[1]
		skill_sets = self.get_skillset_dict(soup)
		for (skill_area, link) in skill_sets.items():
			job_db = self.get_skill_db(link)
			job_db_dict = {skill_area: job_db}
			self.jobs_db.append(job_db_dict)
		return self.jobs_db

	def get_skillset_dict(self, soup):

		# skilㅣ에 따른 구직 정보 페이지(링크)를 dictionary 형태로 리턴한다.
		# parameter: BeautifulSoup 객체
		# return: dictionary => {'skill_name': 'skill_area/기술명' 링크}

		skill_dict = {}
		popular_skills = soup.find_all("a", class_="bjs-bl--dolphin")
		for skill in popular_skills:
			skill_name = re.sub("\n|\t", "", skill.text.split(" ")[0])
			skill_dict[skill_name] = skill['href']
		return skill_dict

	def get_skill_db(self, url):

		# 각 skill_area 의 정보를 모아서 딕셔너리로 리턴한다.
		# parameter: url
		# return: {
		# 				'company': company 명,
		# 				'job_title': 구직 제목,
		# 				'job_description': job_description,
		# 				'link': link
		# 				}

		jobs_according_to_skills = self.activate_page(url)
		page = jobs_according_to_skills[0]
		soup = jobs_according_to_skills[1]
		job_db = []
		job_pages = soup.find_all(class_="page-numbers")
		number_of_pages = 0
		if job_pages:
			number_of_pages = len(job_pages)
		else:
			number_of_pages = 2

		for i in range(1, number_of_pages):
			if i != 1:
				page.goto(f"{self.url}/engineering/page/{i}/")
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


	def activate_page(self, url):

		# url을 입력받아 playwright의 page 객체, BeautifulSoup 객체를 튜플형태로 리턴한다.
		# parameter: url 기본값 berlin구직 사이트 메인 홈
		# return: 튜플 => (page, soup)


		p = sync_playwright().start()
		browser = p.chromium.launch(headless=False)
		page = browser.new_page()
		page.goto(url)
		content = page.content()
		soup = BeautifulSoup(content, 'html.parser')
		p.stop()
		return (page, soup)

scrapper = BerlinStartupScrapper()
result = scrapper.total_jobs()
pprint(result)