from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from multiprocessing import Pool
import time
import os
import codecs
import re

tokenizer = RegexpTokenizer(r'\w+') # create nltk tokenizer
en_stop = get_stop_words('en') # create English stop words list
p_stemmer = PorterStemmer() # Create p_stemmer of class PorterStemmer
wrong_drugname = []


def clean_process(drugname):
	# read drug file to extract the side effects content
	filepath = 'drugs/original/{}.txt'.format(drugname)
	drug_file = open(filepath, 'r')
	drug_raw = drug_file.read()
	drug_file.close()

	# clean and tokenize document string
	drug_raw = drug_raw.lower()
	drug_tokens = tokenizer.tokenize(drug_raw)

	# remove stop words from tokens
	drug_stopped_tokens = [i for i in drug_tokens if not i in en_stop]

	# stem tokens
	drug_stemmed_tokens = [p_stemmer.stem(i) for i in drug_stopped_tokens]

	filepath = 'drugs/preprocessed/{}.data'.format(drugname)
	if not os.path.exists(filepath):
		with open(filepath, 'w') as file:
			file.write(str(drug_stemmed_tokens))
			file.close()

def check_parse(drugname):
	filepath = 'drugs/original/{}.txt'.format(drugname)
	drug_file = open(filepath, 'r')
	drug_raw = drug_file.read()
	drug_file.close()

	if 'The page you requested is either undergoing' in drug_raw:
		wrong_drugname.append(drugname)

def sentence_segment(drugname):
	# read drug file to extract the side effects content
	filepath = 'drugs/original/{}.txt'.format(drugname)
	drug_file = open(filepath, 'r')
	drug_raw = drug_file.read()
	drug_file.close()
	
	drug_raw = drug_raw.replace('e.g.', '')
	drug_raw = re.sub('\d+[.]*\d*[%]*', '', drug_raw)
	drug_raw = drug_raw.replace('()', '')
	drug_raw = drug_raw.replace('.', '.\n')
	drug_raw = os.linesep.join([s.lstrip(' ').decode('utf-8') for s in drug_raw.splitlines() if s and s != ' '])
	filepath = 'drugs/preprocessed/{}.txt'.format(drugname)
	with open(filepath, 'w') as file:
		file.write(drug_raw.encode("ascii", errors='ignore'))
		file.close()


if __name__ == "__main__":
	drug_name_file = open('./drugs_com_web_names.txt','r')
	drug_names = drug_name_file.readlines()
	drug_names = [drug_name.replace('\n','') for drug_name in drug_names]
	# sentence_segment('all day allergy')
	# pool = Pool()
	# result = pool.map_async(sentence_segment, drug_names, chunksize=int(len(drug_names)/8))
	# while (True):
	#   if (result.ready()): break
	#   remaining = result._number_left
	#   print ("Waiting for", remaining, "tasks to complete...")
	#   time.sleep(1)
	# print ('All tasks completed!')
	# pool.close()
	for drug_name in drug_names:
		sentence_segment(drug_name)
	# for drugname in drug_names:
	# 	check_parse(drugname)

	# with open('drugs/wrongName.txt', 'w') as file:
	# 	file.write(str(wrong_drugname))
	# 	file.close()