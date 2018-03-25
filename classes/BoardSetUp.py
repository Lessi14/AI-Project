
class BoardSetUp:
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.board = board

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

    def getBoardSetup(self, filename):
        boardsetup = []
        with open("../ " + filename) as file:
            for line in file:
                if 'e' not in line or ('r' not in line and 'b' not in line):
                    print("This board is not valid. Board: " + line)
                    continue
                board = self.build_board(line)
                boardsetup.append(board)

        return boardsetup
