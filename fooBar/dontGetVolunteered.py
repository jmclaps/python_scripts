import pandas as pd
import numpy as np
from itertools import product

def getPosition(value,chessBoard):
    
    for row in range(chessBoard.shape[0]):
        for col in range(chessBoard.shape[1]):
            if chessBoard.iloc[row,col] == value:
                pos = (row, col)
                break
    return pos

def getMoves(position):
    x, y = position
    moves = list(product([x-1, x+1],[y-2, y+2])) + list(product([x-2,x+2],[y-1,y+1]))
    moves = [(x,y) for x,y in moves if x >= 0 and y >= 0 and x < 8 and y < 8]
    return moves

def solution(src, dest):
    x = []
    for i in np.arange(1,9,1,int):
        x.append(np.arange((i-1)*8,(i*7)+i,1,int))
    
    chessBoard = pd.DataFrame(x)
    destPos = getPosition(dest,chessBoard)
    srcPos = getPosition(src,chessBoard)
    moves = getMoves(srcPos)
    print(moves == [(1,2)])
    return moves

algo = solution(0,1)
print(algo)
