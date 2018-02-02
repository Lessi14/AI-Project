import argparse
import sys

board = [[], [], []]

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
    if(len(candies) < 15):
        print("Error parsing line " + line)
        print("Found only " + str(len(candies)) + " candies")
        return
    board = [[candies[0], candies[1], candies[2], candies[3], candies[4]], [candies[5], candies[6], candies[7], candies[8], candies[9]], [candies[10], candies[11], candies[12], candies[13], candies[14]]]

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