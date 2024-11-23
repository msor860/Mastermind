import tkinter as tk
import turtle
import random
import time
import sys

# initialization of the tkinter window
root = tk.Tk()
root.withdraw()

frame = tk.Frame(root)
canvas = tk.Canvas(frame, width=400, height=560, highlightthickness=0, highlightbackground="black", relief=tk.FLAT, bd=0)

#declaration of the list of the different colors of the game
#namely: yellow, blue, red, green, pink, dark blue (modifiable)
color_list = ['#ffd200', '#3cb4e6', '#ff0000', '#00ff00', '#e6007e', '#03234b']

#definition of the number of lines of play (nb lines test + 1 line result)
nbLinesSet = 11 #here 10 lines of play + 1 line result
#number of values to find per line
nbLineValues = 4 #here 4, so a combination of 4 colors 
#defining the size and spacing betweeen circles
sizeValue = 40
paddingValue = 50

row = 0
cpos = 0

#initialization of the score value
score = 0

colorpicks = [[-1 for i in range(nbLineValues)] for j in range(nbLinesSet)]

def take_player(username):
  global player
  player = username

def show_msg(msg):
  newPage3 = tk.Toplevel(root)
  newPage3.title ("Missing value")
  tk.Label(newPage3, text=msg, font=("Arial", 13, "bold")).pack(pady=10, padx=20)
  tk.Button(newPage3, text="Thanks for the information", command = newPage3.destroy).pack(pady=10)

#definitions of player actions
def userAction():
  canvas.unbind("<space>")
  canvas.bind('<Left>', lambda _ :selectPos(-1))
  canvas.bind('<Right>', lambda _ :selectPos(1))
  canvas.bind('<Up>', lambda _ :switchColor(1))
  canvas.bind('<Down>', lambda _ :switchColor(-1))
  canvas.bind('<Return>', lambda _ :switchrow())

def userInAction():
  canvas.unbind("<space>")
  canvas.unbind("<Left>")
  canvas.unbind("<Right>")
  canvas.unbind("<Up>")
  canvas.unbind("<Down>")
  canvas.unbind("<Return>")

# random generation of the color code to guess
#a color can appear maximum 1x per combination

def createCode():
  selection = [x for x in range(len(color_list))]
  code = []
  for i in range(nbLineValues):
    codeIndex = random.randint(0,len(selection)-1)
    code.append(selection[codeIndex])
    selection.pop(codeIndex)
  return code

codedColor=createCode()

def initRow():
  global selectColors, ColorAndPositionOK, OnlyColorOK
  selectColors = [x for x in range(len(color_list))]
  ColorAndPositionOK = 0
  OnlyColorOK = 0

#function that opens a window in case of defeat
#disappears automatically after 8 seconds, like the game window (return to menu)

def defeat():
  global row, ColorAndPositionOK, score, player
  newPage1 = tk.Toplevel(root)
  newPage1.title("DEFEATEATED")
  newPage1.geometry("400x350")
  score = 0

  newPage1.after(8000, newPage1.destroy)
#function that opens a window in case of victory
#disappears automatically after 8 seconds, like the game window (return to menu)

def win():
  global row, ColorAndPositionOK, score, player
  newPage = tk.Toplevel(root)
  newPage.title("VICTORY")
  newPage.geometry("400x350")
  score = 10 - row
  textV = 'BRAVO' + " You Won!!!"
  tk.Label(newPage, text = textV, font = ("Arial", 20, "bold")).pack(pady=(10))
  tk.Label(newPage, text="Your score is " + str(score) + ".").pack()
  newPage.after(8000, newPage.destroy)

#initialization of the game window
#each position circle to guess takes a white color and the cursor returns to the first line
def initGame():
  global row, cpos, colorpicks, codedColor
  canvas.itemconfig(board[row][cpos], width = 0)
  for i in range(nbLinesSet):
    for j in range(nbLineValues):
      canvas.itemconfig(board[i][j], fill='white')
      
      if i < nbLinesSet-1:
        canvas.itemconfig(response[i][j], fill='white') 
  colorpicks = [[-1 for i in range(nbLineValues)]for j in range(nbLinesSet)]
  row = 0
  cpos = 0
  canvas.itemconfig(board[row][cpos], width = 1)
  userAction()
  codedColor = createCode()
  initRow()


