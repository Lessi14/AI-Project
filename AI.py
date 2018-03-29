import argparse
import math
import sys
import time
import copy
import re
from classes.Moves import Moves
from classes.Node import Node
from classes.BoardSetUp import BoardSetUp
from classes import PuzzleGenerator
from queue import PriorityQueue

board = [[], [], []]

# Global variables
MIN_ROW = 0
MAX_ROW = 2
MIN_COLUMN = 0
MAX_COLUMN = 4
numberOfMoves = 0
startTime = 0
endTime = 0
totalTime = 0
TIMEOUT_TIME = 10
finalFileOutput = ""
puzzleConfigFileOutput = ""
boardNumber = 0
#replace user
#outputpath = r"D:\Winter 2018\COMP 472\Project\AI-Project\\"

#the main loop
def gameLoop(boardSetup):
    global numberOfManualMoves, totalTime, numberOfMoves
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
        move = input_to_enum(userInput)

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
            print("Total time spent is " + str(totalTime * 1000) + " milliseconds")

            endgame = input("Do you want to keep playing? (Please type yes, y, no or n.)\n")
            while not endgamecheck(endgame):
                endgame = input("Please insert a valid input.\n")
            numberOfManualMoves = 0
            if endgame == 'no' or endgame == 'n':
                sys.exit()

            counter += 1
            numberOfMoves = 0
            startTime = time.time()

#checks if end game is reached
def endgamecheck(endgameinput):
    if type(endgameinput) != str:
        return False
    if (endgameinput != 'yes' and endgameinput != 'y'
        and endgameinput != 'no' and endgameinput != 'n'):
        print(endgameinput + " is not valid.")
        return False
    return True

#verifies if input is valid
def autocheck(autoinput):
    if type(autoinput) != str:
        return False

    if (autoinput != '1' and autoinput != '2' and autoinput != '3' and autoinput != '4' and autoInput != '5'):
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
def input_to_enum(inputCheck):
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

#makes a move in the board
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

#prints the board
def print_board(boardSetUp):
    print(get_print_board(boardSetUp))

#retrieves the printed board
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

#creates output file

def create_output_file_board_state(fileName):
    global puzzleConfigFileOutput

    if "input" in fileName:
        lastPart = re.search(r'(?<=\\input)\d.txt$', fileName).group(0)
        file = open(outputpath + r"\output\boards" + lastPart[0] + ".txt", "w+")
    else:
        file = open(outputpath + r"\output\boards.txt", "w+")
    file.write(puzzleConfigFileOutput)

#creates end game file
def create_end_game_file(fileName):
    global finalFileOutput, numberOfMoves, totalTime, boardNumber
    if "input" in fileName:
        lastPart = re.search(r'(?<=\\input)\d.txt$', fileName).group(0)
        file = open(outputpath + r"\output\output" + lastPart[0] + ".txt", "w+")
    else:
        file = open(outputpath + r"\output\output.txt", "w+")
    file.write(finalFileOutput)
    file.write(str(numberOfMoves))
    file.write("\nTotal time is " + str(totalTime) + " seconds\n")
    file.write("Average moves: " + str(numberOfMoves / boardNumber))

#retrieves the letter e
def get_e_letter(boardSetUp):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    index = boardSetUp.x + boardSetUp.y * 5
    return letters[index]

#tries to solve the board
def solve_board(boardSetUp, algoChoice):
    global finalFileOutput
    boardStartTime = time.time()
    if algoChoice == '1':
        best_first_search_algorithm(boardSetUp)
    else:
        a_star_search_algorithm(boardSetUp)
    boardEndTime = time.time()
    boardTime = boardEndTime - boardStartTime
    finalFileOutput += str(math.ceil(boardTime * 1000)) + "ms\n"

#search algorithm
def best_first_search_algorithm(boardSetUp):
    global puzzleConfigFileOutput, TIMEOUT_TIME, finalFileOutput
    totalTime = 0
    startTime = time.time()
    heuristic = calculate_h_n_manhattan_distance(boardSetUp.board)
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
            heuristic = calculate_h_n_manhattan_distance(child_board.board)
            move = get_e_letter(child_board)
            new_node = Node(0, heuristic, current.listOfMoves + move, child_board)
            if heuristic == 0:
                print("Solved in " + str(len(new_node.listOfMoves)))
                numberOfMoves = 0
                print_final_board(new_node)
                return
            else:
                open_list.put((new_node.f_n, count, new_node))
                count += 1
                endTime = time.time()
                totalTime += endTime - startTime
                if totalTime >= TIMEOUT_TIME:
                    puzzleConfigFileOutput += "NO SOLUTION TO BOARD"
                    finalFileOutput += "NO SOLUTION TO BOARD\n"
                    print("Board took more than " + str(TIMEOUT_TIME) + " seconds to solve, so it timed out")
                    return
                else:
                    startTime = endTime
    puzzleConfigFileOutput += "NO SOLUTION TO BOARD"

