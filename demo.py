import solve
import tkinter as tk
from tkinter import Tk, BOTH
from tkinter.ttk import Frame, Button, Style
from tkinter import * 
root= tk.Tk()
root.title("TOÁN LỚP 3")
########################################################################
photo=PhotoImage(file="hinhAI.png")
canvas1 = tk.Canvas(root, width = 1050, height = 600,  relief = 'raised')
canvas1.pack()
canvas1.create_image(0, 0, image=photo, anchor=NW)
########################################################################

label2 = tk.Label(root, text='Mời bé nhập đề:')
label2.config(font=("helvetica", 20), bg='yellow', fg='black')
canvas1.create_window(525, 100, window=label2)
########################################################################
entry1 = tk.Entry(root)
canvas1.create_window(525, 140, window=entry1,width=900,height=40)
def getSquareRoot ():
    x1 = entry1.get()
    x2=tk.StringVar()
    x2=(solve.Solve(x1))
    label4 = tk.Label(root,text=x2,font=('helvetica', 10, 'bold'))
    canvas1.create_window(525, 260, window=label4)
def delete():
    #x2.set=("")
    entry1.delete(0,tk.END) 

button1 = tk.Button(text='Giải:', command=getSquareRoot, bg='yellow', fg='black', font=('helvetica', 12, 'bold'))
Button(root, text="Thoát", command=root.destroy,bg='yellow', fg='black', font=('helvetica', 12, 'bold')).pack()
Button( text="Reset", command=delete,bg='yellow', fg='black', font=('helvetica', 12, 'bold')).pack()
canvas1.create_window(525, 180, window=button1)
root.mainloop()
