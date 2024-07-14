# necessery imports
import tkinter
import random

# function that saves the settings
def save_settings(mines, rows, columns):
    pass

# function that opens a settings window
def settings():
    settings_window = tkinter.Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry("400x200")
    settings_window.resizable(False, False)
    settings_window.config(bg="black")
    settings_window.iconbitmap("Mine.ico")
    # creating a label for the title of the settings window
    title_label = tkinter.Label(settings_window, text="Settings", font=("Helvetica", 20), bg="black", fg="white")
    title_label.pack(side="top")
    # creating a frame for the settings
    settings_frame = tkinter.Frame(settings_window, bg="black")
    settings_frame.pack()
    # creating a label for the number of mines
    mines_label = tkinter.Label(settings_frame, text="Number of Mines:", font=("Helvetica", 12), bg="black", fg="white")
    mines_label.grid(row=0, column=0)
    # creating an entry for the number of mines
    e1 = tkinter.StringVar()
    e1.set(str(num_of_mines))
    mines_entry = tkinter.Entry(settings_frame, font=("Helvetica", 12), textvariable=e1)
    mines_entry.grid(row=0, column=1)
    # creating a label for the number of rows
    rows_label = tkinter.Label(settings_frame, text="Number of Rows:", font=("Helvetica", 12), bg="black", fg="white")
    rows_label.grid(row=1, column=0)
    # creating an entry for the number of rows
    e2 = tkinter.StringVar()
    e2.set(str(num_of_rows))
    rows_entry = tkinter.Entry(settings_frame, font=("Helvetica", 12), textvariable=e2)
    rows_entry.grid(row=1, column=1)
    # creating a label for the number of columns
    columns_label = tkinter.Label(settings_frame, text="Number of Columns:", font=("Helvetica", 12), bg="black", fg="white")
    columns_label.grid(row=2, column=0)
    # creating an entry for the number of columns
    e3 = tkinter.StringVar()
    e3.set(str(num_of_columns))
    columns_entry = tkinter.Entry(settings_frame, font=("Helvetica", 12), textvariable=e3)
    columns_entry.grid(row=2, column=1)
    # creating a label for the resizable window check button
    resizable_label = tkinter.Label(settings_frame, text="Resizable window", font=("Helvetica", 12), bg="black", fg="white")
    resizable_label.grid(row=3, column=0)
    # creating a check button for resizable window
    resizable_var = tkinter.IntVar()
    resizable_check = tkinter.Checkbutton(settings_frame, bg="black", variable=resizable_var)
    resizable_check.grid(row=3, column=1,)
    # creating a save button
    save_button = tkinter.Button(settings_frame, text="Save", font=("Helvetica", 12), bg="black", fg="white", command=lambda: save_settings(mines_entry.get(), rows_entry.get(), columns_entry.get()))
    save_button.grid(row=4, column=0, columnspan=2)

# function that restarts the game
def restart():
    pass

# function that handles the click event on the buttons
def click(i, j):
    # check if the clicked button is a mine if yes than the game is over
    if (i, j) in mine_coordinates:
        # marking the mines
        buttons[i][j].config(text="X", bg="red")
        title_label.config(text="Game Over")
        for x, y in mine_coordinates:
            buttons[x][y].config(text="X", bg="red")
        # disabling the board
        for row in buttons:
            for button in row:
                button.config(state="disabled")
    else:
        reveal(i, j)

# function that reveals the empty spaces and numbers around the clicked button and around the empty bordering buttons and so on
def reveal(i, j):
    # revealing the clicked button
    buttons[i][j].config(bg="white")
    tiles_to_check = []
    tiles_to_check.append((i, j+1))
    tiles_to_check.append((i, j-1))
    tiles_to_check.append((i+1, j))
    tiles_to_check.append((i-1, j))

    # revealing the empty spaces and numbers around the clicked button, if there are any empty spaces around the clicked button the function will check them as well
    while len(tiles_to_check) > 0:
        i, j = tiles_to_check[0][0], tiles_to_check[0][1]
        print(i, j)
        if (i, j) in empty_spaces_coordinates:
            buttons[i][j].config(bg="white")
            empty_spaces_coordinates.remove((i, j))
            print("Empty space")
            tiles_to_check.append((i, j+1))
            tiles_to_check.append((i, j-1))
            tiles_to_check.append((i+1, j))
            tiles_to_check.append((i-1, j))
        elif (i, j) in numbers_coordinates:
            temp = numbers_coordinates[numbers_coordinates.index((i, j))]
            temp2 = numbers_values_coordinates[temp]
            buttons[i][j].config(text=str(temp2), bg="white")
            numbers_coordinates.remove((i, j))
            temp.clear()
            print("Number")
        else:
            print("Mine or out of bounds")
        tiles_to_check.pop(0)
