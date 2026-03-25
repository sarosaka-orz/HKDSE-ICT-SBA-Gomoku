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
`current_player` is set as a storage of current placing player, used for the judgment and the message system. `status_msg` is set as a temporary stack for the game's status, and printed out when a event is happened during the game's process. The reason we need a temporary stack is that we need a variable to store the status message even after the terminal screen has been cleared. After the clear, the support of `status_msg` will provide us the message used for displaying on the next game frame.

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

