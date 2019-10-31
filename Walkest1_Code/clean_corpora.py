#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

# just above is the Encoding declaration for ä,ö,ü !!

import argparse
import os
import re
from collections import Counter
import string

parser = argparse.ArgumentParser(description='preprocess ground truth text, manly removing/replacing characters, according to the vocab list')
parser.add_argument('corpus', help="input corpus e.g. training corpus, file is overwritten with clean data")
parser.add_argument('vocab_list_file', help="only characters listed on the vocab list are kept!")
args = parser.parse_args()

raw_file 		= re.sub(r'([^\.]*)$' , r'raw.\1', args.corpus)  # add .raw to filename (original file)
clean_file		= args.corpus
vocab_list		= []
with open(args.vocab_list_file, 'r') as file:
	for line in file:
		vocab_list.append(line.replace('\n', ''))
print(vocab_list)


with open(args.corpus, 'r') as input_file, open(raw_file, 'w') as output_file: # save a copy of original file
	output_file.writelines(w + '\n' for w in input_file)

bad_char_list = list()					# make a list with all 'bad' chars
with open(clean_file, 'r') as file:
	for line in file:
		for char in line:
			if char not in vocab_list:
				if char not in bad_char_list:
					bad_char_list.append(char)

cleaned_corpus = list()
with open(clean_file, 'r') as file:
	for line in file:
		if 'A' not in vocab_list: 				# this means uppercase letters aren't wanted
			for i in range(26):
				#data = line.replace(string.ascii_uppercase[i], string.ascii_lowercase[i])
				data = line.lower()
			data = data.replace('Ü', 'ü')
			data = data.replace('Ö', 'ö')
			data = data.replace('Ä', 'ä')
		else:
			data = line

		data = data.replace('ß', 'ss')
		data = re.sub('(\w)-(\w)',r'\1 \2', data)  # z.B. CO2-neutral --> C02 neutral

		for char in data:
			if char in bad_char_list:
				data = data.replace(char,'')

		cleaned_corpus.append(data)

with open(clean_file, 'w') as output_file:		# final writing
	output_file.writelines(line + '\n' for line in cleaned_corpus)


print("---------------------------------------")
print("Corpus cleaned and saved here: ", clean_file)
print("A copy of the original raw corpus is saved here: ", raw_file)
print("---------------------------------------")
print(bad_char_list)
print(cleaned_corpus[0:5])
