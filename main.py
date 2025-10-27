#import the libraries

from tkinter import * #imports all the modules from the tkinter label,button,textbox

from tkinter import ttk #imports themed tkinter module which provides the modern widgets

from PIL import Image , ImageTk #these are used to work with the images 

#Image -> for open,manipulate and save
#ImageTk -> Used to convert PIL images into Tkinter-compatible format (so they can be displayed in a GUI).


class Face_Recognition_System:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        #upper image
        img1 = Image.open(r"C:\repo\Facial-Recognition-Attendance\face_bg.webp")
        img1 = img1.resize((1530,200))
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl1 = Label(self.root,image=self.photoimg1)
        f_lbl1.place(x=0,y=0,width=1530,height=200)

      


        #lower image
        #inorder to place the image in our screen we have to use the Image.open()
        img2 = Image.open(r"C:\repo\Facial-Recognition-Attendance\bg2.jpg")
        img2 = img2.resize((1530,590))
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl2 = Label(self.root,image=self.photoimg2)
        f_lbl2.place(x=0,y=200,width=1530,height=590)

        #text on the top of the lower image

        title_lb = Label(f_lbl2,text="Face Recognition Attendance System Software",font=("Times New Roman",40,"bold"),bg="Black",fg="White")
        title_lb.place(x=0,y=0,width=1530,height=45)

        #student button
        btn1 = Button(self.root,text="Student",cursor="hand2",font=("Times New Roman",10,"bold"),bg="Black",fg="White")
        btn1.place(x=220,y=300,width=100,height=50)

        #face detector
        btn2 = Button(self.root,text="Face Detector",cursor="hand2")
        btn2.place(x=400,y=300,width=100,height=50)

        #Attendence
        btn3 = Button(self.root,text="Attendance",cursor="hand2")
        btn3.place(x=620,y=300,width=100,height=50)

        #train
        btn4 = Button(self.root,text="Train Data",cursor="hand2")
        btn4.place(x=800,y=300,width=100,height=50)

        #Photos of Face Button
        btn5 = Button(self.root,text="Photos",cursor="hand2")
        btn5.place(x=1020,y=300,width=100,height=50)

        #Exit button
        btn6=Button(self.root,text="Exit",cursor="hand2")
        btn6.place(x=1200,y=300,width=100,height=50)








if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()

