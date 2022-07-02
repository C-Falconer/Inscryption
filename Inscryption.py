import serial
import tkinter as tk
from PIL import ImageTk, Image

cardHealth = []
cardDamage = []

#Define the tkinter instance
win = tk.Toplevel()
win.title("Rounded Button")

#Define the size of the tkinter frame
win.geometry("700x300")

#Define the working of the button

def my_command():
   text.config(text= "You have clicked Me...")

#Import the image using PhotoImage function
click_btn= ImageTk.PhotoImage(Image.open("Rock.png"))

#Let us create a label for button event
#img_label= tk.Label(image=click_btn)

#Let us create a dummy button and pass the image
button= tk.Button(win, image=click_btn,command= my_command,
borderwidth=0)
button.pack(pady=30)

text= tk.Label(win, text= "")
text.pack(pady=30)

win.mainloop()

def connect():
    arduino = serial.Serial()
    arduino.port = 'COM15'
    arduino.baudrate = 9600
    arduino.open()
    return arduino


def main():
    arduino = connect()
    while True:
        data = arduino.readline()
        print(data)
    
    
main()