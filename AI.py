import argparse
import math
import sys
import time
import copy
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
finalFileOutput = ""
puzzleConfigFileOutput = ""
boardNumber = 0


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


def create_output_file_board_state():
    global puzzleConfigFileOutput
    file = open("output/boards.txt", "w+")
    file.write(puzzleConfigFileOutput)


def create_end_game_file():
    global finalFileOutput, numberOfMoves, totalTime, boardNumber
    file = open("output/output.txt", "w+")
    file.write(finalFileOutput)
    file.write(str(numberOfMoves))
    file.write("\nTotal time is " + str(totalTime) + " seconds\n")
    file.write("Average moves: " + str(numberOfMoves / boardNumber))


def get_e_letter(boardSetUp):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    index = boardSetUp.x + boardSetUp.y * 5
    return letters[index]


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


def best_first_search_algorithm(boardSetUp):
    global puzzleConfigFileOutput
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
    puzzleConfigFileOutput += "NO SOLUTION TO BOARD"


def iterative_best_first_search_algorithm(boardSetUp):
    global puzzleConfigFileOutput
    move_cutoff = 20
    while True:
        move_cutoff += 10
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
            if len(current.listOfMoves) + 1 <= move_cutoff:
                closed_list[get_string_representation(current.boardSetUp.board)] = True
                children_boards = get_children_boards(current)
                for child_board in children_boards:
                    board_string = get_string_representation(child_board.board)
                    if board_string in closed_list:
                        continue
                    heuristic = calculate_h_n_permutation_inversions(child_board.board)
                    move = get_e_letter(child_board)
                    new_node = Node(0, heuristic, current.listOfMoves + move, child_board)
                    if heuristic == 0:
                        print("Solved in " + str(len(new_node.listOfMoves)))
                        print("Move cutoff " + str(move_cutoff))
                        numberOfMoves = 0
                        print_final_board(new_node)
                        return
                    else:
                        open_list.put((new_node.f_n, count, new_node))
                        count += 1
    puzzleConfigFileOutput += "NO SOLUTION TO BOARD"


def iterative_best_first_search_backup_list_algorithm(boardSetUp):
    global puzzleConfigFileOutput
    move_cutoff = 0
    cost_cutoff = 0
    heuristic = calculate_h_n_permutation_inversions(boardSetUp.board)
    start = Node(0, heuristic, "", boardSetUp)
    if heuristic == 0:
        print_final_board(start)
        return
    larger_open_list = PriorityQueue()
    count = 0
    larger_open_list.put((start.f_n, count, start))
    count += 1
    while True:
        move_cutoff += 7
        cost_cutoff += 3
        open_list = larger_open_list
        larger_open_list = PriorityQueue()
        closed_list = {}
        while not open_list.empty():
            current = open_list.get()[2]
            if len(current.listOfMoves) + 1 > move_cutoff or current.f_n > cost_cutoff:
                larger_open_list.put((current.f_n, count, current))
                count += 1
                continue
            closed_list[get_string_representation(current.boardSetUp.board)] = True
            children_boards = get_children_boards(current)
            for child_board in children_boards:
                board_string = get_string_representation(child_board.board)
                if board_string in closed_list:
                    continue
                heuristic = calculate_h_n_permutation_inversions(child_board.board)
                move = get_e_letter(child_board)
                new_node = Node(0, heuristic, current.listOfMoves + move, child_board)
                if len(new_node.listOfMoves) + 1 <= move_cutoff and new_node.f_n <= cost_cutoff:
                    if heuristic == 0:
                        print("Solved in " + str(len(new_node.listOfMoves)))
                        print("Move cutoff " + str(move_cutoff))
                        print("Cost cutoff " + str(cost_cutoff))
                        numberOfMoves = 0
                        print_final_board(new_node)
                        return
                    else:
                        open_list.put((new_node.f_n, count, new_node))
                        count += 1
                else:
                    larger_open_list.put((new_node.f_n, count, new_node))
                    count += 1
    puzzleConfigFileOutput += "NO SOLUTION TO BOARD"


