# Importing Useful modules
from tkinter import *
from tkinter.messagebox import showinfo, askyesno
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename
from PIL import ImageGrab

root = Tk()

# Variables to store previous and next x, y points to draw shapes
previousX = 0
previousY = 0

currentX = 0
currentY = 0

# Varibale for storing the id of latest drawing shape
shape_id = None

# Defining the background and outline colors
bgColor = "white"
outlineColor = "black"

# Storing Current Tool Selection (Default = BRUSH)
currentTool = StringVar()
currentTool.set("Brush")


# Function to change bg color
def changeBgColor():
	global bgColor
	colors = askcolor(title="Choose Color")
	bgColor = colors[1]
	print(f"Background Color set to {bgColor}")
	bgFrame.config(bg=bgColor)

# Function when user want to quit the software
def quit():
	global shape_id
	if shape_id is not None:
		option = askyesno("Quit", "You have unsaved work are you sure you want to quit ?")
		if option:
			root.destroy()
	else:
		root.destroy()

# Function to change outline color
def changeOutlineColor():
	global outlineColor
	colors = askcolor(title="Choose Color")
	outlineColor = colors[1]
	print(f"Outline Color set to {outlineColor}")
	outlineFrame.config(bg=outlineColor)


# Function to create new Window
def newWindow():
	global shape_id
	if shape_id is not None:
		option = askyesno("New Window", "You have unsaved work. Do You want to save it before creating a new canvas")
		if option:
			saveImage(canvas)
			canvas.delete("all")
		else:
			canvas.delete("all")
	else:
		canvas.delete("all")

	

# Function to show about info
def about():
	aboutInfo = f"Software is created by Psycho Coder"
	showinfo("About", aboutInfo)

# Function to save the image of the canvas
def saveImage(widget):
	global imageNumber
	x=root.winfo_rootx()+widget.winfo_x()
	y=root.winfo_rooty()+widget.winfo_y()
	x1=x+widget.winfo_width()
	y1=y+widget.winfo_height()
	fileType = [("PNG File", "*.png"),
	]
	fileName = asksaveasfilename(filetypes=fileType)
	print(f"File Name: {fileName}.png")
	ImageGrab.grab().crop((x,y,x1,y1)).save(f"{fileName}.png")
	showinfo("Done!", "You Photo has been saved successfully!")

# Function to clear the whole canvas
def clearCanvas():
	action = askyesno("Delete", "Are You sure you want to clear all canvas. This action cannot be undo.")
	print(action)
	if action:
		canvas.delete("all")
		print("Canvas Cleared Successfully")



# When user click the left click from mouse it will store the position x, y where user clicked
def leftClick(event):
	global previousX
	global previousY
	print(f"Left Click: X={event.x}, Y={event.y}")
	previousX = event.x
	previousY = event.y



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
def brushChange():
	print("Brush Selected")
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
# This will be useful when user wanted to move a shape using keyboard up, down, left, right buttons
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

# This function is used for drag event while click holding mouse button
# For Brushing Tool
# For Move Tool
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
		x1=event.x
		y1=event.y
		x2=event.x
		y2=event.y
		canvas.create_line(x1, y1, x2, y2, fill=outlineColor, width=5.5, capstyle=ROUND, smooth=TRUE, splinesteps=36)
	

root.title("Drawing Board")
root.geometry("600x300")

# Main Menu Bar
mainMenu = Menu(root)

# File Menu
fileMenu = Menu(mainMenu, tearoff=False)
fileMenu.add_command(label="New", command=newWindow)
fileMenu.add_separator()
fileMenu.add_command(label="Quit", command=quit)
mainMenu.add_cascade(label="File", menu=fileMenu)

# Help Menu
helpMenu = Menu(mainMenu, tearoff=False)
helpMenu.add_command(label="About", command=about)
mainMenu.add_cascade(label="Help", menu=helpMenu)

root.config(menu=mainMenu)

# Tools Menu
editingFrame = Frame(root, bd=2, relief="groove", padx=10, pady=10)
editingFrame.pack(side=TOP)

editingLabel = Label(editingFrame, text="Tools")
editingLabel.pack(side=TOP)

moveButton = Button(editingFrame, text="Move", command=moveChange)
moveButton.pack(side=LEFT, padx=10)

dotButton = Button(editingFrame, text="Brush", command=brushChange)
dotButton.pack(side=LEFT, padx=10)

circleButton = Button(editingFrame, text="Circle", command=circleChange)
circleButton.pack(side=LEFT, padx=10)

lineButton = Button(editingFrame, text="Line", command=lineChange)
lineButton.pack(side=LEFT, padx=10)

rectangleButton = Button(editingFrame, text="Rectangle", command=rectangleChange)
rectangleButton.pack(side=LEFT, padx=10)


textButton = Button(editingFrame, text="Text", command=textChange)
textButton.pack(side=LEFT, padx=10)


# Colors Menu
colorsFrame = Frame(root, bd=2, relief="groove", padx=10, pady=10)

colorsLabel = Label(colorsFrame, text="Colors")
colorsLabel.pack(side=TOP)

backgroundMainFrame = Frame(colorsFrame, padx=10, pady=10)
bgFrame = Frame(backgroundMainFrame, width=100, height=100, bg=bgColor)
bgFrame.pack()
bgButton = Button(backgroundMainFrame, text="Background Color", command=changeBgColor)
bgButton.pack()
backgroundMainFrame.pack(side=LEFT)


outlineMainFrame = Frame(colorsFrame, padx=10, pady=10)
outlineFrame = Frame(outlineMainFrame, width=100, height=100, bg=outlineColor)
outlineFrame.pack()
outlineButton = Button(outlineMainFrame, text="Outline Color", command=changeOutlineColor)
outlineButton.pack()
colorsFrame.pack()
outlineMainFrame.pack(side=LEFT)
# Actions Menu
actionFrame = Frame(root, bd=2, relief="groove", padx=10, pady=10)

actionLabel = Label(actionFrame, text="Actions")
actionLabel.pack(side=TOP)

deleteButton = Button(actionFrame, text="Clear All", command=clearCanvas)
deleteButton.pack(side=LEFT, padx=10)

saveButton = Button(actionFrame, text="Save", command=lambda:saveImage(canvas))
saveButton.pack(side=LEFT)

actionFrame.pack()

# Main Canvas where user draws anything
canvas = Canvas(root, bg="white", width=1500, height=200, highlightcolor="yellow", cursor="dot")

# Left Click Function
canvas.bind("<ButtonPress-1>", leftClick)

# Left Release Function
canvas.bind("<ButtonRelease-1>", leftRelease)

# When We click left mouse button the drag the mouse
canvas.bind("<B1-Motion>", moveTest)

canvas.pack(expand=YES, fill=BOTH)

# Status Bar
statusBar = Frame(root, relief='groove', borderwidth=5)
currentToolLabel = Label(statusBar, textvariable=currentTool)
currentToolLabel.pack()
statusBar.pack(side=BOTTOM, fill=BOTH)

# When user click close button it will prompt the user if he wants to quit because he has unsaved work on canvas
root.protocol("WM_DELETE_WINDOW", quit)
root.mainloop()