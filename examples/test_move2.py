"""Create move test file.

"""
import dancebots as db
from dancebots import Move

DURATION = 10  # [sec]

test = Move()
test.forward(DURATION, 25)

# Build audio file
db.add(test)
db.save("test_move2.wav")
