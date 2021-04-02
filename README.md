[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Dancebots Python

## Prerequisites
You will need Python 3 and virtual environments.

## Setup
From the root directory, run the following to create a Python virtual environment (`venv`) and install all dependencies:
```
cd python/
./setup.sh
```

To activate the virtual environment:
```
source venv/bin/activate
```

### youtube-dl
Follow online installation instructions [here](https://github.com/ytdl-org/youtube-dl/blob/master/README.md#configuration)


## Protocol:
Messages are 3 bytes long:
```
[ LEFT MOTOR | RIGHT MOTOR | LEDS     ]
[ 8-bits     | 8-bits      | 8-bits   ]
```

The motor byte consists of 8-bits. Bits 0-6 are for speed with LSB sent first. The last bit is used for direction (Forward: 1, Backward: 0).

```
[ bit-0 | bit-1 | bit-2 | bit-3 | bit-4 | bit-5 | bit-6 |   bit-7   ]
[  LSB  ----------------- SPEED -----------------  MSB  | DIRECTION ]
```

Bit representation is time-modulated (time between edges) as follows:
-------------------------------------------------
TYPE | Ticks		| Interval (msec)
-------------------------------------------------
START|      > 5805 	|          > 0.725625 
    1| 3367 - 5805	| 0.420875 - 0.725625
    0|      < 3367 	|          < 0.420875

where 1 tick represents one period of the microcontroller's clock, which in this case is 1 / 8 MHz. Note that there is a built-in watchdog timer, which needs to be kicked < 500 msec. Otherwise, the motors are automatically turned off.

The following bit representation will be used in this package:
-----------------------
TYPE | Interval (msec)
-----------------------
START| 2.0 
    1| 0.7
    0| 0.2

```

### Convoluted Description
    Given the 8MHz clock of the ATTiny, a pulse (i.e. time between to edges of the MP3 player voltage on the right channel) is considered a RESET, or start of a new 24bit message, if it is longer than 5805 ticks (0.73ms, or 32 samples at 44.1kHz), considered a 1 if it is between 3367 and 5805 ticks, and a 0 if it is below 3367 ticks. Then, the 24 bit message consists of 8bits for the left motor, 8bits for the right motor, and 8 bits for the 8 LEDs. The LSB is sent first. For the motors, bit 0-6 is speed (valid range 0-100), and bit 7 is direction (1 FWD, 0 BWD [this is wrongly labeled in the FW on Bitbucket). For the LEDs, each bit corresponds directly to the LED.


## Reference
- [Firmware](https://github.com/philippReist/dancebots_electronics/blob/master/DancebotsFirmware/src/MP3DanceBot.c)
- Sonic Visualiser to play and visualize waveforms. It can also be used to annotate the music. https://www.sonicvisualiser.org/