#search algorithm
def a_star_search_algorithm(boardSetUp):
    global puzzleConfigFileOutput, TIMEOUT_TIME, finalFileOutput
    heuristic = calculate_h_n_manhattan_distance(boardSetUp.board)
    totalTime = 0
    startTime = time.time()
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
            heuristic = calculate_h_n_manhattan_distance(child_board.board)
            move = get_e_letter(child_board)
            new_node = Node(current.g_n + 1, heuristic, current.listOfMoves + move, child_board)
            if heuristic == 0:
                print("Solved in " + str(current.g_n + 1))
                print_final_board(new_node)
                return
            else:
                open_list.put((new_node.f_n, count, new_node))
                count += 1
                endTime = time.time()
                totalTime += endTime - startTime
                if totalTime >= TIMEOUT_TIME:
                    puzzleConfigFileOutput += "NO SOLUTION TO BOARD"
                    finalFileOutput += "NO SOLUTION TO BOARD\n"
                    print("Board took more than " + str(TIMEOUT_TIME) + " seconds to solve, so it timed out")
                    return
                else:
                    startTime = endTime
    puzzleConfigFileOutput += "NO SOLUTION TO BOARD"

#prints the final board
def print_final_board(node):
    global finalFileOutput, numberOfMoves, puzzleConfigFileOutput, boardNumber
    numberOfMoves += len(node.listOfMoves)

    finalFileOutput += node.listOfMoves + "\n"

    puzzleConfigFileOutput += "Final configuration\n"
    puzzleConfigFileOutput += get_print_board(node.boardSetUp) + "\n"


#retrieves the position
def get_position(element, array):
    for i in range(len(array)):
        if array[i] == element:
            return i
    return -1

#counts the pieces present in the board
def count_pieces_in_board(board):
    pieces = {}
    # Count how many of each piece we have on the board
    for row in board:
        for letter in row:
            if letter not in pieces:
                pieces[letter] = 0
            pieces[letter] += 1
    return pieces

#tries to predict the final board
def predict_final_board(board):
    pieces = count_pieces_in_board(board)
    winningBoard = copy.deepcopy(board)

    # We make a first pass through the row to look at columns that are already mirrored
    # We don't want to change these rows
    for i in range(0, 5):
        if winningBoard[0][i] == winningBoard[2][i]:
            # pieces[winningBoard[0][1]] -= 2
            pieces[winningBoard[0][i]] -= 2

    allRowsHandled = True
    for i in range(0, 5):
        # If they are equal, we've already taken them into account in the above loop, so skip now
        if winningBoard[0][i] == winningBoard[2][i]:
            continue

        # If either row can be copied, we need to decide which one should be copied
        if pieces[winningBoard[0][i]] >= 2 and pieces[winningBoard[2][i]] >= 2:

            if manhattan_distance(board, winningBoard[0][i], 0, i) <= manhattan_distance(board, winningBoard[2][i], 2, i):
                winningBoard[2][i] = winningBoard[0][i]
                pieces[winningBoard[0][i]] -= 2
            else:
                winningBoard[0][i] = winningBoard[2][i]
                pieces[winningBoard[2][i]] -= 2
        # If this piece in row 1 can be copied to row 3, do that
        elif pieces[winningBoard[0][i]] >= 2:
            winningBoard[2][i] = winningBoard[0][i]
            pieces[winningBoard[0][i]] -= 2
        # Else if piece in row 3 can be copied to row 1, do that
        elif pieces[winningBoard[2][i]] >= 2:
            winningBoard[0][i] = winningBoard[2][i]
            pieces[winningBoard[2][i]] -= 2
        else:
            allRowsHandled = False

    if not allRowsHandled:
        # One final loop through to handle cases where neither the top nor bottom row could be copied
        for i in range(0, 5):
            # Skip all cases we already handled
            if winningBoard[0][i] == winningBoard[2][i]:
                continue
            # If the middle row can be copied, do that
            elif pieces[winningBoard[1][i]] >= 2:
                winningBoard[0][i] = winningBoard[1][i]
                winningBoard[2][i] = winningBoard[1][i]
                pieces[winningBoard[1][i]] -= 2
            # For the others, pick a random piece that has 2 or more of it on the board and place it on both rows
            for piece in pieces:
                if pieces[piece] >= 2:
                    winningBoard[0][i] = piece
                    winningBoard[2][i] = piece
                    pieces[piece] -= 2
    return winningBoard

