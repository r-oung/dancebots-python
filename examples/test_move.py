"""Create move test file.

"""
import dancebots as db
from dancebots import Move

DURATION = 2  # [sec]

# Test speed
test1 = Move()
test1.forward(DURATION, 25)
test1.forward(DURATION, 50)
test1.forward(DURATION, 75)
test1.forward(DURATION, 100)

# Test direction
test2 = Move()
test2.backward(DURATION)
test2.left(DURATION)
test2.right(DURATION)
test2.forward(DURATION)

# Build audio file
db.add(test1)
db.add(test2)
db.save("test_move.wav")
