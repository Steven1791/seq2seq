#!/usr/bin/env python3

import shutil
import argparse
import os
import tarfile
from pydub import AudioSegment
from wav_analiser_walkest1 import wavAnaliser

parser = argparse.ArgumentParser(description='Redistribute audio files of the Speech-Translation TED corpus provided by IWSLT https://sites.google.com/site/iwsltevaluation2018/Lectures-task')
parser.add_argument('yamlfile', help="the yaml file, which determines which wav segment belongs to which sentence")
parser.add_argument('wavDirectory', help="directory where all the wav files are stored")
parser.add_argument('textfile', help="Textfile corresponding to the yamlfile")
args = parser.parse_args()

newDeepSpeechDir = os.path.dirname(args.wavDirectory)+"/DeepSpeech_Data/"

# for the_file in os.listdir(newDeepSpeechDir):  #sort first !!
# 	file_path = os.path.join(newDeepSpeechDir, the_file)
# 	try:
# 		if os.path.isfile(file_path):
# 			os.unlink(file_path)
# 		elif os.path.isdir(file_path): shutil.rmtree(file_path)
# 	except Exception as e:
# 		print(e)

try:
	os.makedirs(newDeepSpeechDir + "clips")
except:
	pass

yamlfile = args.yamlfile
textfile = args.textfile
new_textfile = newDeepSpeechDir + os.path.basename(textfile) + ".tsv"

corpus_name = os.path.splitext(os.path.basename(args.yamlfile))[0]  # split removes extension i.e. .yaml

# Problem Nr. 1: in some long lines the end of the line is moved to the next line.
f = open(yamlfile, "r")
p = open(textfile, "r")
newlines = []
wavlist_ID = []
speakerlist_ID = []
textlist_ID = []
negList = []

i=0
while 1:
	i += 1
	line = p.readline()
	if line == "": break
	line = line.replace("\n", "")
	textlist_ID.append(line)
	print("reading line ", i)
p.close()

while 1:
	line = f.readline()
	if line == "": break  # if f.readline() returns an empty string = end of file. Blank line is represented by '\n'
	if ".wav" not in line:   # check if line isn't complete
		line = line + f.readline()[1:]   # concatenating two lines, [1:] because 2nd line has two spaces at beginning.
	newlines.append(line)
f.close()

print("\nExtracting audio segments...")
for i, line in enumerate(newlines):
	line = line.replace("}", "")
	line = line.replace("\n", "")
	line = line.replace(",", "")
	tokens = line.split(" ")
	try:
		wavefile = tokens[8]
		duration = int(float(tokens[2])*1000)  # *1000 since msec's are needed, not seconds.
		offset = int(float(tokens[4])*1000)
		speakerlist_ID.append(tokens[6])
		if duration > 15000: negList.append(i)

		wavesegm = AudioSegment.from_wav(args.wavDirectory + "/" + wavefile)
		wavesegm = wavesegm[offset : offset + duration]
		waveSegmID = wavefile[:-4] + "_" + str(i).zfill(4) + ".mp3"  # i corresponds to the i'th FULL line in the provided yaml file*
		wavlist_ID.append(waveSegmID)
		wavesegm.export(newDeepSpeechDir + "clips/" + waveSegmID, format="mp3")  # saving mp3 object

	except IndexError as e:
		print (e)
		print ("Line couldn't be red, check yaml file, every line should contain duration, offset and a wavefile.\
		Assumes lines look like this: - {duration: 2.4, offset: 146.38, speaker_id: spk.1922, wav: ted_1922.wav}\n")
	except FileNotFoundError as e:
		print (e)
		print ("Didn't find file(path)")
	except:
		print ("check Error type, all possible errors should be addressed by the except clause above (Line 52)")

with open (new_textfile, 'w') as newtxtfile:
	newtxtfile.writelines("client_id\tpath\tsentence\tup_votes\tdown_votes\tage\tgender\taccent\n")
	for i in range(len(wavlist_ID)):
		if i not in negList:
			newtxtfile.writelines(speakerlist_ID[i] +"\t"+ wavlist_ID[i] +'\t'+ textlist_ID[i] +"\t0\t0\t0\t0\t0\n")

print("Extraction complete.\n")

#Examine one example wav file:
print("Specs of audio files, duration not relevant (random audiosegment):")
wavAnaliser(args.wavDirectory + "/" + wavefile)

print("---------------------------------------")
print("\n%s mp3 files were added to %s \n" %(len(newlines)-len(negList), newDeepSpeechDir + "clips"))
print("---------------------------------------")
