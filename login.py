from tkinter import *
from tkinter import ttk,messagebox
import cv2
import csv
import os
import datetime

class Login:
    def __init__(self,root):
        self.root = root
        self.root.geometry("400x300")
        self.root.title("Login Page")

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
                if row["RegNo"]==regno and row["Password"]==password:
                    messagebox.showinfo("Success", f"Welcome {row['Name']}!")
                    self.open_attendance_window(row)
                    return

        messagebox.showerror("Invalid regno or password")

    #open Attendence Window
    def open_attendance_window(self,student_row):
        new_window = Toplevel(self.root)
        AttendanceWindow(new_window,student_row)

    
class AttendanceWindow:
    def __init__(self, root, student):
        self.root = root
        self.root.title("Mark Attendance")
        self.root.geometry("400x400")
        self.student = student

        Label(self.root, text=f"Welcome {student['Name']}", font=("Times New Roman", 14, "bold")).pack(pady=10)
        Label(self.root, text=f"Reg No: {student['RegNo']}").pack()
        Label(self.root, text=f"Course: {student['Course']}").pack()
        Label(self.root, text=f"Semester: {student['Sem']}").pack(pady=5)

        Button(self.root, text="Mark Attendance", command=self.mark_attendance, bg="green", fg="white", width=20).pack(pady=20)

    def mark_attendance(self):
        regno = self.student["RegNo"]
        name = self.student["Name"]
        course = self.student["Course"]
        sem = self.student["Sem"]

        # open webcam
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot access webcam. Please check camera connection.")
            return 

    

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        messagebox.showinfo("Info", "Press Enter to capture live image")

        self.root.iconify()  # minimize tkinter window


        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow("Attendance - Live", frame)
            if cv2.waitKey(1) == 13:  # Enter key
                break

        cap.release()
        cv2.destroyAllWindows()
        self.root.deiconify()  # restore window

        # Save attendance
        self.save_attendance(regno, name, course, sem)
        messagebox.showinfo("Success", "Attendance marked successfully!")

    def save_attendance(self, regno, name, course, sem):
        filename = "attendance.csv"
        file_exists = os.path.exists(filename)
        date = datetime.date.today().strftime("%Y-%m-%d")
        time_now = datetime.datetime.now().strftime("%H:%M:%S")

        # Avoid duplicate attendance for same day
        if file_exists:
            with open(filename, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["RegNo"] == regno and row["Date"] == date:
                        messagebox.showinfo("Info", "Attendance already marked for today.")
                        return

        with open(filename, "a", newline="") as file:
            fieldnames = ["RegNo", "Name", "Course", "Sem", "Date", "Time", "Status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                "RegNo": regno,
                "Name": name,
                "Course": course,
                "Sem": sem,
                "Date": date,
                "Time": time_now,
                "Status": "Present"
            })


if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()










