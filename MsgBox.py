from tkinter import *
from tkinter import messagebox
class MsgBox:
   def __init__(self):
      pass
   def trigger(self,auto, winner=""):
      if winner=="":
          answer = messagebox.askyesno("Question","The Game ended in a draw. Want to play again?")

      elif winner!="" and not auto: 
         answer = messagebox.askyesno("Question","Congratulations player "+winner.role+"!. Do You want to play again")
      elif auto and winner.__class__.__name__ =="Computer":
         answer = messagebox.askyesno("Question","You Lost! Do You want to play again")
      else:
         answer = messagebox.askyesno("Question","Congratulations You won! Do You want to play again")
      return answer




 
