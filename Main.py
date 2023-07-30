import time, random, math, os, platform, webbrowser
from tkinter import *
from pathlib import Path

Vowels = ['A','E','I','O','U','Y','Æ','Ï','Í','Å','Ø','É','Ə','Э','ʔ','Ō','Ẽ','Œ']
Consonants = ['T','D','F','G','H','Þ','P','K','W','R','L','Z','S','J','N','M','B','X','V','Ð']


global paused
paused = False
global tick
tick = 0.3
global mutationRate
mutationRate = 0.1
global foodRate
foodRate = 20
creatures = {}
food = {}


decimalToFractionBase10 = lambda d : str((d*100))+'/100'  ## coverts decimal to x/100 fraction

def rgbHex(r, g, b): ## coverts rgb to Hexadecimal, returns #rrggbb
    Hex = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    print(Hex)
    return Hex

def updateSettings(): ## Update the settings, called when settings window closes
    global mutationRate
    global foodRate
    mutationRate = Mutationscroll.get()/100
    foodRate = Foodscroll.get()
    settingsWindow.destroy()

def openSettings(): ## Open settings window, called when settings pressed in menu
    global settingsWindow
    settingsWindow = Toplevel()
    ## mutation rate
    global Mutationscroll
    Label(settingsWindow, text='Mutation Rate').grid(row=1, column=1)
    Mutationscroll = Scale(settingsWindow,from_=0, to=100,orient=HORIZONTAL)
    Mutationscroll.grid(row=1, column=2)

    ## food growth rate
    global Foodscroll
    Label(settingsWindow, text='Food Growth Rate').grid(row=2, column=1)
    Foodscroll = Scale(settingsWindow, from_=1, to=100, orient=HORIZONTAL)
    Foodscroll.grid(row=2, column=2)

    exitButton = Button(settingsWindow, text='Save & Close', command=updateSettings)
    exitButton.grid(row=3, column=1)
    settingsWindow.mainloop()

def updateStats(): ## updates stats menu, called when stats opened
    global mutationRate
    global statsMenu
    for i in range(1,3):
        statsMenu.delete(0, 'end')
    statsMenu.add_command(label='Refresh', command=updateStats)
    statsMenu.add_command(label=('Paused: ' + str(paused)))
    statsMenu.add_command(label=('Mutation Rate: ' + decimalToFractionBase10(mutationRate)))
    statsMenu.add_command(label='Food Growth Rate: ' + str(foodRate))

def openInstructions(): ## opens the instructions in google chrome
    position = str(Path.cwd())
    position.replace("\\", '/')
    url = position + '/Evolution/instructions.txt'
    Operator = platform.system()
    if Operator == 'Windows':
        webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open(url)
    elif Operator == 'Darwin':
        webbrowser.get('open -a /Applications/Google\ Chrome.app %s').open(url)
    elif Operator == 'Linux':
        webbrowser.get('/usr/bin/google-chrome %s').open(url)

def drawCreature(x, y, s, color): ## x position, y position, size, color(hex)
    s = s * 3
    x0 = x + s
    x1 = x - s
    y0 = y + s
    y1 = y - s
    worldVisual.create_oval(x0, y0, x1, y1, fill=color)

def pauseUnpause(): ## pauses or unpauses sim, called when pause button clicked
    global paused
    if paused:
        paused = False
    else:
        paused = True

def loop():
    time.sleep(tick)
    global paused
    if not paused:
        for creature in list(creatures.keys()):
            print(creature)

def startWorld(number):
    for i in range(number):
        creatures[Consonants[number]] = {}
        c = creatures[Consonants[number]]
        c['genes'] = {}
        c['genes']['r'] = random.randrange(0, 255)
        c['genes']['g'] = random.randrange(0, 255)
        c['genes']['b'] = random.randrange(0, 255)
        c['genes']['growth'] = random.choice(['L', 'X', 'S', 'T'])
        c['genes']['metabolism'] = random.randrange(1, 5)
        c['size'] = 1
        c['color'] = rgbHex(c['genes']['r'], c['genes']['g'], c['genes']['b'])
        c['capacity'] = 3

def grow(Gtype, age): ## grows by the age of the creature
    newSize = age
    if Gtype == 'L':
        newSize = math.log(newSize + 1)
    elif Gtype == 'S':
        newSize = math.sqrt(newSize)/5
    elif Gtype == 'X':
        newSize = (newSize/7)-(newSize/8)
    elif Gtype == 'T':
        newSize = math.tanh(newSize)
    return newSize



window = Tk()
## wigets
window.title('Evolution sim')
menu = Menu(window)
window.config(menu=menu)
mainFrame = Frame(window)
fileMenu = Menu(menu)
menu.add_cascade(label='📁File', menu=fileMenu)
fileMenu.add_command(label='New')
fileMenu.add_command(label='Load')
fileMenu.add_separator()
fileMenu.add_command(label='Quit', command=window.quit)
menu.add_cascade(label='⚙Settings', command=openSettings)
statsMenu = Menu(menu)
statsMenu.add_command(label = 'Refresh', command=updateStats)
statsMenu.add_command(label=('Paused: ' + str(paused)))
statsMenu.add_command(label=('Mutation Rate: ' + decimalToFractionBase10(mutationRate)))
statsMenu.add_command(label='Food Growth Rate: ' + str(foodRate))
menu.add_cascade(label='📊Statistics', menu=statsMenu)
helpMenu = Menu(menu)
helpMenu.add_command(label='Instuctions', command=openInstructions)
menu.add_cascade(label='🔎Help', menu=helpMenu)
worldVisual = Canvas(window, width=500, height=500)
worldVisual.grid(column=1, row=1)
pausebutton = Button(window, text='Pause', command=pauseUnpause)
pausebutton.grid(row=2, column=1)




## end wigets
window.mainloop()