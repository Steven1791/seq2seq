#!/usr/bin/env python3

import argparse
import os
import tarfile
from pydub import AudioSegment
from wav_analiser_walkest1 import wavAnaliser

parser = argparse.ArgumentParser(description='Redistribute audio files of the Speech-Translation TED corpus provided by IWSLT https://sites.google.com/site/iwsltevaluation2018/Lectures-task')
parser.add_argument('input', help="yaml file (dev test or train or other (i.e. offlimit)")
parser.add_argument('wavDirectory', help="directory where all the wav files are stored")
args = parser.parse_args()

yamlfile = args.input
corpus_name = os.path.splitext(os.path.basename(args.input))[0]  #split removes extension i.e. .yaml
tar_dir = os.path.dirname(args.input)+"/"+corpus_name+".tar"     # .tar with all wav files for the corpus at hand

# Problem Nr. 1: in some long lines the end of the line is moved to the next line.
f = open(yamlfile, "r")
newlines = []
while 1:
	line = f.readline()
	if line == "": break  # if f.readline() returns an empty string = end of file. Blank line is represented by '\n'
	if ".wav" not in line:   # check if line isn't complete
		line = line + f.readline()[1:]   # concatenating two lines, [1:] because 2nd line has two spaces at beginning.
	newlines.append(line)
f.close()

tar = tarfile.open(tar_dir, "w")
print("\nExtracting audio segments...")
for i, line in enumerate(newlines):
	line = line.replace("}", "")
	line = line.replace("\n", "")
	line = line.replace(",", "")
	tokens = line.split(" ")
	try:
		wavefile = tokens[8]
		waveSegmID = wavefile[:-4]+"_"+str(i).zfill(4)+".wav"  # i corresponds to the i'th FULL line in the provided yaml file*
		duration = int(float(tokens[2])*1000)  # *1000 since msec's are needed, not seconds.
		offset = int(float(tokens[4])*1000)

		wavesegm = AudioSegment.from_wav(args.wavDirectory + "/" + wavefile)
		wavesegm = wavesegm[offset : offset+duration]
		wavesegm.export(args.wavDirectory + waveSegmID, format="wav")  # saving temp wavesegm object
		tar.add(args.wavDirectory + waveSegmID, arcname=waveSegmID)
		os.remove(args.wavDirectory + waveSegmID)  # deleting temp wavesegm file

	except IndexError as e:
		print (e)
		print ("Line couldn't be red, check yaml file, every line should contain duration, offset and a wavefile.\
		Assumes lines look like this: - {duration: 2.4, offset: 146.38, speaker_id: spk.1922, wav: ted_1922.wav}\n")
	except FileNotFoundError as e:
		print (e)
		print ("Didn't find file(path)")
	except:
		print ("check Error type, all possible errors should be adressed by the except clause above (Line 52)")

tar.close()
print("Extraction complete.\n")

#Examine one example wav file:
print("Specs of audio files, duration not relevant (random audiosegment):")
wavAnaliser(args.wavDirectory + "/" + wavefile)

print("---------------------------------------")
print("\n%s wav files were added to %s \n" %(len(newlines), tar_dir))
print("---------------------------------------")
