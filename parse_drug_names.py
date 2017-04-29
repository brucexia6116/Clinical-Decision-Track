from bs4 import BeautifulSoup
import requests
import os
import time

base_url = 'https://www.drugs.com'

def parse_drugname():
	agent = {"User-Agent":"Mozilla/5.0"}

	# parse urls that contains the drug names
	root_url = 'https://www.drugs.com/sfx/'
	source=requests.get(root_url, headers=agent).text
	soup = BeautifulSoup(source, 'lxml')
	content = soup.find_all("div", class_="clearAfter")
	content = content[0].find_all('a')
	drug_urls = []
	for element in content:
		drug_urls.append(element['href'])
	
	# parse drug names from the urls obtained before
	drug_names = {}
	for drug_url in drug_urls:
		url = base_url + drug_url
		print url
		while True:
			try:
				source=requests.get(url, headers=agent).text
				break
			except:
				print("Connection refused by the server..")
				time.sleep(5)
		soup = BeautifulSoup(source, 'lxml')
		content = soup.find_all("ul", class_="column-list-2 sitemap-list")
		content = content[0].find_all('li')
		for element in content:
			drug_names[element.get_text()] = element.a['href']
	
	# write drug names to file
	filepath = 'drugs_com_web_names_new.txt'
	if drug_names:
		with open(filepath, 'w') as file:
			file.write(str(drug_names))
			file.close()

if __name__ == "__main__":
	parse_drugname()