from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter import messagebox,ttk

class sign_up:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # ========== Background Image ==========
        img_bg = Image.open(r"C:\repo\Facial-Recognition-Attendance\bg2.jpg")
        img_bg = img_bg.resize((800, 600))
        self.photoimg_bg = ImageTk.PhotoImage(img_bg)

        bg_label = Label(self.root, image=self.photoimg_bg)
        bg_label.place(relx=0.5, rely=0.5, anchor=CENTER, width=800, height=600)

        # ========== Title Bar ==========
        title_lb = Label(
            self.root,
            text="Face Recognition Attendance System",
            font=("Times New Roman", 38, "bold"),
            bg="black",
            fg="white"
        )
        title_lb.place(x=0, y=0, width=1530, height=70)

        # ========== Buttons (Directly on Root) ==========
        btn_font = ("Times New Roman", 15, "bold")

        # Student Sign-In
        btn_signup = Button(
            self.root,
            text="Student Sign-In",
            font=btn_font,
            bg="#0B0C10",
            fg="white",
            cursor="hand2",
            width=20,
            command=self.open_sign_up
        )
        btn_signup.place(relx=0.5, rely=0.45, anchor=CENTER)

        # Student Login
        btn_login = Button(
            self.root,
            text="Student/Admin Login",
            font=btn_font,
            bg="#1F2833",
            fg="white",
            cursor="hand2",
            width=20,
            command=self.open_login
        )
        btn_login.place(relx=0.5, rely=0.55, anchor=CENTER)

       

    # ========== Button Functions ==========
    def open_sign_up(self):
        os.system("python sign_up.py")

    def open_login(self):
        os.system("python login.py")

    


if __name__ == "__main__":
    root = Tk()
    obj =sign_up(root)
    root.mainloop()
