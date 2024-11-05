from bs4 import BeautifulSoup
import requests
from pprint import pprint

def site_data():
	nomad_url = "https://weworkremotely.com/remote-full-time-jobs"
	response = requests.get(url=nomad_url)
	soup = BeautifulSoup(response.content, "html.parser")
	return [nomad_url, soup]

def scrape_jobs(url, soup):
	all_jobs = []
	jobs = soup.find("section", class_="jobs").find_all("li", class_="feature")
	for job in jobs:
		info_area = job.find("div", class_="tooltip--flag-logo").next_sibling
		title = info_area.find("span", class_="title").text
		company, position, region = [element.text for element in info_area.find_all("span", class_="company")]
		website = f'{url}{info_area["href"]}'
		job_info = {
			"title": title,
			"company": company,
			"position": position,
			"region": region,
			"website": website
		}
		all_jobs.append(job_info)
	return all_jobs

def get_pages():
	url, soup = site_data()
	all_pages = soup.find("div", class_="pagination").find_all("span", class_="page")
	number_of_pages = len(all_pages)
	print(number_of_pages)
	for page in range(0, 4):
		page_url = f'{url}?page={page + 1}'
		print(page_url)
		response = requests.get(url=page_url)
		page_soup = BeautifulSoup(response.content, 'html.parser')
		return scrape_jobs(page_url, page_soup)

get_pages()