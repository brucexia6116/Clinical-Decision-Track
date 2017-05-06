from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests
import os
import time
import csv

base_url = 'https://www.drugs.com/sfx/'
match_str_pattern = ['Applies to', 'In addition to its needed effects', 'You should check with your doctor',
					'Some of the side effects that can occur', 'Not all side effects for', 'If any of the following',
					'Other dosage forms']

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
		[x.extract() for x in content.findAll('div', class_='referenceList')]
		
		p_content = content.find_all('p')
		ul_content = content.find_all('ul')
		for item in p_content:
			text = item.get_text()
			if item.has_attr("class"):
				if item['class'][0] in ['drug-subtitle', 'status-box', 'disclaimer', 'more-resources-other-brands']:
					continue
			if any([True for str in match_str_pattern if str in text]):
				continue
			if text.endswith('[Ref]'):
				text = text[:-len('[Ref]')]
			content_text += text + '\n'
		for item in ul_content:
			if item.has_attr("class"):
				continue
			content_text += item.get_text() + '\n'
	content_text = os.linesep.join([s for s in content_text.splitlines() if s])
	return content_text

def dump_side_effects(drugname, url):
	# url = base_url + drug_name.replace(' ', '-') + '-side-effects.html'
	filepath = 'drugs/original/{}.txt'.format(drugname)
	# if not os.path.exists(filepath):
	side_effect = get_side_effects(url)
	if side_effect:
		with open(filepath, 'w') as file:
			file.write(side_effect.encode('utf8'))
			file.close()

if __name__ == "__main__":

	with open('drug_com_web_names_links.csv', 'rb') as csv_file:
		reader = csv.reader(csv_file)
		drug_names_links = dict(reader)

	valid_drug_names_links = []
	for k,v in drug_names_links.iteritems():
		if v != 'S' and v != 'None':
			valid_drug_names_links.append((k,v))
	print len(valid_drug_names_links)

	# wrong_drug_names_links = [(wrong_drug_name, drug_names_links[wrong_drug_name]) for wrong_drug_name in wrong_drug_names if 'https' in drug_names_links[wrong_drug_name]]

	# pool = Pool()
	# result = pool.map_async(dump_side_effects, wrong_drug_names_links, chunksize=int(len(wrong_drug_names_links)/8))
	# while (True):
	#   if (result.ready()): break
	#   remaining = result._number_left
	#   print "Waiting for", remaining, "tasks to complete..."
	#   time.sleep(1)
	# print 'All tasks completed!'
	# pool.close()
	for valid_drug_name_link in valid_drug_names_links:
		dump_side_effects(*(valid_drug_name_link))
	# dump_side_effects('abraxane', drug_names_links['abraxane'])

