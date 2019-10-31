#!/usr/bin/env python3

from pydub import AudioSegment
import argparse
import os
import tarfile

parser = argparse.ArgumentParser(description='Preprocesses audio files for testing with AST models (conversion to wav, downsampling to 16k, splitting (no sentence detection)')
parser.add_argument('input', help="input is the source mp3 file")
parser.add_argument('output', help="output is the destination directory path (incl. dst folder)")
parser.add_argument('name', help="choose a name (idealy no spaces)")
parser.add_argument('--mp3toWav', default=False, help="Set True if file should be converted from mp3 to wav")
parser.add_argument('--resample', default=False, help="Set True if file should be resampled to 'target_samplerate'")
parser.add_argument('--target_samplerate', default=16000, help="choose a samplerate, default value is 16k")
parser.add_argument('--split', default=False, help="Set to 'True' if provided mp3 should additionally be split into segments (length set by 'split_length')")
parser.add_argument('--split_length', default=15, help="Set 'split_length' to number of seconds.)")
args = parser.parse_args()

dst = args.output 
if dst[-1] != "/":  dst = dst+"/"
path = dst+args.name

try: os.mkdir(dst)   # make the dst folder
except: pass

# Set split parameters
t1 = 0
tdelta = int(args.split_length) * 1000 # 1000 equals 1sec
t2 = tdelta
i = 0


def save_wav(newAudio, t1,t2,i,path):
	newAudio_seg = newAudio[t1:t2]     # taking subset of original wav
	wavpath = path + str(i).zfill(4) + ".wav"  # defining wavpath incl. enumerator
	newAudio_seg.export(wavpath, format="wav")  # saving newAudio wav object at wavpath
	tar.add(wavpath, arcname=os.path.basename(wavpath))		# Add wav file to .tar
	os.remove(wavpath)
	return


if args.mp3toWav: # Convert from mp3 to wav
	os.system("sox {} {}.wav".format(args.input,path))
	print("\nmp3 file converted to wav")

if args.resample: # resampling wav to target_samplerate
	newAudio = AudioSegment.from_wav(path+".wav")
	inrate = newAudio.frame_rate
	newAudio = newAudio.set_frame_rate(args.target_samplerate)
	print("\nFramerate changed from %s to %s" % (inrate, args.target_samplerate))

if args.split: # split and save as .tar
	tar = tarfile.open(path+".tar", "w")

	while t2 < len(newAudio):
		save_wav(newAudio,t1,t2,i,path)
		t1 += tdelta
		t2 += tdelta
		i += 1

	t2 = len(newAudio) # for the residuals, in case total length doesn't divide through tdelta
	save_wav(newAudio,t1,t2,i,path)
	tar.close()
	os.remove(path+".wav")
	print("\nSplit file into %s files and saved .tar at this PATH: %s.\n" % (i, path + ".tar"))


