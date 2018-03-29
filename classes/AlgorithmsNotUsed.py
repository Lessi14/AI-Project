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
