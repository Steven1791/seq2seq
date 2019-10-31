#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

import argparse
import os
from collections import Counter
import string

parser = argparse.ArgumentParser(description='creates a character/word vocab list, out of the source file provided.')
parser.add_argument('input', help="train corpus to extract vocab from")
parser.add_argument('vocab_file_name', help="name of vocab file, without path! "
					"USE language Extension at the End i.e. 'vocab.char.en' resp. 'vocab.en'")
parser.add_argument('--min_count', default= 1, help="min count a character needs to be added to vocab list.")
parser.add_argument('--size', default= -1, help="define max number of characters/words wanted in vocabulary")
parser.add_argument('--character_level', default=True, help='If True, builds '
					'a character-level vocabulary. If False, a word level vocabulary.')
parser.add_argument('--default_EN_dictionary', default=False, help="If True, a default English dict will be written not dependent"
					" on any input files. only ascii_lowercase and digits and space")
parser.add_argument('--default_DE_dictionary', default=False, help="If True, a default German dict will be written not dependent"
					" on any input files. only ascii_lowercase and uppercase and digits and Umlaute (ö,ä,ü) and space")
args = parser.parse_args()

train_corpus	= args.input
size 			= args.size
min_count 		= int(args.min_count)
vocab_file 		= os.path.dirname(args.input) + "/" + args.vocab_file_name

_BOS = '<S>'			# Character for Beginning Of Sentence
_EOS = '</S>'			# Character for End Of Sentence
_UNK = '<UNK>'
_KEEP = '<KEEP>'
_DEL = '<DEL>'
_INS = '<INS>'
_SUB = '<SUB>'
_NONE = '<NONE>'

_START_VOCAB = [_BOS, _EOS, _UNK, _KEEP, _DEL, _INS, _SUB, _NONE]


vocab = Counter()		# Counter() is a 'intelligent' dictionary, i.e. most_common(n)
keys_to_del = list()
with open(train_corpus) as input_file, open(vocab_file, 'w') as output_file:
	if args.default_EN_dictionary:
		vocab_list = _START_VOCAB + list(set(string.ascii_lowercase)) + list(set(string.digits)) + list(" ")
		# "abcdefghijklmnopqrstuvwxyz0123456789"

	elif args.default_DE_dictionary:
		vocab_list = _START_VOCAB + list(string.ascii_lowercase)+ list(string.ascii_uppercase) + list(string.digits) + list('äüöÄÜÖ') + list(" ")
		# "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789äüöÄÜÖ"

	else:
		for line in input_file:
			line = line.strip() if args.character_level else line.split()
			for w in line:
				if w not in _START_VOCAB:
					vocab[w] += 1

		if min_count > 1:
			for (w, c) in vocab.items():
				if c < min_count:
					keys_to_del.append(w)

			for w in keys_to_del:
				del vocab[w]

		print("The characters least common are: ", vocab.most_common()[:-7 - 1:-1])
		print("The most common characters  are: ", vocab.most_common(5))

		vocab_list = _START_VOCAB + sorted(vocab, key=lambda w: (-vocab[w], w))

		if 0 < size < len(vocab_list):
			vocab_list = vocab_list[:size]

	output_file.writelines(w + '\n' for w in vocab_list)

print("---------------------------------------")
print("Vocab file created here: ", vocab_file)
print(vocab_list)
print("---------------------------------------")
