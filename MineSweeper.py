import random

def build_board(x, y, num):
  board = []
  for i in range(y):
    row = []
    for j in range(x):
      row.append(0)
    board.append(row)
  board[y - 1][x - 2] = -1
  for j in range(num - 1):
    a = int(random.uniform(0, y))
    b = int(random.uniform(0, x))
    while board[a][b] == -1:
      a = int(random.uniform(0, y))
      b = int(random.uniform(0, x))
    board[a][b] = -1
  return board

def build_psuedo_board(x, y):
  board = []
  for i in range(y):
    row = []
    for j in range(x):
      row.append(" ")
    board.append(row)
  return board

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

def define_board(board):
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] == -1:
        k = i - 1
        while k <= i + 1:
          l = j - 1
          while l <= j + 1:
            if k >= 0 and l >= 0 and k < len(board) and l < len(board[0]) and board[k][l] != -1:
              board[k][l] += 1
            l += 1
          k += 1

def check_move(board, x, y):
  if board[x][y] == -1:
    return 1
  elif board[x][y] > 0:
    return 0
  else:
    return 2

def check_win(board, num):
  count = num
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] != " " or board[i][j] == "f":
        count += 1
  if count == len(board) * len(board[0]):
    return 1
  return 0

def open_area(board, psuedo, x, y, prev):
  if board[x][y] != 0:
    psuedo[x][y] = board[x][y]
    return psuedo
  
  psuedo[x][y] = board[x][y]
  if y + 1 < len(board) and (psuedo[x][y + 1] == " " or psuedo[x][y + 1] == "1") and prev != 2:
    open_area(board, psuedo, x, y + 1, 1)
  if y - 1 >= 0 and (psuedo[x][y - 1] == " " or psuedo[x][y - 1] == "1") and prev != 1:
    open_area(board, psuedo, x, y - 1, 2)
  if x + 1 < len(board[0]) and (psuedo[x + 1][y] == " " or psuedo[x + 1][y] == "1") and prev != 4:
    open_area(board, psuedo, x + 1, y, 3)
  if x - 1 >= 0 and (psuedo[x - 1][y] == " " or psuedo[x - 1][y] == "1") and prev != 3:
    open_area(board, psuedo, x - 1, y, 4)
  if x + 1 < len(board[0]) and y + 1 < len(board) and (psuedo[x + 1][y + 1] == " " or psuedo[x + 1][y + 1] == "1"):
    open_area(board, psuedo, x + 1, y + 1, 0)
  if x + 1 < len(board[0]) and y - 1 >= 0 and (psuedo[x + 1][y - 1] == " " or psuedo[x + 1][y - 1] == "1"):
    open_area(board, psuedo, x + 1, y - 1, 0)
  if x - 1 >= 0 and y + 1 < len(board) and (psuedo[x - 1][y + 1] == " " or psuedo[x - 1][y + 1] == "1"):
    open_area(board, psuedo, x - 1, y + 1, 0)
  if x - 1 >= 0 and y - 1 >= 0 and (psuedo[x - 1][y - 1] == " " or psuedo[x - 1][y - 1] == "1"):
    open_area(board, psuedo, x - 1, y - 1, 0)
  

game_info = input("Enter size and bombs: ")
x, y, num = game_info.split(" ")

game = build_board(int(x), int(y), int(num))
psuedo = build_psuedo_board(int(x), int(y))
define_board(game)
print_board(game)
while(True):
  print_board(psuedo)
  while(True):
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
  if f != "":
    psuedo[x][y] = "f"
    continue
  result = check_move(game, x, y)
  if result == 1:
    print("Game Over")
    print_board(game)
    break
  elif result == 0:
    psuedo[x][y] = game[x][y]
  else:
    psuedo[x][y] = game[x][y]
    open_area(game, psuedo, x, y, 0)
  if check_win(psuedo, int(num)):
    print("You Win!")
    print_board(game)
    break