import argparse
import sys
import time
import math
import copy
import random

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


def gameLoop(boardSetup):
    global numberOfManualMoves,totalTime,numberOfMoves
    counter = 0
    numberOfManualMoves = 0
    startTime = time.time()
    while True:
        if counter >= len(boardSetup):
            print("We are the end of the file.")
            sys.exit()
        print_board(boardSetup[counter])
        # take user input
        userInput = input("What direction should the empty space move.\n")
        while not inputcheck(userInput):
            userInput = input("Please insert a valid input.\n")

        # get Enum version of user input
        move = inputToEnum(userInput)

        # verify move
        if verifyMove(move, boardSetup[counter]):
            print("You moved by " + str(boardSetup[counter].x) + " and " + str(boardSetup[counter].y))
            makeMove(move, boardSetup[counter])
            numberOfManualMoves += 1
        else:
            print("Illegal move! You cannot move " + str(move) + ".")

        if checkWinningCondition(boardSetup[counter].board):
            endTime = time.time()
            totalTime = endTime - startTime
            print_board(boardSetup[counter])
            create_output_file_board_state()
            print("You won")
            print("Total number of moves was " + str(numberOfManualMoves))
            print("Total time spent is " + str(totalTime*1000) + " milliseconds")

            endgame = input("Do you want to keep playing? (Please type yes, y, no or n.)\n")
            while not endgamecheck(endgame):
                endgame = input("Please insert a valid input.\n")
            numberOfManualMoves = 0
            if endgame == 'no' or endgame == 'n':
                sys.exit()

            counter += 1
            numberOfMoves = 0
            startTime = time.time()


def endgamecheck(endgameinput):
    if type(endgameinput) != str:
        return False
    if (endgameinput != 'yes' and endgameinput != 'y'
        and endgameinput != 'no' and endgameinput != 'n'):
        print(endgameinput + " is not valid.")
        return False
    return True


def autocheck(autoinput):
    if type(autoinput) != str:
        return False
    
    if (autoinput != '1' and autoinput != '2' and autoinput != '3' and autoinput != '4'):
        print(autoinput + " is not valid.")
        return False
    return True

# Checks if the user input is valid
def inputcheck(userInputCheck):
    if type(userInputCheck) != str:
        return False
    if (userInputCheck != 'right' and userInputCheck != 'left'
        and userInputCheck != 'up' and userInputCheck != 'down'):
        print(userInputCheck + " is not valid.")
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


def create_output_file_board_state():
    global puzzleConfigFileOutput
    file = open("boards.txt", "w+")
    file.write(puzzleConfigFileOutput)


def create_end_game_file():
    global finalFileOutput, numberOfMoves, totalTime, boardNumber
    file = open("output.txt", "w+")
    file.write(finalFileOutput)
    file.write("\n-----------------------------------------------------------------------\n")
    file.write("All " + str(boardNumber) + " boards solved\n")
    file.write("\nTotal time spent: " + str(totalTime*1000) + " milliseconds")
    file.write("\nTotal moves: " + str(numberOfMoves))


def solve_board(boardSetUp):
    global finalFileOutput
    boardStartTime = time.time()
    a_star_search_algorithm(boardSetUp)
    boardEndTime = time.time()
    boardTime = boardEndTime - boardStartTime
    finalFileOutput += "Board took " + str(boardTime*1000) + " milliseconds to solve\n"


def a_star_search_algorithm(boardSetUp):
    global puzzleConfigFileOutput
    heuristic = calculate_h_n_permutation_inversions(boardSetUp.board)
    start = Node(0, heuristic, "", boardSetUp)
    if heuristic == 0:
        print_final_board(start)
        return
    open_list = PriorityQueue()
    count = 0
    open_list.put((start.f_n, count, start))
    count += 1
    closed_list = {}
    while not open_list.empty():
        current = open_list.get()[2]
        closed_list[get_string_representation(current.boardSetUp.board)] = True
        children_boards = get_children_boards(current)
        for child_board in children_boards:
            board_string = get_string_representation(child_board.board)
            if board_string in closed_list:
                continue
            heuristic = calculate_h_n_permutation_inversions(child_board.board)
            move = get_e_letter(child_board)
            new_node = Node(current.g_n+1, heuristic, current.listOfMoves + move, child_board)
            if heuristic == 0:
                numberOfMoves = 0
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

def calculate_h_n_permutation_inversions(board):
    goal_state = predict_final_board(board)
    goal_reduced = []
    board_reduced = []
    #Add the important 2 rows to a single 1D array
    for i in range(0, 5):
        goal_reduced.append(goal_state[0][i])
        board_reduced.append(board[0][i])
    for i in range(0, 5):
        goal_reduced.append(goal_state[2][i])
        board_reduced.append(board[2][i])
    
    for i in range(len(goal_reduced)):
        goal_reduced[i] = goal_reduced[i] + str(i)
        board_reduced[i] = board_reduced[i] + str(i)
    
    estimation = 0
    if board_reduced[0] != goal_reduced[0]:
        estimation += 1
    for i in range(0, len(goal_reduced)):
        for j in range(i+1, len(goal_reduced)):
            position = get_position(board_reduced[j], goal_reduced)
            #Did not find it in the goal state
            if position < i:
                estimation += 1
            
    return estimation

def get_position(element, array):
    for i in range(len(array)):
        if array[i] == element:
            return i
    return -1

