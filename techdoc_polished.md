# HKDSE ICT SBA Gomoku Project Technical Document

**Author:** Jimmy Yang  
**Project:** Terminal-based Gomoku Implementation

-------

## Section 1: Introduction

This document provides a technical overview of my School-Based Assessment (SBA) Gomoku project. Developed using the **Python 3.14.3** interpreter, the program is designed for cross-platform compatibility, supporting **Windows Terminal**, **macOS**, and **Linux** environments (provided a Python interpreter >=3.14.3 is installed).

The core functionality of the program is to generate a standard 15×15 Gomoku board and handle move entry via coordinates. Key features include an automated win-detection algorithm and a dynamic, self-refreshing terminal interface.

The development was conducted on **Arch Linux x86_64**. The project relies solely on the Python Standard Library, requiring no third-party dependencies for the game logic.

## Section 2: Data & Variables

This section describes the data structures used to manage the game state.

**Board Representation:**
The board is implemented using a **two-dimensional (2D) array** (a list of lists). This structure allows for direct mapping of Cartesian coordinates to the digital board, enabling efficient data access through `board[row][col]`.

The following snippet from the winner recognition phase demonstrates how the board data is accessed:

```Python
while 0 <= nr < SIZE and 0 <= nc < SIZE and board[nr][nc] == p:
```

Status Variables:
Two primary global variables manage the game flow and user experience:

`current_player`: Tracks the active player (Black or White), used for move validation and UI updates.

`status_msg`: Acts as a message buffer. Because the terminal is cleared before every turn, this variable stores feedback—such as error messages or placement confirmations—to ensure they are displayed in the next rendered frame.

## Section 3: Module Composition

This section explains the program's modular architecture and the logic behind its core functions.

### Section 3 Part 1: Parsing Input

To interact with the game, user-entered strings (e.g., "A8") must be translated into array indices.

```python
def parse_input(input_str):
    s = input_str.strip().upper()
    if s == 'Q':
        return 'QUIT', ""
```

The function sanitizes the input by removing whitespace and converting it to uppercase. It immediately checks for the `"Q"` signal to allow users to interrupt and exit the game.

```python
if len(s) < 2:
        return None, "Coordinate too short."
```

The script then performs a length check to ensure the input contains at least a column letter and a row number.

```python
    try:
        col = ord(s[0]) - ord('A')
        row = int(s[1:]) - 1
        
        if 0 <= col < SIZE and 0 <= row < SIZE:
            return (row, col), ""
        else:
            return None, "Coordinate out of range."
    except (ValueError, IndexError):
        return None, "Invalid input."
```

The parsing logic utilizes **Exception Handling** *\(try...except\)*. This follows the *EAFP \(Easier to Ask for Forgiveness than Permission\)* coding style:

**Readability**: It avoids deeply nested if-else logic, improving maintainability.

**Robustness**: It catches runtime errors \(such as invalid characters in the row number\) without crashing the program.

**Validation**: It ensures resulting indices fall within the 0–14 range required by the 15×15 board.

### Section 3 Part 2: Clearing Screen

To provide a seamless visual experience, the program clears the terminal history before rendering each new move.

```python
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
```

The logic detects the operating system via `os.name`. It sends the `cls` command for *Windows \(NT\)* systems and the clear command for *POSIX-compliant systems \(Linux/macOS\)*.

### Section 3 Part 3: Creating Board

The board is initialized using a list comprehension to create a 15x15 grid of empty characters.

```python
def create_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
```

### Section 3 Part 4: Printing Board

This module handles the visual rendering of the game. Every refresh begins with clear_screen() to maintain a "static" board appearance.

```python
def print_board(board, status_msg, current_player):
    clear_screen()
```

The program generates column headers \(A–O\) and the top border. A for loop then iterates through the rows, using the `.rjust(2)` method on row numbers to ensure that single-digit and double-digit numbers align perfectly.


```python
for i in range(SIZE):
    row_num = str(i + 1).rjust(2)
    row_content = " ".join(board[i])
    print(f" {row_num} | {row_content} | {row_num}")
```

The UI metadata \(Current Player and System Messages\) is included in this function to ensure it remains visible on the screen after the clearing operation.

```python
    print(f"\n[ Current Player ]: {current_player}")
    print(f"[ System Msg ]: {status_msg}")
    print("-" * 40)
```

### Section 3 Part 5: Winner Checking

Winner recognition is the core algorithm of the script. To optimize performance, the script implements Local Directional Checking instead of scanning the entire board.

The logic focuses on the most recently placed stone and checks for a line of 5 in four axes: horizontal, vertical, and both diagonals.

```python
def check_win(board, rowc, column, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
```

For each axis, the script performs a bidirectional search:

Forward Search: Moves in one direction \(e.g., right\), incrementing the count for matching stones.

Backward Search: Moves in the opposite direction \(e.g., left\) to find the remainder of the sequence.

#### Forward Search logic
```python
        new_r, new_c = rowc + change_r, column + change_c
        while 0 <= new_r < SIZE and 0 <= new_c < SIZE and \
            board[new_r][new_c] == player:
            count += 1
            new_r += change_r
            new_c += change_c
        
        # Backward Search logic
        new_r, new_c = rowc - change_r, column - change_c
        while 0 <= new_r < SIZE and 0 <= new_c < SIZE and \
            board[new_r][new_c] == player:
            count += 1
            new_r -= change_r
            new_c -= change_c
```

If the count reaches 5 or more \(unlikely to happen unless the script is modded\), the function returns True, signaling a victory.

## Section 4: Main Loop

The `main()` function orchestrates the game's lifecycle. It initializes the board and enters a loop that persists until a win condition is met or the user quits.

The loop handles:

**Validation**: Ensuring the selected cell is not already occupied.

**Win/Draw Detection**: Checking if the last move won the game or if the board is full.

**State Switching**: Toggling the active player between Black and White.

```python
        status_msg = f"Player {current_player} placed at {user_input.upper()}"
        current_player = WHITE if current_player == BLACK else BLACK
```

The script includes a standard Python entry point check, ensuring the functions can be imported as a module without automatically starting the game.

```python
if __name__ == "__main__":
    main()
```

## Section 5: Future Development Plan

Artificial Intelligence \(PvE\):
I plan to implement a player vs. Environment mode using the *Minimax* algorithm \(a search-based AI model\) and potentially research *CNN \(Convolutional Neural Network\)* models like the Rapfi project for advanced pattern recognition.

**UI Enhancements**:
While the current version focuses on terminal portability, a Graphical User Interface \(GUI\) using the `pygame` library could improve accessibility, though it would introduce external dependencies.

## Section 6: Reusability and Portability

The script is highly portable due to its reliance on standard *Python* libraries. It has been tested on:

**Arch Linux x86_64**: Kernel 6.19.9, using the Kitty terminal.

**Windows 11 25H2**: Using Windows Terminal.

**Chimera Linux x86_64**: Preliminary testing on specific Linux distribution, verify the portability on different standard C library.

**aarch64**: Preliminary testing on mobile/embedded Linux architectures.
## Section 7: References

**Python 3.14.3 Tutorial**: https://docs.python.org/3/tutorial/index.html

**Windows Terminal Customize Actions**: https://learn.microsoft.com/zh-tw/windows/terminal/customize-settings/actions

**Rapfi Project**: https://github.com/dhbloo/rapfi

**Markdown Tutorial**: https://markdown.com.cn/

## Section 8: Redistribution and Availability

This project is distributed under the MIT License.

Source code and documentation are available at:
https://github.com/sarosaka-orz/HKDSE-ICT-SBA-Gomoku

