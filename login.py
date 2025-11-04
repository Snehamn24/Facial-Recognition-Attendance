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
        self.root.geometry("400x350")
        self.root.title("Login Page")

        self.var_regno = StringVar()
        self.var_password = StringVar()

        Label(self.root, text="Login Portal", font=("Times New Roman", 18, "bold")).pack(pady=15)

        frame = Frame(self.root, padx=10, pady=10, relief=RIDGE, bd=2)
        frame.pack(pady=10)

        Label(frame, text="Username / RegNo:", font=("Times New Roman", 12)).grid(row=0, column=0, sticky=W, pady=5)
        Entry(frame, textvariable=self.var_regno, width=25).grid(row=0, column=1, pady=5)

        Label(frame, text="Password:", font=("Times New Roman", 12)).grid(row=1, column=0, sticky=W, pady=5)
        Entry(frame, textvariable=self.var_password, show="*", width=25).grid(row=1, column=1, pady=5)

        Button(frame, text="Login", command=self.login_user, width=15, bg="blue", fg="white").grid(row=2, columnspan=2, pady=10)

    def login_user(self):
        username = self.var_regno.get().strip()
        password = self.var_password.get().strip()

        if username == "" or password == "":
            messagebox.showerror("Error", "Enter both Username and Password")
            return

        # ✅ Admin login check
        if username == "admin" and password == "admin123":
            messagebox.showinfo("Admin Login", "Welcome Admin!")
            self.open_admin_dashboard()
            return

        # ✅ Student login
        if not os.path.exists("students.csv"):
            messagebox.showerror("Error", "No student records found. Please sign up first.")
            return

        with open("students.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["RegNo"] == username and row["Password"] == password:
                    messagebox.showinfo("Success", f"Welcome {row['Name']}!")
                    self.open_attendance_window(row)
                    return

        messagebox.showerror("Error", "Invalid credentials")

    def open_attendance_window(self, student_row):
        new_window = Toplevel(self.root)
        AttendanceWindow(new_window, student_row)

    def open_admin_dashboard(self):
        new_window = Toplevel(self.root)
        AdminDashboard(new_window)


class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("600x500")

        Label(self.root, text="Admin Dashboard", font=("Times New Roman", 18, "bold")).pack(pady=10)

        Button(self.root, text="View Registered Students", command=self.view_students, bg="blue", fg="white", width=25).pack(pady=10)
        Button(self.root, text="View Attendance Records", command=self.view_attendance, bg="green", fg="white", width=25).pack(pady=10)

        self.tree_frame = Frame(self.root)
        self.tree_frame.pack(fill=BOTH, expand=True, pady=10)

    def clear_tree(self):
        for widget in self.tree_frame.winfo_children():
            widget.destroy()

    def view_students(self):
        self.clear_tree()
        if not os.path.exists("students.csv"):
            messagebox.showerror("Error", "No student records found.")
            return

        columns = ("RegNo", "Name", "Course", "Sem", "Password")
        tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill=BOTH, expand=True)

        with open("students.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                tree.insert("", END, values=(row["RegNo"], row["Name"], row["Course"], row["Sem"], row["Password"]))

    def view_attendance(self):
        self.clear_tree()
        if not os.path.exists("attendance.csv"):
            messagebox.showerror("Error", "No attendance records found.")
            return

        Label(self.tree_frame, text="Filter by Course:", font=("Times New Roman", 12)).pack(pady=5)
        course_filter = ttk.Combobox(self.tree_frame, values=["All", "MBA", "MCA", "MTech"], state="readonly")
        course_filter.set("All")
        course_filter.pack(pady=5)

        columns = ("RegNo", "Name", "Course", "Sem", "Date", "Time", "Status")
        tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill=BOTH, expand=True)

        def load_data(course):
            for i in tree.get_children():
                tree.delete(i)
            with open("attendance.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if course == "All" or row["Course"] == course:
                        tree.insert("", END, values=(row["RegNo"], row["Name"], row["Course"], row["Sem"], row["Date"], row["Time"], row["Status"]))

        load_data("All")

        def on_select(event):
            load_data(course_filter.get())

        course_filter.bind("<<ComboboxSelected>>", on_select)


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
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(dataset_path, file)
                img = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(img)
                if encodings:
                    known_encodings.append(encodings[0])

        if not known_encodings:
            messagebox.showerror("Error", "No valid face encodings found.")
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open the camera.")
            return

        detected = False
        messagebox.showinfo("Info", "Camera started. Look at the camera to mark attendance.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, encodings):
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)

                if True in matches:
                    detected = True
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, f"{name} ({regno})", (left, bottom + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                    self.save_attendance(regno, name, course, sem)
                    cv2.imshow("Attendance", frame)
                    messagebox.showinfo("Success", "Attendance marked successfully!")
                    cap.release()
                    cv2.destroyAllWindows()
                    return

            cv2.imshow("Attendance", frame)
            if cv2.waitKey(1) == 13:
                break

        cap.release()
        cv2.destroyAllWindows()
        if not detected:
            messagebox.showwarning("Warning", "Face not Recognized. Attendance not marked.")

    def save_attendance(self, regno, name, course, sem):
        filename = "attendance.csv"
        file_exists = os.path.exists(filename)
        date = datetime.date.today().strftime("%Y-%m-%d")
        time_now = datetime.datetime.now().strftime("%H:%M:%S")

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