def predict_final_board(board):
    pieces = {}
    #Count how many of each piece we have on the board
    for row in board:
        for letter in row:
            if letter not in pieces:
                pieces[letter] = 0
            pieces[letter] += 1
    winningBoard = copy.deepcopy(board)
    for i in range(0, 5):
        #If this piece in row 1 can be copied to row 3, do that
        if pieces[winningBoard[0][i]] >= 2:
            winningBoard[2][i] = winningBoard[0][i]
            pieces[winningBoard[0][i]] -= 2
        #Else if piece in row 3 can be copied to row 1, do that
        elif pieces[winningBoard[2][i]] >= 2:
            winningBoard[0][i] = winningBoard[2][i]
            pieces[winningBoard[2][i]] -= 2
            #Otherwise, pick a random piece that has 2 or more of it on the board and place it on both rows
            for piece in pieces:
                if pieces[piece] >= 2:
                    winningBoard[0][i] = piece
                    winningBoard[2][i] = piece
                    pieces[piece] -= 2
    return winningBoard

def calculate_h_n(board):
    counter = 0
    for i in range(0, len(board[0])):
       if board[0][i] is not board[2][i]:
            value = min(manhattan_distance(board, board[2][i], 0, i), manhattan_distance(board, board[0][i], 2, i))
            counter += value
            #counter += 1
    return counter

def manhattan_distance(board, letter, row, column):
    if letter == 'e':
        return 1000000
    if row != 2 and board[row+1][column] == letter:
        return 1
    if row != 0 and board[row-1][column] == letter:
        return 1
    if column != 0 and board[row][column-1] == letter:
        return 1
    if column != 4 and board[row][column+1] == letter:
        return 1
    if column != 4 and row != 2 and board[row+1][column+1] == letter:
        return 2
    if column != 0 and row != 0 and board[row-1][column-1] == letter:
        return 2
    if column != 0 and row != 2 and board[row+1][column-1] == letter:
        return 2
    if column != 4 and row != 0 and board[row-1][column+1] == letter:
        return 2
    if column < 3 and board[row][column+2] == letter:
        return 2
    if column > 1 and board[row][column-2] == letter:
        return 2
    return 3

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
    global startTime, endTime, totalTime, boardNumber, puzzleConfigFileOutput, finalFileOutput, puzzleConfigFileOutput
    global numberOfMoves
    with open(filename) as file:
        startTime = time.time()
        for line in file:
            if 'e' not in line or ('r' not in line and 'b' not in line):
                print("This board is not valid. Board: " + line)
                continue
            boardNumber += 1
            boardSetUp = build_board(line)
            puzzleConfigFileOutput += "\nPuzzle " + str(boardNumber) + " initial configuration\n"
            puzzleConfigFileOutput += get_print_board(boardSetUp) + "\n"
            solve_board(boardSetUp)
        endTime = time.time()
        totalTime = endTime - startTime
    create_output_file_board_state()
    create_end_game_file()
    print("The boards have been solved. Please check the the output files.\n")
    finalFileOutput = ""
    puzzleConfigFileOutput = ""
    boardNumber = 0
    numberOfMoves = 0
    totalTime = 0


def getBoardSetup(filename):
    boardsetup = []
    with open(filename) as file:
        for line in file:
            if 'e' not in line or ('r' not in line and 'b' not in line):
                print("This board is not valid. Board: " + line)
                continue
            boardsetup.append(build_board(line))

    return boardsetup

def generatePuzzleFiles(filename):
    difficulty = input("Choose a difficulty\n1) Novice\n2) Apprentice\n3) Expert\n4) Master\n")
    while not (difficulty == '1' or difficulty == '2' or difficulty == '3' or difficulty == '4'):
        difficulty = input("Please insert a valid input.\n")
    if difficulty == '1':
        generateNoviceFile(filename)
    elif difficulty == '2':
        generateApprenticeFile(filename)
    elif difficulty == '3':
        generateExpertFile(filename)
    elif difficulty == '4':
        generateMasterFile(filename)
    sys.exit()

def generateNoviceFile(filename):
    array = ['e', 'r', 'r', 'r', 'r', 'r', 'r', 'b', 'b', 'b', 'b', 'b', 'b', 'w', 'w']
    generateDifficultyFile(filename, array, 50)

def generateApprenticeFile(filename):
    array = ['e', 'r', 'r', 'r', 'r', 'r', 'r', 'b', 'b', 'b', 'b', 'y', 'y', 'w', 'w']
    generateDifficultyFile(filename, array, 50)

def generateExpertFile(filename):
    array = ['e', 'r', 'r', 'r', 'r', 'g', 'g', 'b', 'b', 'b', 'b', 'y', 'y', 'w', 'w']
    generateDifficultyFile(filename, array, 30)

def generateMasterFile(filename):
    array = ['e', 'r', 'r', 'r', 'r', 'g', 'g', 'b', 'b', 'p', 'p', 'y', 'y', 'w', 'w']
    generateDifficultyFile(filename, array, 10)

def generateDifficultyFile(filename, array, numberOfPuzzles):
    text = ""
    for i in range(0, numberOfPuzzles):
        shuffledArray = copy.deepcopy(array)
        random.shuffle(shuffledArray)
        for letter in shuffledArray:
            text += letter + " "
        text = text.rstrip()
        text += '\n'
    text = text.rstrip('\n')
    generatePuzzleFile(filename, text)

def generatePuzzleFile(filename, text):
    file = open(filename, "w")
    file.write(text)

# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--file", help="The file with the candy info", default="")
args = parser.parse_args()


#main loop
while True:
    autoInput = input("1) Automatic mode\n2) Manual mode\n3) Generate puzzle files\n4) Exit\n")
    while not autocheck(autoInput):
        autoInput = input("Please insert a valid input.\n")

    if autoInput == '2':
        gameLoop(getBoardSetup(args.file))
    elif autoInput == '1':
        solve_file_problems(args.file)
    elif autoInput == '3':
        generatePuzzleFiles(args.file)
    else:
        print('Exiting')
        sys.exit()