board = []
response = []

for i in range(nbLinesSet):
  newRow = []
  newResponse = []
  for j in range(nbLineValues):
    x = paddingValue * j + 5
    y = 550 - paddingValue * i - sizeValue - 5
    newRow.append(canvas.create_oval(x, y, x+sizeValue, y+sizeValue, fill='white', outline='black', width=0))

    if i < nbLinesSet - 1:
      x = paddingValue/2 * j + 255
      y += sizeValue / 8
      newResponse.append(canvas.create_oval(x + sizeValue/4, y + sizeValue/4, x + sizeValue/2, y + sizeValue/2, fill='white', outline = 'black', width = 0))
  board.append(newRow)
  if i < nbLinesSet-1:
    response.append(newResponse)

initGame()
canvas.itemconfig(board[row][cpos], width=1)

def select(colorPosition):
  canvas.itemconfig(colorPosition, width=5)

def deselect(colorPosition):
  canvas.itemconfig(colorPosition, width=0)

def setcolor(colorPosition, color):
    canvas.itemconfig(colorPosition, fill=color)

def selectPos(increment):
  global cpos
  canvas.itemconfig(board[row][cpos], width=0)
  cpos += increment
  if cpos < 0: cpos = nbLineValues - 1
  if cpos >= nbLineValues: cpos = 0
  canvas.itemconfig(board[row][cpos], width=1)

#function to change the color of the selected box
def switchColor(increment):
  colorpicks[row][cpos] += increment
  if colorpicks[row][cpos] > len(color_list) - 1:
    colorpicks[row][cpos] = 0
  if colorpicks[row][cpos] < 0:
    colorpicks[row][cpos] = len(color_list) - 1
  canvas.itemconfig(board[row][cpos], fill=color_list[colorpicks[row][cpos]])

def switchrow():
  global row, ColorAndPositionOK, OnlyColorOK, colorpicks
  for i in range(nbLineValues):
    if colorpicks[row][i] == -1 :
      show_msg ("Warning, a color was not entered on line {}, at position {}. Self destruct activated. The president has been given your location.".format(row + 1, i + 1))
      return False
    for j in range(nbLineValues):
      if (j == i and codedColor[j] == colorpicks[row][i]):
        ColorAndPositionOK += 1
      if (j != i and codedColor[j] == colorpicks[row][i]):
        OnlyColorOK += 1
  
  if ColorAndPositionOK < nbLineValues and row < nbLinesSet - 2:
    print("- Good color and good position: {} \n - Only the right color: {}".format(ColorAndPositionOK, OnlyColorOK))
    for i in range(ColorAndPositionOK):
      canvas.itemconfig(response[row][i], fill="green")
    for i in range(OnlyColorOK):
      canvas.itemconfig(response[row][i+ColorAndPositionOK], fill = "orange")
    canvas.itemconfig(board[row][cpos], width = 0)
    row += 1
    canvas.itemconfig(board[row][cpos], width = 1)
    initRow()
    return False
  else: #VICTORY or FINAL DEFEAT if ROW = 9
    print("Row {} \n - Right color and right position: {} \n - Only the right color: {}".format(row, ColorAndPositionOK, OnlyColorOK))
    output = True
    if row == nbLinesSet - 2:
      output = False
    for i in range(ColorAndPositionOK):
      canvas.itemconfig(response[row][i], fill="green")
    for i in range(OnlyColorOK):
      canvas.itemconfig(response[row][i + ColorAndPositionOK], fill="orange")
    for i in range(nbLineValues):
      canvas.itemconfig(board[nbLinesSet-1][i], fill=color_list[codedColor[i]])
    userInAction()
    # here we display the defeat or victory windows depending on the result
    if row == 9:
      if ColorAndPositionOK == 4:
        win()
      else:
        defeat()
    else:
      win()
      return output

def main_game():
  root.deiconify()
  frame.pack()
  canvas.pack()
  root.title("Current game - MASTERMIND")
  canvas.focus_set()
  userAction()
  canvas.bind("<space>",lambda _ : initGame())

  root.mainloop()

main_game()