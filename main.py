from tkinter import*
from Cell import Cell
from Game import Game
class View:
    root = Tk()

#background color
    def __init__(self):
        self.root.configure(bg='#1A1825')
        self.root.geometry('450x460')
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False,False)
        self.menu_frame=Frame(self.root, bg='#042028', width="400",height="400")
        btn_3=Button(self.menu_frame,bg="#054456",fg="white",text="3x3 Game!",font=20, command=lambda: self.setup(size=3))
        btn_3.place(relx=0.5,rely=0.4,anchor=CENTER)

        btn_5=Button(self.menu_frame,bg="#054456",fg="white",text="5x5 Game!",font=20, command=lambda: self.setup(size=5))
        btn_5.place(relx=0.5,rely=0.6,anchor=CENTER)
        self.menu_frame.place(relx=0.5,rely=0.5,anchor=CENTER)
        self.root.mainloop()


    def setup(self,size):
        self.menu_frame.place_forget()
        header_frame=Frame(self.root, width=450,height = 30)
        game_frame = Frame(self.root,width=450,height=450)
        game_frame.pack(expand=True,fill="both")
        
        heading = Label(header_frame, justify="center")
        heading.place(relx=0.5,rely=0.5,anchor=CENTER)
        header_frame.place(x=1,rely=0.01)
        game_frame.place(relx=0.5, rely=0.55,anchor=CENTER)
        Game(game_frame,self.root,heading,size)
        
v=View()