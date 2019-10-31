#!/usr/bin/env python3

from pydub import AudioSegment
import os
import tarfile


def wavAnaliser(wavfile):
    sound = AudioSegment.from_wav(wavfile)

    # frame rate = sample rate
    inrate = sound.frame_rate
    duration_in_millisec = len(sound)

    # 1= mono, 2= stereo
    channel_count = sound.channels

    # Number of bytes in each sample (1 means 8 bit, 2 means 16 bit, etc). CD Audio is 16 bit, (sample width of 2 bytes).
    if sound.sample_width ==1: bytes_per_sample="8 bit"
    elif sound.sample_width ==2: bytes_per_sample="16 bit"
    else: bytes_per_sample="more then 16 bit"

    # frame_width is equal to channels * sample_width

    print("\n-------------------------------\nInput sample rate: ", inrate)
    print("Duration in seconds: ", round(duration_in_millisec/1000))
    print("Channels (1=mono, 2=stereo): ", channel_count)
    print("Bytes per Sample (sample width, 8 or 16 bit): ", bytes_per_sample)
    print("---------------------------------")

if __name__ == '__main__':  # Section is only executed if this script was directly esecuted. If called from another script, it isn't.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="input is a WAV file")
    args = parser.parse_args()
    wavfile = args.input
    wavAnaliser(wavfile)