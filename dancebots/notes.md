Music
- input: music
- output: length, beats

Dance
  loop(end)
    loop(3)
      move.forward(3)
      turn.right(3)
      wait(3) 
      
    loop(4)
      move.backward(3)
  

Lights
   loop(30)
    blink([1,3,5], every 3 beats, 30 times)
    blink([2,4,6,7] every 3 beats, 30 times)
    loop(5)
      blink([1], every 1 beat, 1 time)