#calculates h(n) using manhattan distance
def calculate_h_n_manhattan_distance(board):
    # print("------------------------")
    pieces = count_pieces_in_board(board)
    winningBoard = copy.deepcopy(board)
    score = 0
    # winningBoard2 = copy.deepcopy(board)

    allRowsHandled = True
    for i in range(0, 5):
        # If they are equal, we've already taken them into account in the above loop, so skip now
        if winningBoard[0][i] == winningBoard[2][i]:
            pieces[winningBoard[0][i]] -= 2
            continue

        # If this piece in row 1 can be copied to row 3, do that
        if pieces[winningBoard[0][i]] >= 2:
            winningBoard[2][i] = winningBoard[0][i]
            pieces[winningBoard[0][i]] -= 2
            score += manhattan_distance(board, winningBoard[0][i], 0, i)
        # Else if piece in row 3 can be copied to row 1, do that
        elif pieces[winningBoard[2][i]] >= 2:
            winningBoard[0][i] = winningBoard[2][i]
            pieces[winningBoard[2][i]] -= 2
            score += manhattan_distance(board, winningBoard[2][i], 2, i)
        # If either row can be copied, we need to decide which one should be copied
        elif pieces[winningBoard[0][i]] >= 2 and pieces[winningBoard[2][i]] >= 2:
            if manhattan_distance(board, winningBoard[0][i], 0, i) <= manhattan_distance(board,
                                                                                                winningBoard[2][i], 2,
                                                                                                i):
                winningBoard[2][i] = winningBoard[0][i]
                pieces[winningBoard[0][i]] -= 2
                score += manhattan_distance(board, winningBoard[0][i], 0, i)
            else:
                winningBoard[0][i] = winningBoard[2][i]
                pieces[winningBoard[2][i]] -= 2
                score += manhattan_distance(board, winningBoard[2][i], 2, i)
        else:
            # print(str(winningBoard) + "\n")
            # print(str(i) + "\n")
            # print(str(winningBoard2) + "\n")
            allRowsHandled = False

    if not allRowsHandled:
        # One final loop through to handle cases where neither the top nor bottom row could be copied
        for i in range(0, 5):
            # Skip all cases we already handled
            if winningBoard[0][i] == winningBoard[2][i]:
                continue
            # If the middle row can be copied, do that
            elif pieces[winningBoard[1][i]] >= 2:
                winningBoard[0][i] = winningBoard[1][i]
                winningBoard[2][i] = winningBoard[1][i]
                pieces[winningBoard[1][i]] -= 2
                score += manhattan_distance(board, winningBoard[1][i], 2, i)
                score += manhattan_distance(board, winningBoard[1][i], 0, i)
                #score += 2
            # For the others, pick a random piece that has 2 or more of it on the board and place it on both rows
            else:
                for piece in pieces:
                    if pieces[piece] >= 2:
                        winningBoard[0][i] = piece
                        winningBoard[2][i] = piece
                        pieces[piece] -= 2
                        score += manhattan_distance(board, piece, 2, i)
                        score += manhattan_distance(board, piece, 0, i)
                        #score += 2
                        break
    # print("+++++++++++++++++++++++")
    # print(str(winningBoard) + "\n")
    # print(str(winningBoard2) + "\n")
    return score


#calculates manhattan distance
def manhattan_distance(board, letter, row, column):
    closest = 1000

    for j in range(0, 5):
        currentValueRow0 = 10000
        currentValueRow2 = 10000
        currentValueRow1 = 10000
        if column == j:
            currentValueRow1 = column - j + 1
        elif column > j:
            currentValueRow1 = column - j + 1
            if row == 0:
                currentValueRow0 = column - j + 2
                currentValueRow2 = column - j
            else:
                currentValueRow0 = column - j
                currentValueRow2 = column - j + 2
        elif column < j:
            currentValueRow1 = j - column + 1
            if row == 0:
                currentValueRow0 = j - column + 2
                currentValueRow2 = j - column
            else:
                currentValueRow0 = j - column
                currentValueRow2 = j - column + 2
        if board[2][j] == letter and closest > currentValueRow2:
            closest = currentValueRow2
        if board[0][j] == letter and closest > currentValueRow0:
            closest = currentValueRow0
        if board[1][j] == letter and closest > currentValueRow1:
            closest = currentValueRow1
    return closest


#retrieves the representation of the column
def get_string_representation(board):
    string = ""
    for row in board:
        for column in row:
            string += column
    return string

#retrieves the children boards
def get_children_boards(parent):
    children_list = []
    valid_moves = get_valid_moves(parent.boardSetUp)
    for move in valid_moves:
        board = copy.deepcopy(parent.boardSetUp.board)
        boardSetUp = BoardSetUp(parent.boardSetUp.x, parent.boardSetUp.y, board)

        makeMove(move, boardSetUp)
        children_list.append(boardSetUp)
    return children_list