def ida_star_search_algorithm(boardSetUp):
    global puzzleConfigFileOutput
    cost_cutoff = 20
    while True:
        cost_cutoff += 10
        heuristic = calculate_h_n_permutation_inversions(boardSetUp.board)
        start = Node(0, heuristic, "", boardSetUp)
        while heuristic >= cost_cutoff:
            cost_cutoff += 10
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
                if heuristic + current.g_n + 1 <= cost_cutoff:
                    move = get_e_letter(child_board)
                    new_node = Node(current.g_n + 1, heuristic, current.listOfMoves + move, child_board)
                    if heuristic == 0:
                        print("Solved in " + str(current.g_n + 1))
                        print("Cost cutoff " + str(cost_cutoff))
                        print_final_board(new_node)
                        return
                    else:
                        open_list.put((new_node.f_n, count, new_node))
                        count += 1
    puzzleConfigFileOutput += "NO SOLUTION TO BOARD"


def a_star_search_algorithm(boardSetUp):
    global puzzleConfigFileOutput
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
            new_node = Node(current.g_n + 1, heuristic, current.listOfMoves + move, child_board)
            if heuristic == 0:
                print("Solved in " + str(current.g_n + 1))
                print_final_board(new_node)
                return
            else:
                open_list.put((new_node.f_n, count, new_node))
                count += 1
    puzzleConfigFileOutput += "NO SOLUTION TO BOARD"


def print_final_board(node):
    global finalFileOutput, numberOfMoves, puzzleConfigFileOutput, boardNumber
    numberOfMoves += len(node.listOfMoves)

    finalFileOutput += node.listOfMoves + "\n"

    puzzleConfigFileOutput += "Final configuration\n"
    puzzleConfigFileOutput += get_print_board(node.boardSetUp) + "\n"


def calculate_h_n_permutation_inversions(board):
    goal_state = predict_final_board(board)
    goal_reduced = []
    board_reduced = []
    # Add the important 2 rows to a single 1D array
    for i in range(0, 5):
        goal_reduced.append(goal_state[0][i])
        board_reduced.append(board[0][i])
    for i in range(0, 5):
        goal_reduced.append(goal_state[2][i])
        board_reduced.append(board[2][i])

    # Add the counter to differentiate different instances of the same candy type
    for i in range(len(goal_reduced)):
        goal_reduced[i] = goal_reduced[i] + str(i)
        board_reduced[i] = board_reduced[i] + str(i)

    estimation = 0
    if board_reduced[0] != goal_reduced[0]:
        estimation += 1
    for i in range(0, len(goal_reduced)):
        for j in range(i + 1, len(goal_reduced)):
            position = get_position(board_reduced[j], goal_reduced)
            # Did not find it in the goal state
            if position < i:
                estimation += 1

    return estimation


def get_position(element, array):
    for i in range(len(array)):
        if array[i] == element:
            return i
    return -1


def count_pieces_in_board(board):
    pieces = {}
    # Count how many of each piece we have on the board
    for row in board:
        for letter in row:
            if letter not in pieces:
                pieces[letter] = 0
            pieces[letter] += 1
    return pieces


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


def calculate_h_n_manhattan_distance(board):
    # print("------------------------")
    pieces = count_pieces_in_board(board)
    winningBoard = copy.deepcopy(board)
    score = 0
    #winningBoard2 = copy.deepcopy(board)

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
            if manhattan_distance(winningBoard, winningBoard[0][i], 0, i) <= manhattan_distance(board, winningBoard[2][i], 2, i):
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
                score += 2
            # For the others, pick a random piece that has 2 or more of it on the board and place it on both rows
            for piece in pieces:
                if pieces[piece] >= 2:
                    winningBoard[0][i] = piece
                    winningBoard[2][i] = piece
                    pieces[piece] -= 2
                    score += 2
    # print("+++++++++++++++++++++++")
    # print(str(winningBoard) + "\n")
    # print(str(winningBoard2) + "\n")
    return score


def calculate_h_n_simplest(board):
    counter = 0
    for i in range(0, len(board[0])):
        if board[0][i] is not board[2][i]:
            value = min(manhattan_distance(board, board[2][i], 0, i), manhattan_distance(board, board[0][i], 2, i))
            counter += value
            # counter += 1
    return counter


def manhattan_distance(board, letter, row, column):
    # print("-------------------")
    closest = 1000
    # print("board: " + str(board) +", letter: " + letter + ", row: " + str(row) + ", column: " + str(column) + "\n")

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
            # print("This is the row " + str(2) + " with a value of " + str(currentValueRow2) + " for letter " + board[2][j] + "\n")
            closest = currentValueRow2
        if board[0][j] == letter and closest > currentValueRow0:
            # print("This is the row " + str(0) + " with a value of " + str(currentValueRow0) + " for letter " + board[0][j] + "\n")
            closest = currentValueRow0
        if board[1][j] == letter and closest > currentValueRow1:
            # print("This is the row " + str(1) + " with a value of " + str(currentValueRow1) + " for letter " + board[1][j] + "\n")
            closest = currentValueRow1
    # print("Closest is " + str(closest))
    # print("------------------------")
    return closest

