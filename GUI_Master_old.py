import tkinter as tk
from tkinter import ttk, LEFT, END
from PIL import Image , ImageTk 
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import time
import sqlite3
#import tfModel_test as tf_test
global fn
fn=""
##############################################+=============================================================
root = tk.Tk()
root.configure(background="seashell2")
#root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("MAIN PAGE")


#430
#++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 =Image.open('11.png')
image2 =image2.resize((750,790), Image.LANCZOS)

background_image=ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0) #, relwidth=1, relheight=1)
#




frame_alpr = tk.LabelFrame(root, text="  ", width=750, height=850, bd=5, font=('times', 14, ' bold '),bg="white")
frame_alpr.grid(row=0, column=0)
frame_alpr.place(x=850, y=0)

image2 =Image.open('logo.png')
image2 =image2.resize((140,120), Image.LANCZOS)

background_image=ImageTk.PhotoImage(image2)
background_label = tk.Label(frame_alpr, image=background_image)

background_label.image = background_image

background_label.place(x=250, y=25)

lbl = tk.Label(frame_alpr, text="Phishing URL Detection", font=('Times New Roman', 35,' bold '),bg="white",fg="black")
lbl.place(x=140, y=180)


logo_label=tk.Label()
logo_label.place(x=0,y=55)


logo_label1=tk.Label(text='___Phishing Website Detection __ \n "Phishing is a multifaceted type \n of attack, aimed at collecting\n usernames and passwords,\n personal information , or,\n sometimes both"',compound='bottom',font=("Times New Roman", 20, 'bold', 'italic'),width=35, bg="#cce6ff", fg="black")
#logo_label=tk.Label(height=500, width=400)
logo_label1.place(x=950,y=550)


def login():

    from subprocess import call
    call(["python", "Login.py"])  
   



#################################################################################################################


def register():

    from subprocess import call
    call(["python", "registration.py"])  

def Ro():

    from subprocess import call
    call(["python", "rosmware.py"])  
   
def window():
    root.destroy()

button1 = tk.Button(frame_alpr, text=" SIGN UP ",command=register,width=15, height=1, font=('times', 15, ' bold '),bg="#3BB9FF",fg="black")
button1.place(x=200, y=350)

button2 = tk.Button(frame_alpr, text="LOGIN",command=login,width=15, height=1, font=('times', 15, ' bold '),bg="#3BB9FF",fg="black")
button2.place(x=200, y=450)




#




root.mainloop()