#retrieves valid moves possible
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

#verifies the algorithm chosen
def algoTypeCheck(algoChoice):
    if type(algoChoice) != str:
        return False

    if algoChoice != '1' and algoChoice != '2':
        print(algoChoice + " is not valid.")
        return False
    return True

#Solves the board, measures the time it takes to solve and outputs to a file
def solve_file_problems(filename, algoChoice):
    global startTime, endTime, totalTime, boardNumber, puzzleConfigFileOutput, finalFileOutput, puzzleConfigFileOutput
    global numberOfMoves

    with open(filename) as file:
        startTime = time.time()
        for line in file:
            if 'e' not in line or ('r' not in line and 'b' not in line):
                print("This board is not valid. Board: " + line)
                continue
            boardNumber += 1
            boardSetUp = BoardSetUp.build_board(line)
            puzzleConfigFileOutput += "\nPuzzle " + str(boardNumber) + " initial configuration\n"
            puzzleConfigFileOutput += get_print_board(boardSetUp) + "\n"
            solve_board(boardSetUp, algoChoice)
        endTime = time.time()
        totalTime = endTime - startTime
    create_output_file_board_state(filename)
    create_end_game_file(filename)
    print("The boards have been solved. Please check the the output files.\n")
    finalFileOutput = ""
    puzzleConfigFileOutput = ""
    boardNumber = 0
    numberOfMoves = 0
    totalTime = 0

#Verifies if the choice is valid or not
def diffCheck(diffChoice):
    if type(diffChoice) != str:
        return False

    if diffChoice != '1' and diffChoice != '2' and diffChoice != '2' and diffChoice != '3' and diffChoice != '4' and diffChoice != '5':
        print(diffChoice + " is not valid.")
        return False
    return True


# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--file", help="The file with the candy info", default="")
args = parser.parse_args()

# main loop
while True:
    autoInput = input("1) Automatic mode\n2) Manual mode\n3) Generate puzzle files\n4) Select Difficulty\n5) Exit\n")
    while not autocheck(autoInput):
        autoInput = input("Please insert a valid input.\n")

    if autoInput == '2':
        if args.file is None or args.file == '':
            print('The file does not exist.')
            exit()

        solve_file_problems(outputpath + r"/puzzlefiles/" + args.file)
        path = "//puzzlefiles//" + args.file
        gameLoop(BoardSetUp.getBoardSetup(BoardSetUp, path))
    elif autoInput == '1':

        algoChoice = input("1) best_first_search_algorithm\n2) a_star_search_algorithm\n")
        while not algoTypeCheck(algoChoice):
            algoChoice = input("Please insert a valid input.\n")

        if args.file is None or args.file == '':
            solve_file_problems(outputpath + "\puzzlefiles\input1.txt", algoChoice)
            solve_file_problems(outputpath + "\puzzlefiles\input2.txt", algoChoice)
            solve_file_problems(outputpath + "\puzzlefiles\input3.txt", algoChoice)
            solve_file_problems(outputpath + "\puzzlefiles\input4.txt", algoChoice)
        else:
            solve_file_problems(outputpath + "\puzzlefiles\\" + args.file, algoChoice)
    elif autoInput == '3':
        print(args.file)
        PuzzleGenerator.generate_puzzle_files()
    elif autoInput == '4':
        diffInput = input("Select difficulty.\n1) Novice \n2) Apprentice \n3) Expert \n4) Master \n5) Arg file\n")
        while not diffCheck(diffInput):
            diffInput = input("Please insert a valid input.\n")

        algoChoice = input("1) best_first_search_algorithm\n2) a_star_search_algorithm\n")
        while not algoTypeCheck(algoChoice):
            algoChoice = input("Please insert a valid input.\n")

        if diffInput == '1':
            solve_file_problems(outputpath + r"/puzzlefiles/novice.txt", algoChoice)
        elif diffInput == '2':
            solve_file_problems(outputpath + r"/puzzlefiles/apprentice.txt", algoChoice)
        elif diffInput == '3':
            solve_file_problems(outputpath + r"/puzzlefiles/expert.txt", algoChoice)
        elif diffInput == '4':
            solve_file_problems(outputpath + r"/puzzlefiles/master.txt", algoChoice)
        elif diffInput == '5':
            if args.file is None or args.file == '':
                print('The file does not exist.')
                exit()
            solve_file_problems(outputpath + r"/puzzlefiles/" + args.file, algoChoice)
    else:
        print('Exiting')
        sys.exit()
