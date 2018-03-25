import random
import copy
import sys
import os


def generate_puzzle_file(filename, text):
    file = open(os.getcwd() +"/puzzlefiles/" + filename, "w")
    print(file)
    file.write(text)


def generate_novice_file(filename):
    array = ['e', 'r', 'r', 'r', 'r', 'r', 'r', 'b', 'b', 'b', 'b', 'b', 'b', 'w', 'w']
    generate_difficulty_file(filename, array, 50)


def generate_apprentice_file(filename):
    array = ['e', 'r', 'r', 'r', 'r', 'r', 'r', 'b', 'b', 'b', 'b', 'y', 'y', 'w', 'w']
    generate_difficulty_file(filename, array, 50)


def generate_expert_file(filename):
    array = ['e', 'r', 'r', 'r', 'r', 'g', 'g', 'b', 'b', 'b', 'b', 'y', 'y', 'w', 'w']
    generate_difficulty_file(filename, array, 30)


def generate_master_file(filename):
    array = ['e', 'r', 'r', 'r', 'r', 'g', 'g', 'b', 'b', 'p', 'p', 'y', 'y', 'w', 'w']
    generate_difficulty_file(filename, array, 10)


def generate_difficulty_file(filename, array, numberOfPuzzles):
    text = ""
    for i in range(0, numberOfPuzzles):
        shuffledArray = copy.deepcopy(array)
        random.shuffle(shuffledArray)
        for letter in shuffledArray:
            text += letter + " "
        text = text.rstrip()
        text += '\n'
    text = text.rstrip('\n')
    generate_puzzle_file(filename, text)


def generate_puzzle_files():
    difficulty = input("Choose a difficulty\n1) Novice\n2) Apprentice\n3) Expert\n4) Master\n")
    while not (difficulty == '1' or difficulty == '2' or difficulty == '3' or difficulty == '4'):
        difficulty = input("Please insert a valid input.\n")
    if difficulty == '1':
        generate_novice_file("novice.txt")
    elif difficulty == '2':
        generate_apprentice_file("apprentice.txt")
    elif difficulty == '3':
        generate_expert_file("expert.txt")
    elif difficulty == '4':
        generate_master_file("master.txt")
    sys.exit()
