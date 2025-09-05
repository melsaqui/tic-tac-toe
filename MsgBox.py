from tkinter import *
from tkinter import messagebox
#from View import View
class MsgBox:
   def __init__(self):
      pass
   def trigger(self, winner=""):
      if winner=="":
          answer = messagebox.askyesno("Question","The Game ended in a draw. Want to play again?")

      else: answer = messagebox.askyesno("Question","Congratulations player "+winner.role+"!. Do You want to play again")
      return answer
      #if answer:
        # View()



 
