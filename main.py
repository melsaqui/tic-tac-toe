from tkinter import*
from Cell import Cell
from Game import Game
class View:
    root = Tk()

    def __init__(self):
        self.root.configure(bg='#1A1825')
        self.root.geometry('450x460')
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False,False)
        self.menu_frame=Frame(self.root, bg='#042028', width="400",height="400")
        btn_3_auto=Button(self.menu_frame,bg="#054456",fg="white",text="3x3 Single Player Game!",font=20, command=lambda: self.setup(size=3,auto=True))
        btn_3_auto.place(relx=0.5,rely=0.2,anchor=CENTER)
        btn_5_auto=Button(self.menu_frame,bg="#054456",fg="white",text="5x5 Single Player Game!",font=20, command=lambda: self.setup(size=5,auto=True))
        btn_5_auto.place(relx=0.5,rely=0.4,anchor=CENTER)

        btn_3_not_auto=Button(self.menu_frame,bg="#054456",fg="white",text="3x3 Multiplayer Game!",font=20, command=lambda: self.setup(size=3,auto=False))
        btn_3_not_auto.place(relx=0.5,rely=0.6,anchor=CENTER)
        btn_5_not_auto=Button(self.menu_frame,bg="#054456",fg="white",text="5x5 Multiplayer Game!",font=20, command=lambda: self.setup(size=5,auto=False))
        btn_5_not_auto.place(relx=0.5,rely=0.8,anchor=CENTER)
      
        
        self.menu_frame.place(relx=0.5,rely=0.5,anchor=CENTER)
        self.root.mainloop()


    def setup(self,size,auto):
        self.menu_frame.place_forget()
        header_frame=Frame(self.root, width=450,height = 30)
        game_frame = Frame(self.root,width=450,height=450)
        game_frame.pack(expand=True,fill="both")
        
        heading = Label(header_frame, justify="center")
        heading.place(relx=0.5,rely=0.5,anchor=CENTER)
        header_frame.place(x=1,rely=0.01)
        game_frame.place(relx=0.5, rely=0.55,anchor=CENTER)
        Game(game_frame,self.root,heading,size,auto)
        
v=View()