from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests
import os
import time

base_url = 'https://www.drugs.com/sfx/'

def get_side_effects(url):
	agent = {"User-Agent":"Mozilla/5.0"}
	content_text = ''
	while content_text == '':
		try:
			source=requests.get(url, headers=agent).text
		except:
			print("Connection refused by the server..")
			time.sleep(5)
			continue
		soup = BeautifulSoup(source, 'lxml')
		content = soup.find_all("div", class_="contentBox")
		content = content[0]
		[x.extract() for x in content.findAll('div', class_='nav nav-tabs vmig clearAfter')]
		
		p_content = content.find_all('p')
		ul_content = content.find_all('ul')
		for item in p_content:
			if item.has_attr("class"):
				if item['class'][0] in ['status-box', 'disclaimer', 'more-resources-other-brands']:
					continue
			content_text += item.get_text() + '\n'
		for item in ul_content:
			if item.has_attr("class"):
				continue
			content_text += item.get_text() + '\n'
	return content_text

def dump_side_effects(drug_name):
	url = base_url + drug_name.replace(' ', '-') + '-side-effects.html'
	filepath = 'drugs/original/{}.txt'.format(drug_name)
	if not os.path.exists(filepath):
		side_effect = get_side_effects(url)
		if side_effect:
			with open(filepath, 'w') as file:
				file.write(side_effect.encode('utf8'))
				file.close()

if __name__ == "__main__":
	drug_name_file = open('./drugs_com_web_names.txt','r')
	drug_names = drug_name_file.readlines()
	drug_names = [drug_name.replace('\n','') for drug_name in drug_names]
	# pool = Pool()
	# result = pool.map_async(dump_side_effects, drug_names)
	# # while (True):
	# #   if (result.ready()): break
	# #   remaining = result._number_left
	# #   print "Waiting for", remaining, "tasks to complete..."
	# #   time.sleep(1)
	# # print 'All tasks completed!'
	# pool.close()
	for drug_name in drug_names:
		dump_side_effects(drug_name)

