import copy


class Node:
    def __init__(self, g_n, h_n, listOfMoves, boardSetUp):
        self.g_n = g_n
        self.h_n = h_n
        self.f_n = self.g_n + self.h_n
        self.listOfMoves = copy.deepcopy(listOfMoves)
        self.boardSetUp = boardSetUp
