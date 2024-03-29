#search algorithm
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


#search algorithm
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

#search algorithm
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


#calculates h(n) using permutation inversions
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


#calculates h(n)
def calculate_h_n_simplest(board):
    counter = 0
    for i in range(0, len(board[0])):
        if board[0][i] is not board[2][i]:
            value = min(manhattan_distance(board, board[2][i], 0, i), manhattan_distance(board, board[0][i], 2, i))
            counter += value
            # counter += 1
    return counter


#alternative to manhattan distance
def manhattan_distance_DM(board, letter, row, column):
    closest = 1000

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
            closest = currentValueRow2
        if board[0][j] == letter and closest > currentValueRow0:
            closest = currentValueRow0
        if board[1][j] == letter and closest > currentValueRow1:
            closest = currentValueRow1
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