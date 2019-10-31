#!/usr/bin/env python3

from pydub import AudioSegment
import argparse
import os
from _helper_downsample_wav_walkest1 import main
import tarfile
from scipy.io.wavfile import read
import numpy

downsampleWav = main

parser = argparse.ArgumentParser()
parser.add_argument('input', help="input is the source mp3 file")
parser.add_argument('output', help="output is the destination directory path (incl. dst folder)")
parser.add_argument('name', help="choose a name (idealy no spaces)")

print("\nThe target samplerate can be specified in _helper_downsample_wav_swa.py. Default values are inrate=44100, outrate=16000, inchannels=2, outchannels=1\n...")

args = parser.parse_args()

src = args.input
dst = args.output 
if dst[-1] != "/":  dst = dst+"/"
name = args.name

try: os.mkdir(dst)   # make the dst folder
except: pass

# Set split parameters
t1 = 0
t2 = 25000
tdelta = 25000 # 1000 equals 1s
i = 0


def save_wav(t1,t2,i,dst, name):
	newAudio2 = newAudio[t1:t2]     # taking subset of original wav
	wavpath = dst + "/" + name + str(i) + ".wav"  # defining wavpath incl. enumerator
	newAudio2.export(wavpath, format="wav")     # saving newAudio2 wav object at wavpath
	tar.add(wavpath, arcname=os.path.basename(wavpath))		# Add wav file to .tar
	os.remove(wavpath)
	return


# convert mp3 to wav, split and save as .tar
newAudio = AudioSegment.from_mp3(src)
wavpath = dst + "/" + name + ".wav"
newAudio.export(wavpath, format="wav")
inrate, outrate, channels, samplewidth = downsampleWav(wavpath, wavpath)
tar = tarfile.open(dst+"/"+name+".tar", "w")

while t2 < len(newAudio):
	save_wav(t1,t2,i,dst, name)
	t1 += tdelta
	t2 += tdelta
	i += 1

t2 = len(newAudio) # for the residuals, in case total length doesn't divide through tdelta
save_wav(t1,t2,i,dst, name)
tar.close()

print("Framerate changed from %s to %s, Channels remain unchanged at %s and samplewidth remains unchanged at %s." % (inrate,outrate,channels,samplewidth))
print("Split file into %s files and saved .tar at this PATH: %s." % (i, dst+"/"+name+".tar"))