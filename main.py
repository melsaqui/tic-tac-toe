from tkinter import*
from Game import Game
import sys
class View:
    root = Tk()

    def __init__(self):
        self.root.configure(bg='#1A1825')
        self.root.geometry('500x510')
        self.root.title("Tic-Tac-Toe")
        #self.root.resizable(False,False)
        self.menu()
       
        self.root.mainloop()
    def menu(self):
        self.menu_frame=Frame(self.root, bg='#042028', width="470",height="470")
        lbl_title=Label(self.menu_frame,bg="#054456",text="Tic-Tac-Toe",font=50,fg="white",width=400,pady=5)
        lbl_title.place(relx=0.5,rely=0.1,anchor=CENTER)

        btn_3_auto=Button(self.menu_frame,bg="#054456",fg="white",text="3x3 Single Player!",width=17,font=15, command=lambda: self.setup(size=3,auto=True))
        btn_3_auto.place(relx=0.48,rely=0.3,anchor=E)
        btn_5_auto=Button(self.menu_frame,bg="#054456",fg="white",text="5x5 Single Player!" ,width=17,font=15, command=lambda: self.setup(size=5,auto=True))
        btn_5_auto.place(relx=0.48,rely=0.45,anchor=E)
        btn_10_auto=Button(self.menu_frame,bg="#054456",fg="white",text="10x10 Single Player!",width=17,font=20, command=lambda: self.setup(size=10,auto=True))
        btn_10_auto.place(relx=0.48,rely=0.6,anchor=E)
        btn_3_not_auto=Button(self.menu_frame,bg="#054456",fg="white",text="3x3 Multiplayer!",width=17,font=20, command=lambda: self.setup(size=3,auto=False))
        btn_3_not_auto.place(relx=0.52,rely=0.3,anchor=W)
        btn_5_not_auto=Button(self.menu_frame,bg="#054456",fg="white",text="5x5 Multiplayer!",width=17,font=20, command=lambda: self.setup(size=5,auto=False))
        btn_5_not_auto.place(relx=0.52,rely=0.45,anchor=W)
        btn_10_not_auto=Button(self.menu_frame,bg="#054456",fg="white",text="10x10 Multiplayer!",width=17,font=20, command=lambda: self.setup(size=10,auto=False))
        btn_10_not_auto.place(relx=0.52,rely=0.6,anchor=W)
      
        btn_exit=Button(self.menu_frame,bg="#054456",fg="white",text="Exit Game",font=20, command=exit)
        btn_exit.place(relx=0.5,rely=0.75,anchor=CENTER)

        self.menu_frame.place(relx=0.5,rely=0.5,anchor=CENTER)
    def exit():
        sys.exit()

    def setup(self,size,auto):
        self.menu_frame.place_forget()
        self.header_frame=Frame(self.root, width=450)
        self.game_frame = Frame(self.root,width=450,height=100)
        
        heading = Label(self.header_frame, justify="center",font=10)
        heading.place(relx=0.5,rely=0.5,anchor=CENTER)
        self.header_frame.place(x=1,rely=0.01,relwidth=1, relheight=0.08)
        self.game_frame.place(relx=0.5, rely=0.55, relwidth=1, relheight=0.8,anchor=CENTER)

        Game(self.game_frame,self.root,heading,size,self,auto)
    
    def reset(self):
        self.game_frame.place_forget()
        self.header_frame.place_forget()
        self.menu()
v=View()