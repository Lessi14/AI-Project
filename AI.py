import argparse
import sys
import time
import math
import copy

board = [[], [], []]
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

from enum import Enum
from queue import PriorityQueue


class Moves(Enum):
    Up = "up",
    Down = "down",
    Left = "left",
    Right = "right",

    def __str__(self):
        return '%s' % self._value_

class Node():
    def __init__(self, g_n, h_n, listOfMoves, boardSetUp):
       self.g_n = g_n
       self.h_n = h_n
       self.f_n = self.g_n + self.h_n
       self.listOfMoves = copy.deepcopy(listOfMoves)
       self.boardSetUp = boardSetUp

class BoardSetUp():
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.board = board

# Global variables
MIN_ROW = 0
MAX_ROW = 2
MIN_COLUMN = 0
MAX_COLUMN = 4
numberOfMoves = 0
startTime = 0
endTime = 0
totalTime = 0


def gameLoop():
    global startTime, endTime
    startTime = time.time()
    # Main game loop
    while True:
        print_board()
        create_output_file_board_state()
        # take user input
        userInput = input("What direction should the empty space move.")
        while not inputCheck(userInput):
            userInput = input("Please insert a valid input")

        # get Enum version of user input
        move = inputToEnum(userInput)

        # verify move
        if verifyMove(move):
            print("You moved by " + str(x) + " and " + str(y))
            makeMove(move)
            numberOfMoves += 1

        if checkWinningCondition(board):
            endTime = time.time()
            totalTime = math.ceil(endTime - startTime)
            print_board()
            create_output_file_board_state()
            print("You won")
            print("Total number of moves was " + str(numberOfMoves))
            print("Total time spent is " + str(totalTime) + " seconds")
            create_end_game_file(1, totalTime, numberOfMoves)
            # Exitprogram
            sys.exit()


# Checks if the user input is valid
def inputCheck(userInputCheck):
    if type(userInputCheck) != str:
        return False
    if (userInputCheck != 'right' and userInputCheck != 'left'
        and userInputCheck != 'up' and userInputCheck != 'down'):
        print(userInputCheck)
        print("not valid")
        return False
    return True


# Transforms the string input into the Enums used locally
def inputToEnum(inputCheck):
    if inputCheck.lower() == "right":
        return Moves.Right
    if inputCheck.lower() == "up":
        return Moves.Up
    if inputCheck.lower() == "left":
        return Moves.Left
    if inputCheck.lower() == "down":
        return Moves.Down


# Verifies if the move is along the grid
def verifyMove(move, boardSetUp):
    global MAX_ROW, MIN_ROW, MAX_COLUMN, MIN_COLUMN
    tempy = boardSetUp.y
    tempx = boardSetUp.x

    if move == Moves.Up:
        tempy = tempy - 1
    elif move == Moves.Down:
        tempy = tempy + 1
    elif move == Moves.Left:
        tempx = tempx - 1
    else:
        tempx = tempx + 1

    if tempy > MAX_ROW or tempy < MIN_ROW or tempx > MAX_COLUMN or tempx < MIN_COLUMN:
        print("Illegal move! You cannot move " + str(move) + ".")
        return False
        
    return True

def makeMove(move, boardSetUp):
    tempy = boardSetUp.y
    tempx = boardSetUp.x

    if move == Moves.Up:
        tempy = tempy - 1
    elif move == Moves.Down:
        tempy = tempy + 1
    elif move == Moves.Left:
        tempx = tempx - 1
    else:
        tempx = tempx + 1

    previousX = boardSetUp.x
    previousY = boardSetUp.y
    currentX = tempx
    currentY = tempy

    boardSetUp.board[previousY][previousX] = boardSetUp.board[currentY][currentX]
    boardSetUp.board[currentY][currentX] = "e"

# Checks if the grid reaches the winning condition (the goal state)
def checkWinningCondition(board):
    for i in range(0, 5):
        if board[0][i] != board[2][i]:
            return False

    return True


def print_board(boardSetUp):
    print("---------------")
    for row in boardSetUp.board:
        line = ""
        for column in row:
            if column is "e":
                boardSetUp.x = row.index(column)
                boardSetUp.y = boardSetUp.board.index(row)
                line = line + "| |"
            else:
                line = line + "|" + column + "|"
        print(line)
        print("---------------")


