import argparse
import sys
import time
import math
import copy

board = [[], [], []]

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
finalFileOutput = ""
puzzleConfigFileOutput = ""
boardNumber = 0


def gameLoop():
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
        #print("Illegal move! You cannot move " + str(move) + ".")
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
    boardSetUp.x = currentX
    boardSetUp.y = currentY

    boardSetUp.board[previousY][previousX] = boardSetUp.board[currentY][currentX]
    boardSetUp.board[currentY][currentX] = "e"

# Checks if the grid reaches the winning condition (the goal state)
def checkWinningCondition(board):
    for i in range(0, 5):
        if board[0][i] != board[2][i]:
            return False

    return True


def print_board(boardSetUp):
    print(get_print_board(boardSetUp))

def get_print_board(boardSetUp):
    string = "---------------\n"
    for row in boardSetUp.board:
        line = ""
        for column in row:
            if column is "e":
                boardSetUp.x = row.index(column)
                boardSetUp.y = boardSetUp.board.index(row)
                line = line + "| |"
            else:
                line = line + "|" + column + "|"
        string += line + "\n"
        string += "---------------\n"
    return string

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
    global puzzleConfigFileOutput
    file = open("boards.txt", "w")
    file.write(puzzleConfigFileOutput)


def create_end_game_file():
    global finalFileOutput, numberOfMoves, totalTime, boardNumber
    file = open("output.txt", "w")
    file.write(finalFileOutput)
    file.write("\n-----------------------------------------------------------------------\n")
    file.write("All " + str(boardNumber) + " boards solved\n")
    file.write("\nTotal time spent: " + str(totalTime) + " milliseconds")
    file.write("\nTotal moves: " + str(numberOfMoves))


def solve_board(boardSetUp):
    global finalFileOutput
    boardStartTime = time.time()
    a_star_search_algorithm(boardSetUp)
    boardEndTime = time.time()
    boardTime = boardEndTime - boardStartTime
    finalFileOutput += "Board took " + str(boardTime) + " milliseconds to solve\n"

def a_star_search_algorithm(boardSetUp):
    global puzzleConfigFileOutput
    heuristic = calculate_h_n(boardSetUp.board)
    start = Node(0, heuristic, "", boardSetUp)
    if heuristic == 0:
        print_final_board(start)
        return
    open_list = PriorityQueue()
    count = 0
    open_list.put((start.f_n, count, start))
    count += 1
    closed_list = set()
    while not open_list.empty():
        current = open_list.get()[2]
        closed_list.add(get_string_representation(current.boardSetUp.board))
        children_boards = get_children_boards(current)
        for child_board in children_boards:
            board_string = get_string_representation(child_board.board)
            if board_string in closed_list:
                continue
            heuristic = calculate_h_n(child_board.board)
            move = get_e_letter(child_board)
            new_node = Node(current.g_n+1, heuristic, current.listOfMoves + move, child_board)
            if heuristic == 0:
                print_final_board(new_node)
                return
            else:
                open_list.put((new_node.f_n, count, new_node))
                count += 1
    puzzleConfigFileOutput += "NO SOLUTION TO BOARD"

def get_e_letter(boardSetUp):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    index = boardSetUp.x + boardSetUp.y*5
    return letters[index]

def print_final_board(node):
    global finalFileOutput, numberOfMoves, puzzleConfigFileOutput, boardNumber
    numberOfMoves += node.g_n
    
    finalFileOutput += "\nSolved board " + str(boardNumber) + " in " + str(node.g_n) + " moves!\n"
    finalFileOutput += node.listOfMoves+"\n"
    
    puzzleConfigFileOutput += "Final configuration\n"
    puzzleConfigFileOutput += get_print_board(node.boardSetUp) + "\n"

def calculate_h_n(board):
    counter = 0
    for column in board[0]:
       if column is not board[2][board[0].index(column)]:
            counter += 1
    return counter

def get_string_representation(board):
    string = ""
    for row in board:
        for column in row:
            string += column
    return string

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
    if verifyMove(Moves.Up, boardSetUp):
        valid_moves.append(Moves.Up)
    if verifyMove(Moves.Down, boardSetUp):
        valid_moves.append(Moves.Down)
    if verifyMove(Moves.Right, boardSetUp):
        valid_moves.append(Moves.Right)
    if verifyMove(Moves.Left, boardSetUp):
        valid_moves.append(Moves.Left)
    return valid_moves

def solve_file_problems(filename):
    global startTime, endTime, totalTime, boardNumber, puzzleConfigFileOutput
    with open(filename) as file:
        startTime = time.time()
        for line in file:
            boardNumber += 1
            boardSetUp = build_board(line)
            puzzleConfigFileOutput += "\nPuzzle " + str(boardNumber) + " initial configuration\n"
            puzzleConfigFileOutput += get_print_board(boardSetUp) + "\n"
            solve_board(boardSetUp)
        endTime = time.time()
        totalTime = endTime - startTime
    create_output_file_board_state()
    create_end_game_file()


# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--file", help="The file with the candy info", default="")
parser.add_argument("--int", help="example int arg", type=int, default=1)
args = parser.parse_args()

solve_file_problems(args.file)
