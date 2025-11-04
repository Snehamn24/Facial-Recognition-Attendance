from tkinter import *
from tkinter import ttk, messagebox
import os
import csv
import cv2
import dlib
import face_recognition
from scipy.spatial import distance as dist

def eye_aspect_ratio(eye):
    # Compute EAR
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

class signup:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign up")
        self.root.geometry("500x500")

        self.var_name = StringVar()
        self.var_pass = StringVar()
        self.var_regno = StringVar()
        self.var_course = StringVar()
        self.var_sem = StringVar()

        title = Label(self.root, text="Student Face Recognition Form", font=("Times New Roman", 10, "bold"))
        title.pack(pady=10)

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


    def capture_face(self):
        name = self.var_name.get().strip()
        regno = self.var_regno.get().strip()
        if name == "" or regno == "":
            messagebox.showerror("Error", "Please enter the name and regno before capturing.")
            return

        folder_path = os.path.join("dataset", regno)
        os.makedirs(folder_path, exist_ok=True)

        # Load dlib face detector and predictor
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(r"C:\repo\Facial-Recognition-Attendance\shape_predictor_68_face_landmarks (1).dat")

        # Define eye landmark indices
        (lStart, lEnd) = (42, 48)
        (rStart, rEnd) = (36, 42)
        EAR_THRESHOLD = 0.21
        CONSEC_FRAMES = 2
        blink_detected = False
        counter = 0

        cap = cv2.VideoCapture(0)
        messagebox.showinfo("Instruction", "Look at the camera and blink to confirm you're live.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 0)

            for rect in rects:
                shape = predictor(gray, rect)
                shape = [(shape.part(i).x, shape.part(i).y) for i in range(68)]

                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0

                if ear < EAR_THRESHOLD:
                    counter += 1
                else:
                    if counter >= CONSEC_FRAMES:
                        blink_detected = True
                        messagebox.showinfo("Live Confirmed", "Blink detected — capturing your face now!")
                    counter = 0

                if blink_detected:
                    for i in range(1, 6):
                        file_path = os.path.join(folder_path, f"{name}_{i}.jpg")
                        cv2.imwrite(file_path, frame)
                    messagebox.showinfo("Success", "Face captured successfully after blink!")
                    blink_detected = False
                    cap.release()
                    cv2.destroyAllWindows()
                    return

            cv2.imshow("Live Detection (Press 'q' to exit)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Exit", "No blink detected. Try again with a real person.")


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

        if file_exists:
            with open("students.csv", "r") as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) >= 5 and row[3] == reg and row[4] == course:
                        messagebox.showerror("Error", "Student already exists!")
                        return

        next_id = 1
        if file_exists:
            with open("students.csv", "r") as file:
                lines = file.readlines()
                if len(lines) > 1:
                    last_line = lines[-1].split(",")
                    next_id = int(last_line[0]) + 1

        with open("students.csv", "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["ID", "Name", "Password", "RegNo", "Course", "Sem"])
            writer.writerow([next_id, name, password, reg, course, sem])

        messagebox.showinfo("Success", f"Student Registered Successfully!\nYour ID: {next_id}")
        self.var_name.set("")
        self.var_pass.set("")
        self.var_regno.set("")
        self.var_course.set("Select Course")
        self.var_sem.set("Select Sem")


if __name__ == "__main__":
    root = Tk()
    obj = signup(root)
    root.mainloop()