def build_board(line):
    candies = line.split()
    if len(candies) < 15:
        print("Error parsing line " + line)
        print("Found only " + str(len(candies)) + " candies")
        return
    board = [[candies[0], candies[1], candies[2], candies[3], candies[4]],
             [candies[5], candies[6], candies[7], candies[8], candies[9]],
             [candies[10], candies[11], candies[12], candies[13], candies[14]]]
    boardSetUp = BoardSetUp(0, 0, board)
    return boardSetUp
    #gameLoop()


def create_output_file_board_state():
    file = open("output.txt", "a")
    global board
    file.write("\nNUMBER OF MOVES " + str(numberOfMoves) + "\n")
    file.write("---------------")
    for row in board:
        line = ""
        for column in row:
            if column is "e":
                line = line + "| |"
            else:
                line = line + "|" + column + "|"
        file.write("\n" + line)
        file.write("\n---------------")


def create_end_game_file(gamenumber, timespent, totalmoves):
    file = open("output.txt", "a")
    file.write("\nGame: " + str(gamenumber))
    file.write("\nTime spent: " + str(timespent) + " seconds")
    file.write("\nTotal moves: " + str(totalmoves))


def solve_board(boardSetUp):
    print("Start solving the board here")
    a_star_search_algorithm(boardSetUp)

def a_star_search_algorithm(boardSetUp):
    start = Node(0, calculate_h_n(boardSetUp.board), numberOfMoves, boardSetUp)
    open_list = PriorityQueue()
    count = 0
    open_list.put((start.f_n, count, start))
    count += 1
    closed_list = set()
    while (not open_list.empty()):
        current = open_list.get()[2]
        closed_list.add(get_string_representation(current.boardSetUp.board))
        children_boards = get_children_boards(current)
        for child_board in children_boards:
            board_string = get_string_representation(child_board.board)
            if board_string in closed_list:
                continue
            heuristic = calculate_h_n(child_board.board)
            new_node = Node(current.f_n, heuristic, current.listOfMoves, child_board)
            if heuristic == 0:
                print("0 heuristic")
                print_final_board(new_node)
                break
            else:
                print(new_node.f_n)
                open_list.put((new_node.f_n, count, new_node))
                count += 1
    print("Done looking through list")

def print_final_board(node):
    print("Solved board!\n")
    print_board(node.boardSetUp.board)
    print(node.listOfMoves+"\n")

def calculate_h_n(board):
    counter = 0
    for column in board[0]:
       if column is not board[2][board[0].index(column)]:
            print(column + " " + board[2][board[0].index(column)])
            counter += 1
    return counter

def get_string_representation(board):
    string = ""
    for row in board:
        for column in row:
            string += column
    return string

##NOT DONE BUT YOU NEED TO ADD ALL CHILDREN THAT ACTUALLY CAN MAKE THE MOVE
'''1) get current
2) add current to closed list
3) get children
4) for each child check that it's not already in closed list
5) get heuristic
6) if heuristic is 0, finish because we have a winning board
7) else, add to open list(edited)'''
def get_children_boards(parent):
    children_list = []
    valid_moves = get_valid_moves(parent.boardSetUp)
    for move in valid_moves:
        board = copy.deepcopy(parent.boardSetUp.board)
        boardSetUp = BoardSetUp(parent.boardSetUp.x, parent.boardSetUp.y, board)
        
        makeMove(move, boardSetUp)
        children_list.append(boardSetUp)
    return children_list

def get_valid_moves(boardSetUp):
    valid_moves = []
    if verifyMove("up", boardSetUp):
        valid_moves.append("up")
    if verifyMove("down", boardSetUp):
        valid_moves.append("down")
    if verifyMove("right", boardSetUp):
        valid_moves.append("right")
    if verifyMove("left", boardSetUp):
        valid_moves.append("left")
    return valid_moves

def solve_file_problems(filename):
    with open(filename) as file:
        for line in file:
            boardSetUp = build_board(line)
            print("Initial configuration")
            print_board(boardSetUp)
            solve_board(boardSetUp)


# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--file", help="The file with the candy info", default="")
parser.add_argument("--int", help="example int arg", type=int, default=1)
args = parser.parse_args()

solve_file_problems(args.file)
