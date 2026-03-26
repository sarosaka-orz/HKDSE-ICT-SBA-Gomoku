import os

SIZE = 15
EMPTY = ' '
BLACK = 'X'
WHITE = 'O'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def print_board(board, status_msg, current_player):
    clear_screen()
    
    letters = [chr(ord('A') + i) for i in range(SIZE)]
    print("\n      " + " ".join(letters))
    print("     +" + "--" * SIZE + "+")

    for i in range(SIZE):
        row_num = str(i + 1).rjust(2)
        row_content = " ".join(board[i])
        print(f" {row_num} | {row_content} | {row_num}")

    print("     +" + "--" * SIZE + "+")
    print("      " + " ".join(letters))
    
    print(f"\n[ Current Player ]: {current_player}")
    print(f"[ System Msg ]: {status_msg}")
    print("-" * 40)

def parse_input(input_str):
    s = input_str.strip().upper()
    if s == 'Q':
        return 'QUIT', ""
    
    if len(s) < 2:
        return None, "Coordinate too short."
    
    try:
        col = ord(s[0]) - ord('A')
        row = int(s[1:]) - 1
        
        if 0 <= col < SIZE and 0 <= row < SIZE:
            return (row, col), ""
        else:
            return None, "Coordinate out of range."
    except (ValueError, IndexError):
        return None, "Invalid input."

def check_win(board, rowc, column, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for change_r, change_c in directions:
        count = 1
        new_r, new_c = rowc + change_r, column + change_c
        while 0 <= new_r < SIZE and 0 <= new_c < SIZE and \
            board[new_r][new_c] == player:
            count += 1
            new_r += change_r
            new_c += change_c
        new_r, new_c = rowc - change_r, column - change_c
        while 0 <= new_r < SIZE and 0 <= new_c < SIZE and \
            board[new_r][new_c] == player:
            count += 1
            new_r -= change_r
            new_c -= change_c
        if count >= 5:
            return True
    return False

def main():
    board = create_board()
    current_player = BLACK
    status_msg = f"Player {current_player} please place."

    while True:
        print_board(board, status_msg, current_player)
        
        user_input = input("Please input the coordinate, or type in Q to quit.")
        
        result, error_err = parse_input(user_input)
        
        if result == 'QUIT':
            print("Interrupt signal detected.")
            break
            
        if result is None:
            status_msg = f"Error: {error_err}"
            continue
            
        row, col = result
        
        if board[row][col] != EMPTY:
            status_msg = f"Error: Position {user_input.upper()} is already taken."
            continue
            
        board[row][col] = current_player
        
        if check_win(board, row, col, current_player):
            print_board(board, f" Congrats! Player {current_player} wins!", current_player)
            print("GAME OVER")
            break
            
        if all(cell != EMPTY for row in board for cell in row):
            print_board(board, "It is a draw!", current_player)
            break

        status_msg = f"Player {current_player} placed at {user_input.upper()}"
        current_player = WHITE if current_player == BLACK else BLACK

if __name__ == "__main__":
    main()
