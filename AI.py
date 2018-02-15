import argparse
import sys

board = [[], [], []]
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

from enum import Enum


class Moves(Enum):
    Up = "Up",
    Down = "Down",
    Left = "Left",
    Right = "Right",


# Global variables
MIN_ROW = 0
MAX_ROW = 2
MIN_COLUMN = 0
MAX_COLUMN = 4
x = 0
y = 0


def gameLoop():
    # Main game loop

    while True:
        print_board()
        # take user input
        userInput = input("What direction should the empty space move.")
        while not inputCheck(userInput):
            userInput = input("Please insert a valid input")
            break

        # get Enum version of user input
        move = inputToEnum(userInput)

        # verify move
        if (verifyMove(move)):
            print("You moved by " + str(x) + " and " + str(y))

        if (checkWinningCondition(board)):
            print("You won")
            # Exitprogram
            sys.exit()


# Checks if the user input is valid
def inputCheck(userInputCheck):

    if (type(userInputCheck) != str):
        return False
    if (len(userInputCheck.split()) > 1):
        return False
    if (userInputCheck == 'right' and userInputCheck == 'left'
        and userInputCheck == 'up' and userInputCheck == 'down'):
            print(userInputCheck)
            print("not valid")
            return False
    return True

# Transforms the string input into the Enums used locally
def inputToEnum(inputCheck):

    if (inputCheck.lower() == "right"):
        return Moves.Right
    if (inputCheck.lower() == "up"):
        return Moves.Up
    if (inputCheck.lower() == "left"):
        return Moves.Left
    if (inputCheck.lower() == "down"):
        return Moves.Down


# Verifies if the move is along the grid
def verifyMove(move):
    global MAX_ROW, MIN_ROW, MAX_COLUMN, MIN_COLUMN, x, y, board
    tempy = y
    tempx = x

    if (move == Moves.Up):
        tempy = tempy - 1
    elif (move == Moves.Down):
        tempy = tempy + 1
    elif (move == Moves.Left):
        tempx = tempx - 1
    else:
        tempx = tempx + 1

    if tempy > MAX_ROW or tempy < MIN_ROW or tempx > MAX_COLUMN or tempx < MIN_COLUMN:
        print("Illegal move! You cannot move " + str(move))
        return False
    
    previousX = x
    previousY = y
    x = tempx
    y = tempy
    
    board[previousY][previousX] = board[y][x]
    board[y][x] = "e"
    
    return True


# Checks if the grid reaches the winning condition (the goal state)
def checkWinningCondition(board):
    for i in range(0, 5):
        if board[0][i] != board[2][i]:
            return False

    return True


def print_board():
    global board
    print("---------------")
    for row in board:
        line = ""
        for column in row:
            if column is "e":
                line = line + "| |"
            else:
                line = line + "|" + column + "|"
        print(line)
        print("---------------")


def build_board(line):
    global board
    candies = line.split()
    if len(candies) < 15:
        print("Error parsing line " + line)
        print("Found only " + str(len(candies)) + " candies")
        return
    board = [[candies[0], candies[1], candies[2], candies[3], candies[4]],
             [candies[5], candies[6], candies[7], candies[8], candies[9]],
             [candies[10], candies[11], candies[12], candies[13], candies[14]]]
    gameLoop()


def solve_board():
    global board
    print("Start solving the board here")


def solve_file_problems(filename):
    with open(filename) as file:
        for line in file:
            build_board(line)
            print("Initial configuration")
            print_board()
            solve_board()
            print("Board solved!\n")


# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--file", help="The file with the candy info", default="")
parser.add_argument("--int", help="example int arg", type=int, default=1)
args = parser.parse_args()

solve_file_problems(args.file)
