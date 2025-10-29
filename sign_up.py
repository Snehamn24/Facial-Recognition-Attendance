from tkinter import *
from tkinter import ttk, messagebox
import csv
import os
import cv2

class signup:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign up")
        self.root.geometry("500x500")

        # Variables
        self.var_name = StringVar()
        self.var_pass = StringVar()
        self.var_regno = StringVar()
        self.var_course = StringVar()
        self.var_sem = StringVar()

        title = Label(self.root, text="Student Face Recognition Form", font=("Times New Roman", 10, "bold"))
        title.pack(pady=10)

        # Form Frame
        form_frame = Frame(self.root, padx=10, pady=10, bd=2, relief=RIDGE)
        form_frame.pack(pady=20)

        Label(form_frame, text="Name:", font=("Times New Roman", 12, "bold")).grid(row=0, column=0, sticky=W, pady=5)
        Entry(form_frame, textvariable=self.var_name, width=25, font=("Times New Roman", 12)).grid(row=0, column=1, pady=5)

        Label(form_frame, text="Password:", font=("Times New Roman", 12, "bold")).grid(row=1, column=0, sticky=W, pady=5)
        Entry(form_frame, textvariable=self.var_pass, show="*", width=25, font=("Times New Roman", 12)).grid(row=1, column=1, pady=5)

        Label(form_frame, text="Regno:", font=("Times New Roman", 12, "bold")).grid(row=2, column=0, sticky=W, pady=5)
        Entry(form_frame, textvariable=self.var_regno, width=25, font=("Times New Roman", 12)).grid(row=2, column=1, pady=5)

        Label(form_frame, text="Course:", font=("Times New Roman", 12, "bold")).grid(row=3, column=0, sticky=W, pady=5)
        course_combo = ttk.Combobox(form_frame, textvariable=self.var_course, font=("Times New Roman", 12), state="readonly")
        course_combo["values"] = ("Select Course", "MCA", "MBA", "MTech")
        course_combo.current(0)
        course_combo.grid(row=3, column=1, pady=5)

        Label(form_frame, text="Semester:", font=("Times New Roman", 12, "bold")).grid(row=4, column=0, sticky=W, pady=5)
        sem_combo = ttk.Combobox(form_frame, textvariable=self.var_sem, font=("Times New Roman", 12), state="readonly")
        sem_combo["values"] = ("Select Sem", "1", "2")
        sem_combo.current(0)
        sem_combo.grid(row=4, column=1, pady=5)

        Button(form_frame, text="Capture Face", command=self.capture_face, width=15, bg="blue", fg="white").grid(row=5, column=0, pady=15)
        Button(form_frame, text="Register", command=self.register_data, width=15, bg="green", fg="white").grid(row=5, column=1, pady=15)

    # ====== Capture Face ======
    def capture_face(self):
        name = self.var_name.get()
        regno = self.var_regno.get()
        if name == "" or regno=="":
            messagebox.showerror("Error", "Please enter the name before capturing face.")
            return
        #count = 0
        folder_path = os.path.join("dataset",regno)
        os.makedirs(folder_path, exist_ok=True)
        #cv2.imwrite(os.path.join(folder_path, f"{name}_{count}.jpg"), img)

        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        img_id = 0
        messagebox.showinfo("Info", "Capturing 10 face samples. Please look at the camera.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                img_id += 1
                face_img = frame[y:y + h, x:x + w]
                file_path = os.path.join(folder_path, f"{name}_{img_id}.jpg")
                cv2.imwrite(file_path, face_img)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, str(img_id), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            cv2.imshow("Capturing Faces", frame)
            if cv2.waitKey(1) == 13 or img_id >= 10:
                break

        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Face samples captured successfully!")

    # ====== Register Data ======
    def register_data(self):
        name = self.var_name.get()
        password = self.var_pass.get()
        reg = self.var_regno.get()
        course = self.var_course.get()
        sem = self.var_sem.get()

        if name == "" or password == "" or reg == "" or course == "Select Course" or sem == "Select Sem":
            messagebox.showerror("Error", "All fields are required!")
            return

        file_exists = os.path.exists("students.csv")

        # Check for duplicates
        if file_exists:
            with open("students.csv", "r") as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) >= 5 and row[3] == reg and row[4] == course:
                        messagebox.showerror("Error", "Student with same Reg No and Course already exists!")
                        return

        # Auto ID
        next_id = 1
        if file_exists:
            with open("students.csv", "r") as file:
                lines = file.readlines()
                if len(lines) > 1:
                    last_line = lines[-1].split(",")
                    next_id = int(last_line[0]) + 1

        # Write to CSV
        with open("students.csv", "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["ID", "Name", "Password", "RegNo", "Course", "Sem"])
            writer.writerow([next_id, name, password, reg, course, sem])

        messagebox.showinfo("Success", f"Student Registered Successfully!\nYour ID: {next_id}")

        # Clear fields
        self.var_name.set("")
        self.var_pass.set("")
        self.var_regno.set("")
        self.var_course.set("Select Course")
        self.var_sem.set("Select Sem")


if __name__ == "__main__":
    root = Tk()
    obj = signup(root)
    root.mainloop()
