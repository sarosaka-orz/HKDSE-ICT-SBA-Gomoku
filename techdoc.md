# HKDSE ICT SBA Gomoku Project Technical Document

Made by Jimmy Yang.

-------

## Section 1 : Introduction

This is a technical document for my school-based assessment Gomoku project. The program is based on *Python 3.14.3* interpreter while can be executed under *Windows Terminal* and *macOS/Linux terminal environment* with the support of *Python (>=3.14.3)* interpreter.

The program's core function is to spawn a 15×15 standard Gomoku chessboard and supports the coordinates method for arranging the chesses. Other basic functions are automatic winner recognition and the refresh of the terminal screen.

Program's development environment is standard *Python 3.14.3* under *Arch Linux x86_64*, while doesn't have any requirements of external third-party libraries.

## Section 2 : Data Structures

In this section, I will explain how do I store the game's status.

Board's presentation: use 2-dimensional array to initialize the board as empty. The reason for choosing the 2-dimensional is the easy access of the data through `board[row][col]`.

The accessing code example below is from the *winner recognition* part.

```Python
while 0 <= nr < SIZE and 0 <= nc < SIZE and board[nr][nc] == p:
```

Status variables: In the code, I set 2 main global variables for the game's experience optimization,
`current_player` is set as a storage of current placing player, used for the judgment and the message system.   
`status_msg` is set as a temporary stack for the game's status, and printed out when a event is happened during the game's process. The reason we need a temporary stack is that we need a variable to store the status message even after the terminal screen has been cleared. After the clear, the support of `status_msg` will provide us the message used for displaying on the next game frame.

## Section 3 : Core Algorithms

In this section, I will explain how my program runs, and its core algorithms, while having some quotes of the code.

### Section Part 1 : Parsing Input

The first part will be the method of breaking user's input into parts that the program can understand. In this part, the user will type in their potential coordinates into the terminal like A8 or H8, however, the algorithms cannot directly decide the position, so we need to break it apart, and transfer them into offsets to the array.

```Python
def parse_input(input_str):
    s = input_str.strip().upper()
    if s == 'Q':
        return 'QUIT', ""
```

This part of the code will first accept the user's input, and check if the user's input is requiring the program to interrupt and exit, by checking if the input is the exit signal `"Q"`.

```Python
    if len(s) < 2:
        return None, "Coordinate too short."
```

This part of the code will secondly accept the user's input, if the user's request is not interrupting and quitting the program. It will check the input's length, and make sure the input is long enough to proceed, otherwise it will return `None` and require user to re-enter the coordinates.

```Python
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

This part of the code is the error handling part. It uses the `try catch throw` method of catching and handling error, whether to jump to another part of the program or just simply interrupt the program from continue running, and pass the further processing to end-user. The `try catch throw` method has several benefits than traditional error handling:

1. Code is clear and easy to read, rather than bunch of `if-else`, benefit the future extend and maintenance.
2. `try-except` can catch runtime errors easily without interrupting the entire program and pops up a error message.
3. The usage of this error handling method has performed a famous thinking in *Python* world, that is *EAFP*, *Easier to Ask for Forgiveness than Permission*.

If the user is trying to input values that is out of the range, it will return a `None` and then told the user to input again, but not interrupt the program itself.

### Section 3 Part 2 : Clearing Screen

Tired of scrolling down the terminal page? Then `os` module have you covered.

```Python
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
```

This part of the code takes a very little of the total space of the entire script, but it improves the experience of the game a lot. Rather than keep scrolling down the terminal output, it will automatically clear the screen for you, keep your mind focusing on the chess board.

The core logic of the code is checking OS type and then send the correct clearing command to the terminal emulator. If the result of `os.name` is `nt`, which is a abbreviation of a certain type of OS `Windows NT`, or more commonly the normal *Windows* we use today. If the result was not `nt`, then the program will recognize the environment as `POSIX Compliant System`, or more commonly *macOS*, *UNIX* or *Linux*.

### Section 3 Part 3 : Creating Board

This section of the code is simply create a two-dimensional array which is used for storing the data of the chess board.

```Python
def create_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
```

### Section 3 Part 4 : Printing Board

In this part of the program, the program itself will print or display the board to the current terminal screen.

Below is the first part of the code, it will first define the function itself, which let itself can be used in the main program, then it will call `clear_screen` function, it was used for clearing the terminal output to keep the screen clean, in order to improve the game experience.

```Python
def print_board(board, status_msg, current_player):
    clear_screen()
```
After clearing the screen, program will first discover the 15 letters which is board is using, and then print the board by adding line break symbol \(`\n`\) and spaces. Then it will use `-` as a symbol for printing the border of the chess board.

```Python
    letters = [chr(ord('A') + i) for i in range(SIZE)]
    print("\n      " + " ".join(letters))
    print("     +" + "--" * SIZE + "+")
```

In the next period of the code, the script will call `for` loop, use `i` as a local variable, and the global variable `SIZE` as the range for the loop. Then it will set `row_num` and `row_content`, these two local variable will help the script to adjust the length of the row, or in another way, to make it aligned. After that, `row_content` will help us to store the chess' position data in the two-dimensional array we created. Moreover, the `print` function will print the position indicator \(A5 or H6\) above the border.

```Python
    for i in range(SIZE):
        row_num = str(i + 1).rjust(2)
        row_content = " ".join(board[i])
        print(f" {row_num} | {row_content} | {row_num}")
```
Behind this period of the code, the script will call `print` function for 2 times, in order to display the bottom border of the chess board.

```Python
    print("     +" + "--" * SIZE + "+")
    print("      " + " ".join(letters))
```
Additionally, the script will call `print` function for 3 times, in order to print `Current Player`, `System Msg\(abbreviation of message\)` and the bottom of the board. This is one of the most core part of the script, because it provides a improved experience for the player, and a pipeline for the player to know the situation and the event, or even a error thrown. We need to include this part of `print` function block in the `print_board` part, in order to keep them on the screen after we call the `clear_screen` function to clear the screen every time when the board needs refreshing.

```Python
    print(f"\n[ Current Player ]: {current_player}")
    print(f"[ System Msg ]: {status_msg}")
    print("-" * 40)
```

### Section 3 Part 5 : Winner Checking

In this part of the technical document, we will break apart the most core algorithms in the Gomoku script - the winner checking part.

The most straightforward and the most violent way to check the winner is to scan the whole chess board and looking for a continuous 5 chesses, whether it is in a row, a column or a diagonal.

What is the problem of scanning the whole chess board? The most fatal problem is the poor performance. Although modern computers doesn't need this type of small optimization, but a huge performance problem is heaped up by small performance problems. So in this part, I decided to develop a new method of checking the winner, the answer is *local checking*.
