#!/usr/bin/env python3

import io
import os
import argparse

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
client = speech.SpeechClient()

parser = argparse.ArgumentParser(description='Uploads and gets provided wav files from Google Speech transcription API')
parser.add_argument('input', help="directory with only audio files to be transcribed")
args = parser.parse_args()

transcript_file = os.path.dirname(args.input) + "/" + os.path.splitext(os.path.basename(args.input))[0] + "_transcript.txt"
wavdir = args.input
fileList = []
for subdir, dirs, files in os.walk(wavdir):
    for file in files:
        fileList.append(os.path.join(wavdir, subdir, file))

fileList.sort()
print("\n%s Files are sent to Google for transcription, this can take a while!\n" %len(fileList))

with open(transcript_file, 'w') as transcript:
    for file_name in fileList:

        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US')

        # Detects speech in the audio file
        response = client.recognize(config, audio)
        transcr = []
        for result in response.results:  # if the audio contains multiple sentences, each is seperated to one result
            transcr.append(result.alternatives[0].transcript)  # but this is not wanted by me, so I re-connect them

        print(os.path.splitext(os.path.basename(file_name))[0], ' transcribed: ', " ".join(transcr))
        transcript.writelines(" ".join(transcr) + "\n")
