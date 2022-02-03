[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Dancebots Python
A Python 3 package for [Dancebots](https://www.dancebots.ch/) 🕺💃🤖.🎉✨


## Installation
```shell
git clone https://github.com/r-oung/dancebots-python.git
pip install -e dancebots-python/
```

To build from source:
```shell
python setup.py build
python setup.py install
```

### Dependencies
The package uses [librosa](https://github.com/librosa/librosa) for reading MP3 files and beat detection, which means:
- If you don't plan to synchronize your compositions with music, then there shouldn't be any problem. 
- If you are going to synchronize your composition with music, then you'll need to install [ffmpeg](https://www.ffmpeg.org/) or [gstreamer](https://gstreamer.freedesktop.org/). Refer to [this link](https://github.com/librosa/librosa#hints-for-the-installation) for installation hints.


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

More examples can be found in the `examples` folder.


## Protocol Description
A frame is the smallest unit in the Dancebot protocol. It contains all of the information necessary to drive the motors and LEDs. It consists of 3 bytes (or 24-bits):
```
[ -------------- FRAME -------------- ]
[ LEFT MOTOR | RIGHT MOTOR | LEDS     ]
[ 8-bits     | 8-bits      | 8-bits   ]
```

Each motor byte consists of 8-bits:
```
[ bit-0 | bit-1 | bit-2 | bit-3 | bit-4 | bit-5 | bit-6 |   bit-7   ]
[  LSB  ----------------- SPEED -----------------  MSB  | DIRECTION ]
```

Bits 0-6 are for speed with LSB sent first; only decimal values of 0 to 100 are valid. The last bit is used for direction:
  - Forward: 1
  - Backward: 0

Frames are concatenated one after another, separated by a delimiter block, to form a bitstream.
```
[ FRAME ][ DELIMITER ][ FRAME ][ DELIMITER ] ... [ FRAME ][ DELIMITER ]
```

Bit representation is time-modulated (time between rising/falling edges) as follows:
| Type      | Ticks       | Interval (msec)     |
|-----------|-------------|---------------------|
| DELIMITER |      > 5805 |          > 0.725625 |
|     1     | 3367 - 5805 | 0.420875 - 0.725625 |
|     0     |      < 3367 |          < 0.420875 |

where 1 tick represents one period of the microcontroller's clock, which in this case is 1/(8 MHz). Note that there is a built-in watchdog timer that needs to be kicked every < 500 milliseconds, otherwise the motors will automatically turn off.

The following bit representation is used in this package:
| TYPE      | Interval (msec) |
|-----------|-----------------|
| DELIMITER |       2.0       |
|     1     |       0.6       |
|     0     |       0.2       |


## Contributions
The following (default configurations) are used:
- [Black](https://github.com/psf/black)
- [Pylint](https://pylint.org/)

[Semantic versioning](https://semver.org/) is used.


### Unit Tests
```shell
cd tests/
python -m unittest
```