# function that fills the game board with mines based on the number of mines
def fill_mines():
    global mine_coordinates
    # filling the list with random coordinates for the mines
    for i in range(num_of_mines):
        x = random.randint(0, num_of_rows - 1)
        y = random.randint(0, num_of_columns - 1)
        # ensuring that the upper left corner is not a mine, this ensures that the player can start the game without risk
        if x == 0 and y == 0:
            i -= 1
        elif (x, y) not in mine_coordinates:
            mine_coordinates.append((x, y))
        else:
            i -= 1

# function that calculates the number of mines around each button and displays the number on the button
def numbers_around_mines():
    global numbers_coordinates, numbers_values_coordinates
    for i in range(num_of_rows):
        for j in range(num_of_columns):
            if (i, j) not in mine_coordinates:
                mines = 0
                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        if x >= 0 and x < num_of_rows and y >= 0 and y < num_of_columns and (x, y) in mine_coordinates:
                            mines += 1
                if mines > 0:
                    #buttons[i][j].config(text=str(mines))
                    #numbers_values_coordinates.append((i, j))
                    numbers_values_coordinates.append(mines)
                    numbers_coordinates.append((i, j))
    #print(numbers_coordinates)

# function that filles a list of empty spaces
def empty_spaces():
    for i in range(num_of_rows):
        for j in range(num_of_columns):
            empty_spaces_coordinates.append((i, j))
    # removing all the tiles that are in other lists
    for x, y in mine_coordinates:
        empty_spaces_coordinates.remove((x, y))
    for (x, y) in numbers_coordinates:
        empty_spaces_coordinates.remove((x, y))
    print(len(empty_spaces_coordinates))

# function to create the buttons for the game board
def create_board():
    global buttons
    for i in range(num_of_rows):
        row = []
        for j in range(num_of_columns):
            button = tkinter.Button(game_frame, width=5, height=2, bg="gray", relief="raised", command=lambda i=i, j=j: click(i, j))
            button.grid(row=i, column=j)
            row.append(button)
        buttons.append(row)

# variables for the game
num_of_mines = 10
num_of_rows = 10
num_of_columns = 10
buttons = []
mine_coordinates = []
numbers_coordinates = []
numbers_values_coordinates = []
empty_spaces_coordinates = []

# creating the main window
window = tkinter.Tk()
window.title("Minesweeper")
window.geometry("700x600")
window.resizable(False, False)
window.config(bg="black")
window.iconbitmap("Mine.ico")

# creating a label for the title of the game
title_label = tkinter.Label(window, text="Minesweeper", font=("Helvetica", 30), bg="black", fg="white")
title_label.pack(side="top")

# creating a main frame for the game
main_frame = tkinter.Frame(window, bg="black")
main_frame.pack()

# creating a frame for the buttons representing the game board
game_frame = tkinter.Frame(main_frame, bg="black")
game_frame.grid(row=0, column=0)

# creating a frame for the control buttons like restart and settings
control_frame = tkinter.Frame(main_frame, bg="black")
control_frame.grid(row=0, column=1)

# creating a label for game information
info_label = tkinter.Label(control_frame, text="Information label", font=("Helvetica", 20), bg="black", fg="white")
info_label.grid(row=1, column=0, columnspan=2)

# creating a restart button
restart_button = tkinter.Button(control_frame, text="Restart", font=("Helvetica", 15), bg="black", fg="white", command=lambda: restart())
restart_button.grid(row=2, column=0)

# creating a settings button
settings_button = tkinter.Button(control_frame, text="Settings", font=("Helvetica", 15), bg="black", fg="white", command=lambda: settings())
settings_button.grid(row=2, column=1)

# fililng the game board with buttons and performing the necessery functions
create_board()
fill_mines()
numbers_around_mines()
empty_spaces()

window.mainloop()
