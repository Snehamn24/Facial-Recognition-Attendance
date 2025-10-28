from tkinter import *
from tkinter import ttk,messagebox
import cv2
import csv
import os
import datetime

class Login:
    def __init__(self,root):
        self.root = root
        self.root.geometry(400x300)
        delf.root.title("Login Page")

        self.var_regno = StringVar()
        self.var_password = StringVar()

        Label(self.root,text="student Login",font=("Times New Roman",16,"bold")).pack(pady=15)

        frame = Frame(self.root, padx=10, pady=10, relief=RIDGE, bd=2)
        frame.pack(pady=10)

        Label(frame, text="Reg No:", font=("Times New Roman", 12)).grid(row=0, column=0, sticky=W, pady=5)
        Entry(frame, textvariable=self.var_regno, width=25).grid(row=0, column=1, pady=5)

        Label(frame, text="Password:", font=("Times New Roman", 12)).grid(row=1, column=0, sticky=W, pady=5)
        Entry(frame, textvariable=self.var_password, show="*", width=25).grid(row=1, column=1, pady=5)

        Button(frame, text="Login", command=self.login_student, width=15, bg="blue", fg="white").grid(row=2, columnspan=2, pady=10)

    #login credentials
    def login_student(self):
        regno = self.var_regno.get().strip()
        password = self.var_password.get().strip()

        if regno=="" or password=="":
            messagebox.showerror("Enter the regno and password")
            return

        if not os.path.exists("students.csv"):
            messagebox.showerror("Registered students not found , Please Sign-up")
            return

        with open("students.csv","r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Regno"]==regno and row["Password"]==password:
                    messagebox.showinfo("Success", f"Welcome {row['Name']}!")
                    self.open_attendance_window(row)
                    return

        messagebox.showerror("Invalid regno or password")
        








