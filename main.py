# necessery imports
import tkinter
import random

# function that saves the settings
def save_settings(mines, rows, columns, resizable):
    global num_of_mines, num_of_rows, num_of_columns
    try:
        if int(mines) < 10 or int(rows) < 10 or int(columns) < 10 or int(mines) > 50 or int(rows) > 30 or int(columns) > 30 or int(mines)/2 > int(rows) * int(columns):
            info_label.config(text="Wrong input!")
    except:
        info_label.config(text="Wrong input!")
    else:
        # setting the new values
        num_of_mines = int(mines)
        num_of_rows = int(rows)
        num_of_columns = int(columns)
        if resizable:
            window.resizable(True, True)
        else:
            window.resizable(False, False)
        # resetting the text of the information label
        info_label.config(text="Info label")
        # restarting the game to apply the new settings
        restart()

# function that opens a settings window
def settings():
    settings_window = tkinter.Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry("500x200")
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
    # instructions label
    label = tkinter.Label(settings_frame, text="Min = 10, Max = rows * colums / 2", font=("Helvetica", 8), bg="black", fg="white")
    label.grid(row=0, column=2)
    # creating a label for the number of rows
    rows_label = tkinter.Label(settings_frame, text="Number of Rows:", font=("Helvetica", 12), bg="black", fg="white")
    rows_label.grid(row=1, column=0)
    # creating an entry for the number of rows
    e2 = tkinter.StringVar()
    e2.set(str(num_of_rows))
    rows_entry = tkinter.Entry(settings_frame, font=("Helvetica", 12), textvariable=e2)
    rows_entry.grid(row=1, column=1)
    # instructions label
    label = tkinter.Label(settings_frame, text="Min = 10, Max = 30", font=("Helvetica", 8), bg="black", fg="white")
    label.grid(row=1, column=2)
    # creating a label for the number of columns
    columns_label = tkinter.Label(settings_frame, text="Number of Columns:", font=("Helvetica", 12), bg="black", fg="white")
    columns_label.grid(row=2, column=0)
    # creating an entry for the number of columns
    e3 = tkinter.StringVar()
    e3.set(str(num_of_columns))
    columns_entry = tkinter.Entry(settings_frame, font=("Helvetica", 12), textvariable=e3)
    columns_entry.grid(row=2, column=1)
    # instructions label
    label = tkinter.Label(settings_frame, text="Min = 10, Max = 30", font=("Helvetica", 8), bg="black", fg="white")
    label.grid(row=2, column=2)
    # creating a label for the resizable window check button
    resizable_label = tkinter.Label(settings_frame, text="Resizable window", font=("Helvetica", 12), bg="black", fg="white")
    resizable_label.grid(row=3, column=0)
    # creating a check button for resizable window
    resizable_var = tkinter.IntVar()
    resizable_check = tkinter.Checkbutton(settings_frame, bg="black", variable=resizable_var, activebackground="black", activeforeground="white")
    resizable_check.grid(row=3, column=1,)
    # creating a save button
    save_button = tkinter.Button(settings_frame, text="Save", font=("Helvetica", 12), bg="black", fg="white",activebackground="black", activeforeground="white", command=lambda: save_settings(mines_entry.get(), rows_entry.get(), columns_entry.get(), resizable_var.get()))
    save_button.grid(row=4, column=0, columnspan=2)

# function that is called to start a new game
def new_game():
    create_board()
    fill_mines()
    numbers_around_mines()
    empty_spaces()

# function that restarts the game
def restart():
    # resetting all the variables and lists
    global mine_coordinates, numbers_coordinates, numbers_values_coordinates, empty_spaces_coordinates, buttons_size
    mine_coordinates = []
    numbers_coordinates = []
    numbers_values_coordinates = []
    empty_spaces_coordinates = []
    # destroying all the buttons on the game board, so that new buttons can be created
    for widget in game_frame.winfo_children():
        widget.destroy()
    buttons.clear()
    # resizing the widgets in the window and resetting them to their defaults
    # getting the new sizes for the widgets
    title_size = window.winfo_height() // 20
    info_label_size = window.winfo_height() // 30
    settings_restart_size = window.winfo_height() // 40
    buttons_size = window.winfo_height() // num_of_rows // 12
    # resizing the widgets and setting default text
    title_label.config(font=("Helvetica", title_size), text="Minesweeper")
    info_label.config(font=("Helvetica", info_label_size), text="Info label")
    restart_button.config(font=("Helvetica", settings_restart_size), width=int(settings_restart_size/2))
    settings_button.config(font=("Helvetica", settings_restart_size), width=int(settings_restart_size/2))
    flag_button.config(font=("Helvetica", settings_restart_size), width=int(settings_restart_size/2))
    # starting a new game
    new_game()

# function that handles the click event on the buttons
def click(i, j):
    # checking if the flag is on, if yes than the player can mark the mines
    if is_flag_on:
        # checking if the pressed button is already marked with a number, if yes than the player can't mark it as a mine
        if (i, j) in numbers_coordinates and buttons[i][j]["bg"] == "white":
            return
        # changing the text of a button
        if buttons[i][j]["text"] == "F":
            buttons[i][j].config(text="")
        else:
            buttons[i][j].config(text="F")
        return
    # check if the clicked button is a mine if yes than the game is over
    if (i, j) in mine_coordinates:
        # marking the mines
        buttons[i][j].config(text="X", bg="red")
        info_label.config(text="Game Over")
        for x, y in mine_coordinates:
            buttons[x][y].config(text="X", bg="red")
        # disabling the board
        for row in buttons:
            for button in row:
                button.config(state="disabled")
    else:
        reveal(i, j)

