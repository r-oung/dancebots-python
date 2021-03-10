# Dancebots Python

## Prerequisites
You will need Python 3 and virtual environments.

## Setup
From the root directory, run the following to create a Python virtual environment (`venv`) and install all dependencies:
```
$ cd python/
$ ./setup.sh
```

To activate the virtual environment:
```
$ source venv/bin/activate
```

## Notes
Email from Philipp Reist:
    Given the 8MHz clock of the ATTiny, a pulse (i.e. time between to edges of the MP3 player voltage on the right channel) is considered a RESET, or start of a new 24bit message, if it is longer than 5805 ticks (0.73ms, or 32 samples at 44.1kHz), considered a 1 if it is between 3367 and 5805 ticks, and a 0 if it is below 3367 ticks. Then, the 24 bit message consists of 8bits for the left motor, 8bits for the right motor, and 8 bits for the 8 LEDs. The LSB is sent first. For the motors, bit 0-6 is speed (valid range 0-100), and bit 7 is direction (1 FWD, 0 BWD [this is wrongly labeled in the FW on Bitbucket). For the LEDs, each bit corresponds directly to the LED.

## Protocol:
Messages are 24-bits long, LSB sent first.
```
[ LEFT MOTOR | RIGHT MOTOR | LEDS     ]
[ 01234567   | 01234567    | 01234567 ]
[ 8-bits     | 8-bits      | 8-bits   ]
```

Bit representation is time-modulated as follows:
-------------------------------------------------
TYPE | Ticks		| Interval (msec)
-------------------------------------------------
START|      > 5805 	|             > 0.725625 
    1| 3367 - 5805	|    0.420875 - 0.725625
    0|      < 3367 	|             < 0.420875

The following bit representation will be used in this script:
-----------------------
TYPE | Interval (msec)
-----------------------
START| 2.0 
    1| 0.7
    0| 0.2

```

Therefore, the longest message will be 2.0 + (24 x 0.7) = 18.8 msec.


youtube-dl (https://github.com/rg3/youtube-dl/blob/master/README.md)
$ sudo apt-get install ffmpeg # converts WAV to MP3 files

$ pip install youtube_dl # converts youtube to MP3 files
$ pip install pydub # python library for converting MP3 to WAV and v.v.
$ pip install scipy # for manipulating WAV files
$ pip install matplotlib # for visualising wavforms
$ pip install librosa # audio analysis library


One can use Sonic Visualiser to play and visualize waveforms. It can also be used to annotate the music.
https://www.sonicvisualiser.org/

Workflow:
1. Open an audio file
2. Add a new Time Instance Layer
3. While playing the song, tap on the keyboard ";". A tap can represent a motion primitive, LED pattern, etc. By default annotations will be Cyclical Two-Level Counter (measure/beat). This can be changed under Edit > Number New Instants With
4. Annotations can be exported (CTRL + Y) to a CSV file, which can then be read in by a Python script to generate the dance protocol.

