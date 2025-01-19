import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector as con

class RegisterMember: 
    def __init__(self, root):
        
        self.root = tk.Toplevel(root)
        self.root.title("University Library Management System")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.logo_image = Image.open("images/logo.jpg")
        self.logo_image = self.logo_image.resize((20,20))
        self.logo_img = ImageTk.PhotoImage(self.logo_image)
        self.root.iconphoto(False,self.logo_img)


        self.frame = tk.Frame(self.root, bg="#fff")
        self.frame.place(relwidth=1,relheight=1)

        self.bg_img = Image.open("images/login.png")
        self.bg_img = self.bg_img.resize((250,250))
        self.bg_photo = ImageTk.PhotoImage(self.bg_img)

        self.bg_label = tk.Label(self.frame, image=self.bg_photo, bg="#fff")
        self.bg_label.place(relx=0, rely=0.05)

        self.lblTitle = tk.Label(self.frame, text="Register New Member", bg="#fff", fg="#1c6f9c", font=("Times", 20, "bold"))
        self.lblTitle.place(relx=0.25, rely=0.02)

        self.user_entry = tk.Entry(self.frame, width=25, font=("Arial", 15), border=0, bg="#fff", fg="#000")
        self.user_entry.insert(0,'User Name')
        self.user_entry.place(relx=0.5, rely=0.2)
        self.user_entry.bind('<FocusIn>', self.on_focus)
        self.user_entry.bind('<FocusOut>', self.on_exit)
        tk.Frame(self.frame, width=257,height=2,bg="#000").place(relx=0.5,rely=0.29)

        self.roll_entry = tk.Entry(self.frame, width=25, font=("Arial", 15), border=0, bg="#fff", fg="#000")
        self.roll_entry.insert(0,'Roll Number')
        self.roll_entry.place(relx=0.5, rely=0.4)
        self.roll_entry.bind('<FocusIn>', self.on_focus1)
        self.roll_entry.bind('<FocusOut>', self.on_exit1)
        tk.Frame(self.frame, width=257,height=2,bg="#000").place(relx=0.5,rely=0.48)

        self.dept_entry = tk.Entry(self.frame, width=25, font=("Arial", 15), border=0, bg="#fff", fg="#000")
        self.dept_entry.insert(0,'Class OR Department')
        self.dept_entry.place(relx=0.5, rely=0.6)
        self.dept_entry.bind('<FocusIn>', self.on_focus2)
        self.dept_entry.bind('<FocusOut>', self.on_exit2)
        tk.Frame(self.frame, width=257,height=2,bg="#000").place(relx=0.5,rely=0.67)


        self.btn = tk.Button(self.frame, text="Register", padx=20, pady=7, font=("Arial", 10, "bold"), fg="#fff", bg="#3586ff", command=self.registerMember)
        self.btn.place(relx=0.57,rely=0.8, anchor="center")

                                                    
        self.root.mainloop()
                

    def on_focus(self, e):
        user = self.user_entry.get()
        if user == "User Name":
            self.user_entry.delete(0,'end')

    def on_exit(self, e):
        name = self.user_entry.get()
        if name=="":
            self.user_entry.insert(0,'User Name')


    def on_focus1(self,e):
        roll = self.roll_entry.get()
        if roll == "Roll Number":
            self.roll_entry.delete(0,'end')

    def on_exit1(self,e):
        roll = self.roll_entry.get()
        if roll=="":
            self.roll_entry.insert(0,'Roll Number')

    def on_focus2(self,e):
        dept = self.dept_entry.get()
        if dept == "Class OR Department":
            self.dept_entry.delete(0,'end')

    def on_exit2(self,e):
        dept = self.dept_entry.get()
        if dept=="":
            self.dept_entry.insert(0,'Class OR Department')

    def registerMember(self):
        user = self.user_entry.get()
        roll = self.roll_entry.get()
        dept = self.dept_entry.get()

        dbcon = con.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "university_librarydb"
            )
        mycursor = dbcon.cursor()
        query = "INSERT INTO members (name, roll, department) VALUES(%s, %s, %s)"
        value = (user, roll, dept, )
        mycursor.execute(query, value)
        dbcon.commit()

        count = mycursor.rowcount
        if count > 0:
            print("Successfully inserted")
            self.root.destroy()
            messagebox.showinfo("Register New Member", "New Member Record Successfully inserted")
        else:
            messagebox.showerror("Register New Member", "Sorry, Cannot insert member record")
        


#RegisterMember(tk.Tk())        
            
        
