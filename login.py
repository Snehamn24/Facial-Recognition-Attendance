from tkinter import *
from tkinter import ttk, messagebox
import cv2
import csv
import os
import datetime
import numpy as np
import face_recognition

class Login:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x300")
        self.root.title("Login Page")

        self.var_regno = StringVar()
        self.var_password = StringVar()

        Label(self.root, text="Student Login", font=("Times New Roman", 16, "bold")).pack(pady=15)

        frame = Frame(self.root, padx=10, pady=10, relief=RIDGE, bd=2)
        frame.pack(pady=10)

        Label(frame, text="Reg No:", font=("Times New Roman", 12)).grid(row=0, column=0, sticky=W, pady=5)
        Entry(frame, textvariable=self.var_regno, width=25).grid(row=0, column=1, pady=5)

        Label(frame, text="Password:", font=("Times New Roman", 12)).grid(row=1, column=0, sticky=W, pady=5)
        Entry(frame, textvariable=self.var_password, show="*", width=25).grid(row=1, column=1, pady=5)

        Button(frame, text="Login", command=self.login_student, width=15, bg="blue", fg="white").grid(row=2, columnspan=2, pady=10)

    def login_student(self):
        regno = self.var_regno.get().strip()
        password = self.var_password.get().strip()

        if regno == "" or password == "":
            messagebox.showerror("Error", "Enter both RegNo and Password")
            return

        if not os.path.exists("students.csv"):
            messagebox.showerror("Error", "Registered students not found. Please Sign-up first.")
            return

        with open("students.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["RegNo"] == regno and row["Password"] == password:
                    messagebox.showinfo("Success", f"Welcome {row['Name']}!")
                    self.open_attendance_window(row)
                    return

        messagebox.showerror("Error", "Invalid RegNo or Password")

    def open_attendance_window(self, student_row):
        new_window = Toplevel(self.root)
        AttendanceWindow(new_window, student_row)


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

        dataset_path = os.path.join("dataset", regno)
        if not os.path.exists(dataset_path):
            messagebox.showerror("Error", "No face data found for this student.")
            return

        known_encodings = []
        for file in os.listdir(dataset_path):
            img_path = os.path.join(dataset_path, file)
            img = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(img)
            if encodings:
                known_encodings.append(encodings[0])

        if not known_encodings:
            messagebox.showerror("Error", "No valid face encodings found.")
            return

        

        cap = cv2.VideoCapture(0)
        messagebox.showinfo("Info", "Camera is opening... Look at the camera.")

        face_recognized = False #flag

        while True:

            ret, frame = cap.read()
            if not ret:
                break
       

            # Convert frame to RGB for face_recognition
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, encodings):

                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
                color = (0, 0, 255)  # Red box for mismatch
                label = "Unknown"

                if True in matches:
                    color = (0, 255, 0)  # Green = matched
                    label = f"{name} ({regno})"

                

                    # Display student details on screen
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                    cv2.putText(frame, label, (left + 5, bottom - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    # Also show Course & Semester on top left
                    cv2.putText(frame, f"Course: {course}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, f"Sem: {sem}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                    # Save attendance
                    self.save_attendance(regno, name, course, sem)
                    messagebox.showinfo("Success", "Attendance marked successfully!")
                    #cap.release()
                    face_recognized = True
                    #cv2.destroyAllWindows()
                    break
                else:

                    # Draw red box for unknown
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    cv2.putText(frame, label, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                

            cv2.imshow("Face Recognition - Mark Attendance", frame)

            #Exit Conditions
            if face_recognized:
                break
            if cv2.waitKey(1)==13:#Press Enter to Exit manually
                break

        cap.release()
        cv2.destroyAllWindows()
        if face_recognized:
             messagebox.showinfo("Success", "Attendance marked successfully.")

        else:
            messagebox.showerror("Error","Face not recognized and attendance not marked")
       



   

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
