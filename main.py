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

        title_lb = Label(img2,text="Face Recognition Attendence System Software",font=("Times New Roman"),bg="Black",fg="Red")
        title_lb.place(x=0,y=0,width=1530,height=45)


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()

