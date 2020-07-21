import math

def area (unitMeasure):
    squares = []
    rest = unitMeasure
    
    while rest > 0:
        side = int(math.sqrt(rest))
        square = int(math.pow(side,2))
        squares.append(square)
        rest = rest-square

    return squares

sq_yds = 15324

print(area(sq_yds))