def manhattan_distance_DM(board, letter, row, column):
    # print("-------------------")
    closest = 1000
    # print("board: " + str(board) +", letter: " + letter + ", row: " + str(row) + ", column: " + str(column) + "\n")

    for j in range(0, 5):
        currentValueRow0 = 10000
        currentValueRow2 = 10000
        currentValueRow1 = 10000
        if column >= j:
            currentValueRow1 = column - j + 1
            if row == 0:
                currentValueRow0 = column - j + 2
                currentValueRow2 = column - j
            else:
                currentValueRow0 = column - j
                currentValueRow2 = column - j + 2
        else:
            currentValueRow1 = j - column + 1

        if column < j:
            if row == 0:
                currentValueRow0 = j - column + 2
                currentValueRow2 = j - column
            else:
                currentValueRow0 = j - column
                currentValueRow2 = j - column + 2
        if board[2][j] == letter and closest > currentValueRow2:
            # print("This is the row " + str(2) + " with a value of " + str(currentValueRow2) + " for letter " + board[2][j] + "\n")
            closest = currentValueRow2
        if board[0][j] == letter and closest > currentValueRow0:
            # print("This is the row " + str(0) + " with a value of " + str(currentValueRow0) + " for letter " + board[0][j] + "\n")
            closest = currentValueRow0
        if board[1][j] == letter and closest > currentValueRow1:
            # print("This is the row " + str(1) + " with a value of " + str(currentValueRow1) + " for letter " + board[1][j] + "\n")
            closest = currentValueRow1
    # print("Closest is " + str(closest))
    # print("------------------------")
    return closest


def manhattan_distance_v1(board, letter, row, column):
    if letter == 'e':
        return 1000000
    if row != 2 and board[row + 1][column] == letter:
        return 1
    if row != 0 and board[row - 1][column] == letter:
        return 1
    if column != 0 and board[row][column - 1] == letter:
        return 1
    if column != 4 and board[row][column + 1] == letter:
        return 1
    if column != 4 and row != 2 and board[row + 1][column + 1] == letter:
        return 2
    if column != 0 and row != 0 and board[row - 1][column - 1] == letter:
        return 2
    if column != 0 and row != 2 and board[row + 1][column - 1] == letter:
        return 2
    if column != 4 and row != 0 and board[row - 1][column + 1] == letter:
        return 2
    if column < 3 and board[row][column + 2] == letter:
        return 2
    if column > 1 and board[row][column - 2] == letter:
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


def algoTypeCheck(algoChoice):
    if type(algoChoice) != str:
        return False

    if algoChoice != '1' and algoChoice != '2':
        print(algoChoice + " is not valid.")
        return False
    return True

def solve_file_problems(filename):
    global startTime, endTime, totalTime, boardNumber, puzzleConfigFileOutput, finalFileOutput, puzzleConfigFileOutput
    global numberOfMoves

    algoChoice = input("1) best_first_search_algorithm\n2) a_star_search_algorithm\n")
    while not algoTypeCheck(algoChoice):
        algoChoice = input("Please insert a valid input.\n")

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
    create_output_file_board_state()
    create_end_game_file()
    print("The boards have been solved. Please check the the output files.\n")
    finalFileOutput = ""
    puzzleConfigFileOutput = ""
    boardNumber = 0
    numberOfMoves = 0
    totalTime = 0

# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--file", help="The file with the candy info", default="")
args = parser.parse_args()

# main loop
while True:
    autoInput = input("1) Automatic mode\n2) Manual mode\n3) Generate puzzle files\n4) Exit\n")
    while not autocheck(autoInput):
        autoInput = input("Please insert a valid input.\n")

    if autoInput == '2':
        gameLoop(BoardSetUp.getBoardSetup("puzzlefiles/" + args.file))
    elif autoInput == '1':
        solve_file_problems("puzzlefiles/" + args.file)
    elif autoInput == '3':
        print(args.file)
        PuzzleGenerator.generate_puzzle_files()
    else:
        print('Exiting')
        sys.exit()
