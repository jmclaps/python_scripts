import pandas as pd
import numpy as np
from itertools import product

def getPosition(values,chessBoard):
    pos = []
    for value in values:
        for row in range(chessBoard.shape[0]):
            for col in range(chessBoard.shape[1]):
                if chessBoard.iloc[row,col] == value:
                    pos = pos + [[row, col]]
                    break
            # encontrar la manera de que corte antes
            if len(pos) == len(values):
                break
    return pos

def getMoves(position,chessBoard):
    coordinates = getPosition(position,chessBoard)
    # este for no acumula los moves
    allMoves = []
    for coordinate in coordinates:
        x, y = coordinate
        moves = list(product([x-1, x+1],[y-2, y+2])) + list(product([x-2,x+2],[y-1,y+1]))
        moves = [(x,y) for x,y in moves if x >= 0 and y >= 0 and x < 8 and y < 8]
        allMoves.extend(moves)
    
    valuesReturn = []
    for move in allMoves:
        valueReturn = chessBoard.iloc[move]
        valuesReturn.append(valueReturn)
    return valuesReturn

def solution(src, dest):

    x = []
    for i in np.arange(1,9,1,int):
        x.append(np.arange((i-1)*8,(i*7)+i,1,int))
    
    chessBoard = pd.DataFrame(x)

    solutions = [[src]]
    response = []

    while True:
        nextMoves = getMoves(solutions[-1],chessBoard)

        solutions.append(nextMoves)

        response = [len(solutions) for i in solutions if dest in i]
        if response != []:
            break

    return (response[0]-1)


def getMoves(from: (int, int), to: (int, int), moves: [[(int, int)]]) -> [[(int, int)]]
  if (from == to)
    return moves
  else
    val validMoves = getValidMoves(from, moves)
    return validMoves.map(move => getMoves(move, to, addMovement(from, moves)))


# main
val posibleSolutions = getMoves((0,1), (4,5), [[]])

if (posibleSolutions.length == 0)
  print("No solutions")
else
  val solution = posibleSolutions.sortBy((s1, s2) => s1.length < s2.length).head
  print("Solution: ${solution}")