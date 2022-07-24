# Importing Useful modules
from tkinter import *
from tkinter.messagebox import showinfo, askyesno
from tkinter.colorchooser import askcolor


root = Tk()

# Variables to store previous and next x, y points to draw shapes
previousX = 0
previousY = 0

currentX = 0
currentY = 0

# Varibale for storing the id of shapes
shape_id = 0


# Defining the background and outline colors
bgColor = "white"
outlineColor = "black"

# Storing Current Tool Selection (Default =)

currentTool = StringVar()
currentTool.set("Brush")


# Function to change color


def changeBgColor():
	global bgColor
	colors = askcolor(title="Choose Color")
	bgColor = colors[1]
	print(f"Background Color set to {bgColor}")


def changeOutlineColor():
	global outlineColor
	colors = askcolor(title="Choose Color")
	outlineColor = colors[1]
	print(f"Outline Color set to {outlineColor}")


# Function to clear the whole canvas
def clearCanvas():
	action = askyesno("Delete", "Are You sure you want to clear all canvas. This action cannot be undo.")
	print(action)
	if action:
		canvas.delete("all")
		print("Canvas Cleared Successfully")



# When user click the left click from mouse it will store the position x, y where user clicked
def leftClick(event):
	# global shape_id
	# if currentTool.get() == "Move":
	# 	canvas.coords(shape_id, event.x, event.y, event.x+10, event.y+10)
	global previousX
	global previousY
	print(f"Left Click: X={event.x}, Y={event.y}")
	previousX = event.x
	previousY = event.y
	# print(f"Shape Id: {shape_id}")



# When user release left mouse button it will store new x, y position to new variable
def leftRelease(event):
	global currentX
	global currentY
	currentX = event.x
	currentY = event.y
	global shape_id
	print(f"Previous Points X={previousX}, Y={previousY}")
	print(f"Next Points X={currentX}, Y={currentY}")

	# Checking the current tool and drawing the specific shapes

	# If user selected Circle Tool
	if currentTool.get() == "Circle":
		shape_id = canvas.create_oval(previousX, previousY, currentX, currentY, fill=bgColor)

	# If User Selected Line Tool
	elif currentTool.get() == "Line":
		shape_id = canvas.create_line(previousX, previousY, currentX, currentY, fill=outlineColor)

	# If user selected Rectangle Tool
	elif currentTool.get() == "Rectangle":
		shape_id = canvas.create_rectangle(previousX, previousY, currentX, currentY, fill=bgColor)

	# If user selected Text Tool
	elif currentTool.get() == "Text":
		shape_id = canvas.create_text(currentX, currentY, text="Hussnain")

# If User Selected the Line tool
def lineChange():
	canvas.config(cursor="crosshair")
	global currentTool
	currentTool.set("Line")
	statusBar.update()

# If User Selected the Rectangle Tool
def rectangleChange():
	canvas.config(cursor="crosshair")
	global currentTool
	currentTool.set("Rectangle")
	statusBar.update()


# If user selected Text Tool
def textChange():
	canvas.config(cursor="xterm")
	global currentTool
	currentTool.set("Text")
	statusBar.update()


# If User Selected the Circle tool
def circleChange():
	print("Circle Selected")
	canvas.config(cursor="crosshair")
	global currentTool
	currentTool.set("Circle")
	statusBar.update()


# If User Select the Brush tool
def dotChange():
	print("Dot Selected")
	canvas.config(cursor="dot")
	currentTool.set("Brush")
	statusBar.update()


# If User selected Move Tool
def moveChange():
	print("Move Selected")
	canvas.config(cursor="fleur")
	currentTool.set("Move")
	statusBar.update()

# Functions for Move Tools
def left(e):
   x = -20
   y = 0
   canvas.move(img, x, y)

def right(e):
   x = 20
   y = 0
   canvas.move(img, x, y)

def up(e):
   x = 0
   y = -20
   canvas.move(img, x, y)

def down(e):
   x = 0
   y = 20
   canvas.move(img, x, y)


def moveTest(event):
	if currentTool.get() == "Move":
		global shape_id
		if shape_id is not None:
			coord = canvas.coords(shape_id)
			print(coord)
			width = coord[2] - coord[0]
			height = coord[3] - coord[1]
			if currentTool.get() == "Move":
				canvas.coords(shape_id, event.x, event.y, event.x+width, event.y+height)
	elif currentTool.get() == "Brush":
		print("BRUSH!")
		x1=event.x
		y1=event.y
		x2=event.x
		y2=event.y
		canvas.create_line(x1, y1, x2, y2, fill="black", width=5.5, capstyle=ROUND, smooth=TRUE, splinesteps=36)
	

root.title("Drawing Board")
root.geometry("600x300")

# Tools Menu
editingFrame = Frame(root, bd=2, relief="groove", padx=10, pady=10)
editingFrame.pack()

moveButton = Button(editingFrame, text="Move", command=moveChange)
moveButton.pack()

dotButton = Button(editingFrame, text="Dot", command=dotChange)
dotButton.pack()

circleButton = Button(editingFrame, text="Circle", command=circleChange)
circleButton.pack()

lineButton = Button(editingFrame, text="Line", command=lineChange)
lineButton.pack()

rectangleButton = Button(editingFrame, text="Rectangle", command=rectangleChange)
rectangleButton.pack()


textButton = Button(editingFrame, text="Text", command=textChange)
textButton.pack()

editingLabel = Label(editingFrame, text="Tools")
editingLabel.pack(side="bottom")



# Actions Menu
actionFrame = Frame(root, bd=2, relief="groove", padx=10, pady=10)

deleteButton = Button(actionFrame, text="Clear All", command=clearCanvas)
deleteButton.pack()

bgButton = Button(actionFrame, text="Background Color", command=changeBgColor)
bgButton.pack()

outlineButton = Button(actionFrame, text="Outline Color", command=changeOutlineColor)
outlineButton.pack()

actionLabel = Label(actionFrame, text="Actions")
actionLabel.pack(side="bottom")
actionFrame.pack()


canvas = Canvas(root, bg="white", width=1500, height=200, highlightcolor="yellow", cursor="dot")



# Left Click Function
canvas.bind("<ButtonPress-1>", leftClick)


# Left Release Function
canvas.bind("<ButtonRelease-1>", leftRelease)


canvas.bind("<B1-Motion>", moveTest)

canvas.pack(expand=YES, fill=BOTH)

statusBar = Frame(root, relief='groove', borderwidth=5)
currentToolLabel = Label(statusBar, textvariable=currentTool)
currentToolLabel.pack()
statusBar.pack(side=BOTTOM, fill=BOTH)


root.mainloop()