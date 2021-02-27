#! /usr/bin/env python

# Use pyaudio to open the microphone and run aubio.pitch on the stream of
# incoming samples. If a filename is given as the first argument, it will
# record 5 seconds of audio to this location. Otherwise, the script will
# run until Ctrl+C is pressed.

# Examples:
#    $ ./python/demos/demo_pyaudio.py
#    $ ./python/demos/demo_pyaudio.py /tmp/recording.wav

import pyaudio
import sys
import numpy as np
import aubio
from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller as MouseController
import time
import keypress
import window

keyboard = Controller()
mouse = MouseController()

#pitches
rightClick = 45
leftClick = 50
A=57
B=59#a
C=60#w
D=62#s
E=64#d
mmm = 72

F2 = 65
G2 = 67
A2 = 69
B2 = 71

#keys
e = 0x12
w = 0x11
a = 0x1E
s = 0x1F
d = 0x20

pitchdict = {A : e, B : a, C : w, D : s, E : d, mmm : w}# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
buffer_size = 1024
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)

if len(sys.argv) > 1:
    # record 5 seconds
    output_filename = sys.argv[1]
    record_duration = 5 # exit 1
    outputsink = aubio.sink(sys.argv[1], samplerate)
    total_frames = 0
else:
    # run forever
    outputsink = None
    record_duration = None

# setup pitch
tolerance = 0.9
win_s = 4096 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)
epress = 0
print("*** starting recording")
while True:
    try:
        audiobuffer = stream.read(buffer_size)
        signal = np.fromstring(audiobuffer, dtype=np.float32)

        pitch = pitch_o(signal)[0]
        confidence = pitch_o.get_confidence()
        window.makeActive()
        print("{} / {}".format(pitch,confidence))
        #print("{} / {}".format(pitch,confidence))
        for tone in pitchdict:
            if (  abs((round(pitch) - tone)) < 1):
                print(pitch, tone)
                if (pitchdict[tone] == e):
                    epress = epress + 1
                    print(epress, epress % 100)
                    if (epress % 10 == 9):
                        keypress.PressKey(pitchdict[tone])
                        time.sleep(0.05)
                        keypress.ReleaseKey(pitchdict[tone])
                    break
                keypress.PressKey(pitchdict[tone])
                time.sleep(0.05)
                keypress.ReleaseKey(pitchdict[tone])
        if(round(pitch) == F2):
            keypress.moveMouse(-10, 0)
        if(round(pitch) == G2):
            keypress.moveMouse(0, 10)
        if(round(pitch) == A2):
            keypress.moveMouse(0, -10)
        if(round(pitch) == B2):
            keypress.moveMouse(10, 0)
        if(round(pitch) == leftClick):
            mouse.press(Button.left)
            time.sleep(0.1)
            mouse.release(Button.left)
        if(round(pitch) == rightClick):
            mouse.press(Button.right)
            time.sleep(0.1)
            mouse.release(Button.right)
        if outputsink:
            outputsink(signal, len(signal))

        if record_duration:
            total_frames += len(signal)
            if record_duration * samplerate < total_frames:
                break
    except KeyboardInterrupt:
        print("*** Ctrl+C pressed, exiting")
        break
a
aprint("*** done recording")
stream.stop_stream()
astream.close()
aaaaaaaaaaaaaaaaaaaaaap.terminate()
