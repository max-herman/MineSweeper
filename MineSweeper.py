# imported libraries
import random


# method: board which holds values of each position, not what is displayed in game
# input: x,y range and num bombs
# output: built board with bombs in place
# effects: none
def build_board(x, y, num):
    board = []
    for i in range(y):
        row = []
        for j in range(x):
            row.append(0)
        board.append(row)

    # Find a random position for all bombs
    for j in range(num):
        a = int(random.uniform(0, y))
        b = int(random.uniform(0, x))

        # if a bomb exists in the given spot, find another x,y
        while board[a][b] == -1:
            a = int(random.uniform(0, y))
            b = int(random.uniform(0, x))
        board[a][b] = -1
    return board


# method: build a board to display
# input: x,y range
# output: board with nothing showing inside
# effects: none
def build_psuedo_board(x, y):
    board = []
    for i in range(y):
        row = []
        for j in range(x):
            row.append(" ")
        board.append(row)
    return board


# method: Defined print formatting for printing the board with numeric position
# input: board
# output: print formatted layout for board
# effects: none
def print_board(board):
    print("    ", end="")
    for i in range(len(board[0])):
        print(" ", i, "  ", sep = "", end = "")
    print("\n  ", end = "")
    print("--- " * len(board) + "---")
    for i in range(len(board)):
        print(i,"| ", end = "")
        for j in range(len(board[0])):
            print("%2s" % str(board[i][j]), end = "  ")
        print("|")
    print("  ", "--- " * len(board) + "---\n\n", sep="")


# method: get a value for any position != -1, i.e. if 1 or 2 ... 8 bombs surround a position
# input: board
# output: none
# effects: change values of board to show how many bombs are adjacent
def define_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):

          # if a bomb is found, add 1 to every position adjacent to i,j
          if board[i][j] == -1:
              k = i - 1
              while k <= i + 1:
                  l = j - 1
                  while l <= j + 1:
                      if k >= 0 and l >= 0 and k < len(board) and l < len(board[0]) and board[k][l] != -1:
                          board[k][l] += 1
                      l += 1
                  k += 1


# method: check if a position contains a bomb
# input: board, x,y positon
# output: boolean if a bomb is in place
# effects: none
def check_move(board, x, y):
    if board[x][y] == -1:
        return False
    else:
        return True


# method: Check if the board is completed and the user won
# input: board, shown board
# output: boolean, if a board is fully filled
# effects: none
def check_win(board, psuedo):
    for i in range(len(psuedo)):
        for j in range(len(psuedo[0])):

            # if a position is not filled, game is not over
            if psuedo[i][j] == " " and board[i][j] != -1:
                return 0
            if psuedo[i][j] == 'f' and board[i][j] != -1:
                return 0
    return 1


# method: Recursive method to show all zeros/near-digits in a reltaed area
# input: board, shown board, x,y positon
# output: shown board
# effects: modifies shown board by revealing zeros
def open_area(board, psuedo, x, y):

    # if a position is not a zero, then show it and backtrack
    if board[x][y] != 0:
        psuedo[x][y] = board[x][y]
        return psuedo
  
    psuedo[x][y] = board[x][y]

    # check every position surrounding x,y
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if i < len(psuedo) and j < len(psuedo[i]) and i >= 0 and j >= 0:
                if psuedo[i][j] == ' ' or psuedo[i][j] == "1":
                    open_area(board, psuedo, i, j)
  
# main game loop
if __name__ == "__main__":

    # generate a game board in a dynamic size with n bombs
    game_info = input("Enter size and bombs: ")
    x, y, num = game_info.split(" ")

    # create 2 boards, one to be displayed and one holding bomb values
    game = build_board(int(x), int(y), int(num))
    psuedo = build_psuedo_board(int(x), int(y))
    define_board(game)
    print_board(game)
    print("Valid Move: \'x y f\'; f value is optional")

    # start main game loop, ask for a position to check and either place a flag or reveal if a bomb exists
    while(True):
        print_board(psuedo)

        # keep requesting a move until a valid move is given
        while(True):

            # if more than 2 values given, break
            try:
                move = input("Move: ")
                if len(move) == 5:
                  y, x, f = move.split(" ")
                else:
                  y, x = move.split(" ")
                  f = ""
                x, y = int(x), int(y)
                break
            except:
                print("ERROR: Only (2) integers allowed.")
                continue
        
        # if a 'flag' flag is given then place a flag
        if f != "":
            if psuedo[x][y] == "f":
              psuedo[x][y] = ""
            else:
              psuedo[x][y] = "f"
            continue
        
        # Check whether the given position contains a bomb or not
        result = check_move(game, x, y)

        # if not, check if it is adjacent to a bomb or a zero
        if result:
            psuedo[x][y] = game[x][y]

            # open up the surrounding positions if a zero
            if game[x][y] == 0:
                open_area(game, psuedo, x, y)
            
        # if x,y contains a bomb, then the user losses the game
        else:
            print("Game Over")
            print_board(game)
            break
        
        # check whether the user has won the game
        if check_win(game, psuedo):
            print("You Win!")
            print_board(game)
            break