# function that checks if the player has won the game
def check_win():
    # checking if there are any buttons left that are not mines and are not clicked
    for i in range(num_of_rows):
        for j in range(num_of_columns):
            if buttons[i][j]["bg"] == "gray" and buttons[i][j] not in mine_coordinates:
                return False
    title_label.config(text="You Win!")
    # showing player the position of the mines
    for x, y in mine_coordinates:
        buttons[x][y].config(text="X", bg="red")
    # disabling the buttons after the player has won
    for row in buttons:
        for button in row:
            button.config(state="disabled")
    return True

# function that reveals the empty spaces and numbers around the clicked button and around the empty bordering buttons and so on
def reveal(i, j):
    if (i, j) in numbers_coordinates:
        buttons[i][j].config(bg="white")
        buttons[i][j].config(text=str(numbers_values_coordinates[i][j]))
        if str(numbers_values_coordinates[i][j]) == "1":
            buttons[i][j].config(fg="blue")
        elif str(numbers_values_coordinates[i][j]) == "2":
            buttons[i][j].config(fg="green")
        elif str(numbers_values_coordinates[i][j]) == "3":
            buttons[i][j].config(fg="red")
        elif str(numbers_values_coordinates[i][j]) == "4":
            buttons[i][j].config(fg="purple")
        elif str(numbers_values_coordinates[i][j]) == "5":
            buttons[i][j].config(fg="orange")
        else:
            buttons[i][j].config(fg="black")
        return
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
        if (i, j) in empty_spaces_coordinates:
            buttons[i][j].config(bg="white", text="")
            empty_spaces_coordinates.remove((i, j))
            tiles_to_check.append((i, j+1))
            tiles_to_check.append((i, j-1))
            tiles_to_check.append((i+1, j))
            tiles_to_check.append((i-1, j))
        elif (i, j) in numbers_coordinates:
            buttons[i][j].config(bg="white")
            buttons[i][j].config(text=str(numbers_values_coordinates[i][j]))
            if str(numbers_values_coordinates[i][j]) == "1":
                buttons[i][j].config(fg="blue")
            elif str(numbers_values_coordinates[i][j]) == "2":
                buttons[i][j].config(fg="green")
            elif str(numbers_values_coordinates[i][j]) == "3":
                buttons[i][j].config(fg="red")
            elif str(numbers_values_coordinates[i][j]) == "4":
                buttons[i][j].config(fg="purple")
            elif str(numbers_values_coordinates[i][j]) == "5":
                buttons[i][j].config(fg="orange")
            else:
                buttons[i][j].config(fg="black")
        else:
            pass
        tiles_to_check.pop(0)
        check_win()

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
        numbers_values_coordinates.append([])
        for j in range(num_of_columns):
            if (i, j) not in mine_coordinates:
                mines = 0
                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        if x >= 0 and x < num_of_rows and y >= 0 and y < num_of_columns and (x, y) in mine_coordinates:
                            mines += 1
                if mines > 0:
                    numbers_values_coordinates[i].append(mines)
                    numbers_coordinates.append((i, j))
                else:
                    numbers_values_coordinates[i].append(0)
            else:
                numbers_values_coordinates[i].append(0)

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

# function to create the buttons for the game board
def create_board():
    global buttons
    for i in range(num_of_rows):
        row = []
        for j in range(num_of_columns):
            button = tkinter.Button(game_frame, width=buttons_size, height=int(buttons_size/2), bg="gray", relief="raised", command=lambda i=i, j=j: click(i, j), activebackground="gray")
            button.grid(row=i, column=j)
            row.append(button)
        buttons.append(row)

# function for the flag button
def flagging(flag_button):
    global is_flag_on
    if flag_button["text"] == "Flag Off":
        flag_button.config(text="Flag On", bg="red")
        is_flag_on = True
    else:
        flag_button.config(text="Flag Off")
        flag_button.config(bg="black")
        is_flag_on = False

# variables for the game
num_of_mines = 15
num_of_rows = 15
num_of_columns = 15
buttons = []
mine_coordinates = []
numbers_coordinates = []
numbers_values_coordinates = []
empty_spaces_coordinates = []
is_flag_on = False

# creating the main window
window = tkinter.Tk()
window.title("Minesweeper")
window.geometry("700x600")
window.resizable(False, False)
window.config(bg="black")
window.iconbitmap("Mine.ico")

# size variables
title_size = window.winfo_height() // 20
info_label_size = window.winfo_height() // 30
settings_restart_size = window.winfo_height() // 40
buttons_size = window.winfo_height() // num_of_rows //12

# creating a label for the title of the game
title_label = tkinter.Label(window, text="Minesweeper", font=("Helvetica", title_size), bg="black", fg="white")
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
info_label = tkinter.Label(control_frame, text="Info label", font=("Helvetica", info_label_size), bg="black", fg="white")
info_label.grid(row=0, column=0, columnspan=2)

# creating a  button for flagging the mines
flag_button = tkinter.Button(control_frame, text="Flag Off", font=("Helvetica", settings_restart_size), bg="black", fg="white", width=int(settings_restart_size/2), command=lambda: flagging(flag_button), activebackground="black", activeforeground="white")
flag_button.grid(row=1, column=0)

# creating a restart button
restart_button = tkinter.Button(control_frame, text="Restart", font=("Helvetica", settings_restart_size), bg="black", fg="white", command=lambda: restart(), width=int(settings_restart_size/2), activebackground="black", activeforeground="white")
restart_button.grid(row=1, column=1)

# creating a settings button
settings_button = tkinter.Button(control_frame, text="Settings", font=("Helvetica", settings_restart_size), bg="black", fg="white", command=lambda: settings(), width=int(settings_restart_size/2), activebackground="black", activeforeground="white")
settings_button.grid(row=2, column=1)

# starting a new game
new_game()

window.mainloop()
