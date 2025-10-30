from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk

class Student:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Student")

         #upper image
        img1 = Image.open(r"C:\repo\Facial-Recognition-Attendance\face_bg.webp")
        img1 = img1.resize((1530,790))
        self.img1 = ImageTk.PhotoImage(img1)

        label1 = Label(self.root,image=self.img1)
        label1.place(x=0,y=0,width=1530,height=200)

        #left label frame
        left_frame = LabelFrame(self.root,text="Student Details",bd = 2,relief=RIDGE)
        left_frame.place(x=8,y=200,width=730,height=580)

        #right label frame
        # right_frame = LabelFrame(self.root,text="Student Details",bd=2,relief=RIDGE)
        # right_frame.place(x=750,y=200,width=730,height=580)

        current_course_frame = LabelFrame(left_frame,text="Current course",bg="White")
        current_course_frame.place(x=5,y=5,width=720,height=300)


        #Name
        name_label = Label(current_course_frame,text="Name",font=("Times New Roman",9,"bold"))
        name_label.grid(row=0,column=0)
        name_box = Entry(current_course_frame,width=25,font=("Times New Roman",10))
        name_box.grid(row=0,column=1,padx=10,pady=5,sticky=W)

        
        #course
        course_label = Label(current_course_frame,text="Course",font=("Times New Roman",9,"bold"))
        course_label.grid(row=1,column=0,padx=2,pady=10)

        course_combo = ttk.Combobox(current_course_frame,font=("Times New Roman",10,"bold"),state="readonly")
        course_combo["values"]=("Select course","MCA","MBA","MTECh")
        course_combo.current(0)
        course_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)

        #year
        year_label = Label(current_course_frame,text="Year",font=("Times New Roman",9,"bold"))
        year_label.grid(row=2,column=0,padx=10,pady=10)

        year_combo = ttk.Combobox(current_course_frame,font=("Times New Roman",10,"bold"),state="readonly")
        year_combo["values"]=("Select year","2024-25","2025-26")
        year_combo.current(0)
        year_combo.grid(row=2,column=1,padx=2,pady=10,sticky=W)

        #Semester
        semester_label = Label(current_course_frame,text="Semester",font=("Times New Roman",9,"bold"))
        semester_label.grid(row=3,column=0,padx=10,pady=10)

        semester_combo = ttk.Combobox(current_course_frame,font=("Times New Roman",10,"bold"),state="readonly")
        semester_combo["values"]=("Select sem","1","2")
        semester_combo.current(0)
        semester_combo.grid(row=3,column=1,padx=10,pady=10,sticky=W)



if __name__=="__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()