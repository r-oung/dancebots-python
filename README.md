[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Dancebots Python
A Python 3 package for [DanceBots](https://www.dancebots.ch/).

## Example
```python
import dancebots as db
from dancebots import Move

# Move the robot
move = Move()
move.forward(3) # move forward for 3 beats
move.backward(3)  # move backward for 3 beats
move.left(2)  # turn left for 2 beats
move.right(2)  # turn right for 2 beats

# Print to sequence of moves
print(move)

# Build audio file
db.add(move)  # add move
db.save("01_sample.wav")  # save to disk
db.plot()  # visualize the audio file
```

## Dependencies
This package relies on the packages listed in `requirements.txt`.

## Virtual Environments
It is recommended to use a Python virtual environment when working with dependencies. A `setup.sh` script is provided in the root directory that will automatically create a virtual environment and install all necessary dependencies (Linux and macOS only):
```
cd dancebots-python/
./setup.sh
```

Activate the virtual environment:
```
source venv/bin/activate
```

## Protocol Description
A frame is the smallest unit in the Dancebot protocol. It contains all of the information necessary to drive the motors and LEDs. It consists of 24-bits:
```
[ LEFT MOTOR | RIGHT MOTOR | LEDS     ]
[ 8-bits     | 8-bits      | 8-bits   ]
```

Frames are concatenated one after another, separated by a delimiter block, to form a bitstream.

Bit representation is time-modulated (time between rising/falling edges) as follows:
| Type      | Ticks       | Interval (msec)     |
|-----------|-------------|---------------------|
| DELIMITER |      > 5805 |          > 0.725625 |
|     1     | 3367 - 5805 | 0.420875 - 0.725625 |
|     0     |      < 3367 |          < 0.420875 |

where 1 tick represents one period of the microcontroller's clock, which in this case is 1/(8 MHz). Note that there is a built-in watchdog timer that needs to be kicked every < 500 msec. Otherwise the motors will automatically turn off.

The following bit representation will be used in this package:
| TYPE      | Interval (msec) |
|-----------|-----------------|
| DELIMITER |       2.0       |
|     1     |       0.7       |
|     0     |       0.2       |

In the datagram illustration above, the motor byte consists of 8-bits:
- Bits 0-6 are for speed with LSB sent first
- The last bit is used for direction:
  - Forward: 1
  - Backward: 0

```
[ bit-0 | bit-1 | bit-2 | bit-3 | bit-4 | bit-5 | bit-6 |   bit-7   ]
[  LSB  ----------------- SPEED -----------------  MSB  | DIRECTION ]
```

#### A Convoluted Description
    Given the 8MHz clock of the ATTiny, a pulse (i.e. time between to edges of the MP3 player voltage on the right channel) is considered a RESET, or start of a new 24bit message, if it is longer than 5805 ticks (0.73ms, or 32 samples at 44.1kHz), considered a 1 if it is between 3367 and 5805 ticks, and a 0 if it is below 3367 ticks. Then, the 24 bit message consists of 8bits for the left motor, 8bits for the right motor, and 8 bits for the 8 LEDs. The LSB is sent first. For the motors, bit 0-6 is speed (valid range 0-100), and bit 7 is direction (1 FWD, 0 BWD [this is wrongly labeled in the FW on Bitbucket). For the LEDs, each bit corresponds directly to the LED.


## Contributions
- [Black](https://google.github.io/styleguide/pyguide.html)
- [Pylint](https://pylint.org/)

## Unit Testing
```
cd tests/
python -m unittest
```

## Reference
- [Firmware](https://github.com/philippReist/dancebots_electronics/blob/master/DancebotsFirmware/src/MP3DanceBot.c)
