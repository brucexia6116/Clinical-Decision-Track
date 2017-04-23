from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words

tokenizer = RegexpTokenizer(r'\w+') # create nltk tokenizer
en_stop = get_stop_words('en') # create English stop words list
p_stemmer = PorterStemmer() # Create p_stemmer of class PorterStemmer


def clean_process(drugname):
	# read drug file to extract the side effects content
	filepath = 'drugs/original/{}.txt'.format(drug_name)
	drug_file = open(filepath, 'r')
	drug_raw = drug_file.read()
	drug_file.close()

	# clean and tokenize document string
	drug.raw = drug_raw.lower()
    drug_tokens = tokenizer.tokenize(drug_raw)

    # remove stop words from tokens
    drug_stopped_tokens = [i for i in drug_tokens if not i in en_stop]

    # stem tokens
    drug_stemmed_tokens = [p_stemmer.stem(i) for i in drug_stopped_tokens]

    filepath = 'drugs/preprocessed/{}.txt'.format(drug_name)
	if not os.path.exists(filepath):
		with open(filepath, 'w') as file:
			file.write(drug_stemmed_tokens.encode('utf8'))
			file.close()

if __name__ == "__main__":
	drug_name_file = open('./drugs_com_web_names.txt','r')
	drug_names = drug_name_file.readlines()
	drug_names = [drug_name.replace('\n','') for drug_name in drug_names]
	pool = Pool(processes=16)
	result = pool.map_async(clean_process, drug_names[:5])
	while (True):
	  if (result.ready()): break
	  remaining = result._number_left
	  print "Waiting for", remaining, "tasks to complete..."
	  time.sleep(1)
	print 'All tasks completed!'
	pool.close()