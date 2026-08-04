# Facial Recognition Attendance System

A desktop application that registers students with face data and marks attendance using facial recognition. Built with Python, Tkinter, OpenCV, and the `face_recognition` library, it stores student and attendance records in CSV files.

**Repository:** [https://github.com/Snehamn24/Facial-Recognition-Attendance](https://github.com/Snehamn24/Facial-Recognition-Attendance)

---

## Features

- **Student registration** — Sign up with name, registration number, course, semester, and password
- **Live face capture** — Blink detection (liveness check) before saving face images
- **Facial recognition login** — Mark attendance by matching your face against stored images
- **Duplicate prevention** — One attendance record per student per day
- **Admin dashboard** — View registered students and filter attendance by course (MBA, MCA, MTech)
- **CSV storage** — Simple, portable data format for students and attendance

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| GUI | Tkinter |
| Face recognition | `face_recognition`, dlib |
| Camera & image processing | OpenCV (`cv2`) |
| Liveness detection | dlib 68-point facial landmarks (Eye Aspect Ratio) |
| Image handling | Pillow (PIL) |
| Data storage | CSV |

---

## Prerequisites

- **Python 3.8+**
- **Webcam** (required for face capture and attendance)
- **Windows** (tested on Windows; paths in the code use Windows-style locations)

### External files (not included in the repo)

You must add these before running the app:

1. **Background image** — `bg2.jpg` in the project root (used on the home screen)
2. **dlib shape predictor** — Download [shape_predictor_68_face_landmarks.dat](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2), extract it, and place it in the project root. The code expects the filename:
   ```
   shape_predictor_68_face_landmarks (1).dat
   ```

> **Note:** `main.py` and `sign_up.py` use absolute paths (`C:\repo\Facial-Recognition-Attendance\...`). If your project lives elsewhere, update those paths or switch them to relative paths.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Snehamn24/Facial-Recognition-Attendance.git
   cd Facial-Recognition-Attendance
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install opencv-python face_recognition dlib Pillow numpy scipy
   ```

   Installing `dlib` on Windows may require [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) or a pre-built wheel. If `pip install dlib` fails, search for a compatible wheel for your Python version.

4. **Add required assets**

   - Place `bg2.jpg` in the project root
   - Place the dlib shape predictor file in the project root (see above)

5. **Create the dataset folder** (optional — created automatically on first face capture)

   ```bash
   mkdir dataset
   ```

---

## Project Structure

```
Facial-Recognition-Attendance/
├── main.py              # Home screen — entry point
├── sign_up.py           # Student registration & face capture
├── login.py             # Login, attendance marking, admin dashboard
├── students.csv         # Registered student records
├── attendance.csv       # Attendance logs
├── dataset/             # Face images per student (folder per RegNo)
│   └── <RegNo>/
│       └── *.jpg
├── bg2.jpg              # Home screen background (add manually)
└── shape_predictor_68_face_landmarks (1).dat   # dlib model (add manually)
```

---

## How to Run

From the project directory:

```bash
python main.py
```

The home screen offers:

- **Student Sign-In** — Opens registration (`sign_up.py`)
- **Student/Admin Login** — Opens login (`login.py`)

---

## Usage Guide

### 1. Student registration

1. Click **Student Sign-In** on the home screen.
2. Fill in Name, Password, Registration Number, Course, and Semester.
3. Click **Capture Face**:
   - Look at the webcam and **blink** to confirm liveness.
   - After a blink is detected, five face images are saved under `dataset/<RegNo>/`.
4. Click **Register** to save the student to `students.csv`.

**Supported courses:** MCA, MBA, MTech  
**Supported semesters:** 1, 2

### 2. Mark attendance (student)

1. Click **Student/Admin Login**.
2. Enter your **Registration Number** and **Password**.
3. Click **Mark Attendance**.
4. Look at the camera when prompted; attendance is recorded when your face matches stored images.
5. Press **Enter** to cancel if needed.

Attendance is saved to `attendance.csv` with date, time, and status **Present**. Only one entry per student per day is allowed.

### 3. Admin dashboard

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |

After logging in as admin you can:

- **View Registered Students** — All records from `students.csv`
- **View Attendance Records** — Filter by course (All, MBA, MCA, MTech)

---

## Data Files

### `students.csv`

| Column | Description |
|--------|-------------|
| ID | Auto-increment student ID |
| Name | Full name |
| Password | Login password |
| RegNo | Registration number |
| Course | MBA / MCA / MTech |
| Sem | Semester (1 or 2) |

### `attendance.csv`

| Column | Description |
|--------|-------------|
| RegNo | Registration number |
| Name | Student name |
| Course | Course name |
| Sem | Semester |
| Date | YYYY-MM-DD |
| Time | HH:MM:SS |
| Status | Present |

### `dataset/`

Each student has a folder named after their registration number. Face images captured during sign-up are stored as `.jpg` files and used for recognition during attendance.

---

## Troubleshooting

| Issue | Possible fix |
|-------|----------------|
| Camera not opening | Check webcam permissions and that no other app is using the camera |
| Face not recognized | Re-capture face images in good lighting; ensure images exist in `dataset/<RegNo>/` |
| Blink not detected | Face the camera directly; adjust lighting |
| `dlib` install fails | Install Visual C++ Build Tools or use a pre-built wheel |
| Background image error | Ensure `bg2.jpg` exists and the path in `main.py` is correct |
| Shape predictor error | Download and place the `.dat` file; verify the path in `sign_up.py` |

---

## Security Notes

This project is intended for learning and local/demo use:

- Passwords are stored in plain text in `students.csv`
- Admin credentials are hardcoded in `login.py`
- Do not use this as-is in production without proper authentication, encryption, and access controls

---

## License

This project is open source. Add a license file if you plan to publish or share it formally.

---

## Author

**Snehamn24** — [GitHub](https://github.com/Snehamn24)
