# called by main_convert_split_downsample_swa.py
# -*- coding: utf-8 -*-
#
#  downsample.py
#
#  Copyright 2015 John Coppens <john@jcoppens.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import wave
import numpy as np
import scipy.signal as sps

class DownSample():
    def __init__(self):
        self.out_rate = 16000.0

    def open_file(self, fname):
        try:
            self.in_wav = wave.open(fname)
        except:
            print("Cannot open wav file (%s)" % fname)
            return False

        self.in_wav_framerate = self.in_wav.getframerate()
        self.in_nframes = self.in_wav.getnframes()
        print("Frames: %d" % self.in_wav.getnframes())

        if self.in_wav.getsampwidth() == 1:
            self.nptype = np.uint8
        elif self.in_wav.getsampwidth() == 2:
            self.nptype = np.uint16

        return self.in_wav_framerate, self.out_rate

    def resample(self, fname):
        self.out_wav = wave.open(fname, "w")
        self.out_wav.setframerate(self.out_rate)
        self.out_wav.setnchannels(self.in_wav.getnchannels())
        self.out_wav.setsampwidth (self.in_wav.getsampwidth())
        self.out_wav.setnframes(1)

        print("Nr output channels: %d" % self.out_wav.getnchannels())

        audio = self.in_wav.readframes(self.in_nframes)
        nroutsamples = round(len(audio) * self.out_rate/self.in_wav_framerate)
        print("Nr output samples: %d" %  nroutsamples)

        audio_out = sps.resample(np.fromstring(audio, self.nptype), nroutsamples)
        audio_out = audio_out.astype(self.nptype)

        self.out_wav.writeframes(audio_out.copy(order='C'))

        self.out_wav.close()
        return self.in_wav.getnchannels(), self.in_wav.getsampwidth()

    def closeWav(self):
        self.in_wav.close()

def main(inwave, outwave):
    ds = DownSample()
    inframerate, outframerate = ds.open_file(inwave)
    if inframerate != outframerate:
        channels, samplewidth = ds.resample(outwave)
        return inframerate, outframerate, channels, samplewidth
    else:
        closeWav()
        return inframerate, outframerate