import tkinter as tk

def klik():
    print("Gumb je kliktnut, pozdrav iz konzole.")

prozor=tk.Tk()
prozor.title("Vježba")
prozor.geometry('300x200+100+100')
poruka = tk.Label(prozor, text = 'Pozdrav 4a!',bg='light blue',font='Calibri')
gumb=tk.Button(prozor, text = 'Klikni me',bg='pink',command=klik,font='calibri')
prozor.config(bg = 'light pink')

poruka.pack()
gumb.pack()
prozor.mainloop()

