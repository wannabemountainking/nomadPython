# berlinstartupjobs.com 웹사이트용 스크래퍼를 만듭니다.
# 스크래퍼는 다음 URL을 스크랩할 수 있어야 합니다:
# https://berlinstartupjobs.com/engineering/
# https://berlinstartupjobs.com/skill-areas/python/
# https://berlinstartupjobs.com/skill-areas/typescript/
# https://berlinstartupjobs.com/skill-areas/javascript/
# 첫 번째 URL에는 페이지가 있으므로 pagination 을 처리해야 합니다.
# 나머지 URL은 특정 스킬에 대한 것입니다. URL의 구조에 스킬 이름이 있으므로 모든 스킬을 스크래핑할 수 있는 스크래퍼를 만드세요.
# 회사 이름, 직무 제목, 설명 및 직무 링크를 추출하세요.


import requests
from bs4 import BeautifulSoup
from pprint import pprint

URL = "https://berlinstartupjobs.com"

response = requests.get(f"{URL}/engineering/")
content = response.content

soup = BeautifulSoup(content, 'html.parser')

jobs = soup.find_all("li", class_="bjs-jlid")
print(jobs)
job_db = []

for job in jobs:
	first_link = job.find("a")
	title = first_link.text

	company = job.find("a", class_="bjs-jlid__b").text

	job_description = job.find("div", class_="bjs-jlid__description").text

	link = first_link["href"]

	job_data = dict(
		company=company,
		job_title=title,
		job_description=job_description,
		link=link
	)
	job_db.append(job_data)
print(job_db)
