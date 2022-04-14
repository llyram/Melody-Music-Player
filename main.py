import os
from tkinter import *
import tkinter.messagebox
from pygame import mixer #to play music
from tkinter import filedialog

root = Tk() #create window object

#create the menubar 
menubar = Menu(root)
root.config(menu = menubar)

def browse_file():
    global filename
    filename = filedialog.askopenfilename()

#create submenu
subMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "File", menu = subMenu)
subMenu.add_command(label = "Open", command = browse_file)
subMenu.add_command(label = "Exit", command = root.destroy)

def about_us():
    tkinter.messagebox.showinfo('Ablout Melody', 'Music player developed using python')


subMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Help", menu = subMenu)
subMenu.add_command(label = "About us", command = about_us)

mixer.init() #initializing mixer


root.title("Melody")            #set window title
#everything inside the window is a widget

fileLabel = Label(root, text = 'Lets make some noise!')#Label widget to show text(and other widgets)
fileLabel.pack(pady = 10) #Need to pack widgets so that they show up in the window

lengthLabel = Label(root, text = 'Total length - 0:00')
lengthLabel.pack()


#photoImage widget for photos DUH!
playPhoto = PhotoImage(file = 'images/play.png')
stopPhoto = PhotoImage(file = 'images/stop.png')
pausePhoto = PhotoImage(file = 'images/pause.png')
rewindPhoto = PhotoImage(file = 'images/rewind.png')
mutePhoto = PhotoImage(file = 'images/mute.png')
volumePhoto = PhotoImage(file = 'images/volume.png')

def show_details():
    fileLabel['text'] = "Playing" + " - " + os.path.basename(filename)

    a = mixer.Sound(filename)
    total_Length = a.get_length() # get_length() function gets the lenght of the music file
    mins, secs = divmod(total_Length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformart = '{:02d}:{:02d}'.format(mins, secs)
    lengthLabel['text'] = "Total Length" + " - " + timeformart



def play_music():
    global paused

    if paused:
        paused = False
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
    else:
        try:
            mixer.music.load(filename)
            mixer.music.play()
            statusbar['text'] = "Playing music" + " " + os.path.basename(filename)
            show_details()
        except:
            tkinter.messagebox.showerror("File not Found", "Melody could not find the file please check again.")
        
    
def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music stopped"

paused = False

def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = "Paused"

def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume) 
    #set_volume of mixer takes vale only from 0 to 1.

def rewind_music(): 
    play_music()
    statusbar['text'] = "Music rewinded"

muted = False

def mute_music():
    global muted
    if muted:
        #Unmute the music
        mixer.music.set_volume(0.7)
        volume_btn.configure(image=volumePhoto)
        scale.set(70)
        muted = False
    else:
        #mute the music
        mixer.music.set_volume(0)
        volume_btn.configure(image=mutePhoto)
        scale.set(0)
        muted = True

#middleframe created
middleframe = Frame(root)
middleframe.pack(padx=30, pady=30)

## All buttons in the window are defined below
#BUTTON!! parameters are window, image/text, command
play_btn = Button(middleframe, image = playPhoto, command = play_music)
play_btn.grid(row=0, column=0)

stop_btn = Button(middleframe, image = stopPhoto, command = stop_music)
stop_btn.grid(row=0, column=1)

pause_btn = Button(middleframe, image = pausePhoto, command = pause_music)
pause_btn.grid(row=0, column=2)

#Bottom frame created
bottomframe = Frame(root)
bottomframe.pack()

rewind_btn = Button(bottomframe, image = rewindPhoto, command = rewind_music)
rewind_btn.grid(row=0, column=0)

volume_btn = Button(bottomframe, image = volumePhoto, command = mute_music)
volume_btn.grid(row=0, column=1)


#Volume scale
scale = Scale(bottomframe, from_ = 0, to = 100, orient = HORIZONTAL, command = set_vol)
scale.set(100)
set_vol(100)
scale.grid(row=0, column=2, pady=15, padx=30)

#Statusbar
statusbar = Label(root, text="Welcome to melody", relief = SUNKEN, anchor = W)
statusbar.pack(side = BOTTOM, fill = X)

#put the windown in infinite loop so that it is persistant on the screen
root.mainloop() 