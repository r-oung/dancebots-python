"""Create light test.

"""
import dancebots as db
from dancebots import Light

# Test each LED
test1 = Light()
test1.hold([1, 0, 0, 0, 0, 0, 0, 0], 1)
test1.hold([0, 1, 0, 0, 0, 0, 0, 0], 1)
test1.hold([0, 0, 1, 0, 0, 0, 0, 0], 1)
test1.hold([0, 0, 0, 1, 0, 0, 0, 0], 1)
test1.hold([0, 0, 0, 0, 1, 0, 0, 0], 1)
test1.hold([0, 0, 0, 0, 0, 1, 0, 0], 1)
test1.hold([0, 0, 0, 0, 0, 0, 1, 0], 1)
test1.hold([0, 0, 0, 0, 0, 0, 0, 1], 1)

# Test blinking
DURATION = 5 # [sec]
test2 = Light()
test2.blink([1] * 8, DURATION, 1)
test2.blink([1] * 8, DURATION, 2)
test2.blink([1] * 8, DURATION, 5)
test2.blink([1] * 8, DURATION, 10)

# Build audio file
db.add(test1)
db.add(test2)
db.save("test_light.wav")
