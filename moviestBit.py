from pandas import Series
from numpy import where

# Get the frame rate (first line) and frame sizes / types (second onwards)
with open('frames.csv', 'r') as frameCSV:
    lines = frameCSV.read().split('\n')
    frameRate = round(float(lines[0].strip()))
    frames = [i.strip().split(',') for i in lines[2:-1]]

# If it's an I frame, it will naturally be higher and skew, so get average between previous and next
for i, frame in enumerate(frames):
    if frame[1] == 'I':
        frame[0] = round(float((int(frames[i-1][0]) + int(frames[i+1][0])) / 2))

# Get the highest 1.5s frame size average and return starting second
period = int(frameRate * 1.5)
roll = Series([i[0] for i in frames]).rolling(period).mean()
loudest = where(roll == roll.max())[0][0]
print(round(((loudest - period) / frameRate), 2), end="")