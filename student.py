from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk

class Student:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Student")

         #upper image
        img1 = Image.open(r"C:\repo\Facial-Recognition-Attendance\face_bg.webp")
        img1 = img1.resize((1530,790))
        self.img1 = ImageTk.PhotoImage(img1)

        label1 = Label(self.root,image=self.img1)
        label1.place(x=0,y=0,width=1530,height=200)

        #left label frame
        left_frame = LabelFrame(self.root,text="Student Details",bd = 2,relief=RIDGE)
        left_frame.place(x=8,y=200,width=730,height=580)

        #right label frame
        right_frame = LabelFrame(self.root,text="Student Details",bd=2,relief=RIDGE)
        right_frame.place(x=750,y=200,width=730,height=580)



if __name__=="__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()