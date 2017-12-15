# Joe Gao
# Mandelbrot snowflake
# Web Interpreter - altered 

from turtle import *
import numpy

# setup turtle
pd()
ht()

# for larger image, change vales
width, height = 240, 240
halfW, halfH = int(width / 2), int(height / 2)

offsetConst = (width + height) / 7.68

# default 480 x 480 values = 720 x 720 canvas
bgcolor(2, 8, 15)

# initialize empty graph
origCopy = [[0 for x in range(width)] for y in range(height)]


# iterative function
def z(a, b, ca, cb):
    real = a * a - b * b + ca
    imag = 2 * a * b + cb
    return real, imag


# maps a value between new range
def mapVal(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2


# draws mandelbrot set
def createGrid():
    for x in range(-halfW, halfW):
        for y in range(-halfH, halfH):
            a = mapVal(x, -180, 180, -1.5, 1.5)
            b = mapVal(y, -180, 180, -1.5, 1.5)
            aConst, bConst, val, valid = a, b, 0, True

            for i in range(100):
                a, b = z(a, b, aConst, bConst)

                # diverging towards infinity
                if abs(a + b) > 16:
                    val = int(mapVal(i, 0, 100, 0, 255))
                    valid = False
                    break

            # ignore lower range values
            if val > 0 and val < 15:
                val = -2

            origCopy[x][y] = val


# for alt rpb value mapping for cleaner code
def mapAlt(val, targMax):
    return mapVal(val, 0, 255, 0, targMax)


# disable animation to increase speed
speed(0)

# draw grid and store as original deep copy
createGrid()

# clone and transform graph sets to form snowflake
for i in range(4):
    startY, finishY, prevVal = -9999, -9999, -1
    xOffset, yOffset = 0, 0

    # rotate 2d array copy
    gridCopy = numpy.rot90(origCopy, i)

    # fixed origin point
    if (i + 1) % 2 == 0:
        yOffset = i == 1 and -offsetConst or offsetConst
    else:
        xOffset = i == 0 and -offsetConst or offsetConst

    for x in range(-halfW, halfW):
        for y in range(-halfH, halfH):
            val = gridCopy[x][y]
            xp, yp = x + xOffset, y + yOffset
            if i == 3 and xp == 0 and yp > 125:
                pencolor(0, 0, 0)
                pd()
                setpos(xp, yp)
            else:
                # increase efficiency to reduce drawing time
                if val != prevVal or prevVal == -1:
                    if prevVal == -1 or prevVal == -2:
                        pencolor()
                    else:
                        pencolor(int(mapAlt(prevVal, 30)), int(mapAlt(prevVal, 136)), int(prevVal))

                    pd()
                    setpos(xp, yp - 1)

                    if val == -2:
                        pencolor()
                    else:
                        pencolor(int(mapAlt(val, 30)), int(mapAlt(val, 136)), int(val))

                    setpos(xp, yp)
                    prevVal = int(val)

                if y - yOffset + 1 == halfH:
                    setpos(xp, yp)

        # new line so let go of pen to switch
        pu()
        setpos(x + 1, -halfH)
        pd()

update()

# keep screen opened
print("done")
mainloop()
