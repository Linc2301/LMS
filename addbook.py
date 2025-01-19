import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector as con

class AddBook: 
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

        self.bg_img = Image.open("images/book.jpg")
        self.bg_img = self.bg_img.resize((250,250))
        self.bg_photo = ImageTk.PhotoImage(self.bg_img)

        self.bg_label = tk.Label(self.frame, image=self.bg_photo, bg="#fff")
        self.bg_label.place(relx=0, rely=0.05)

        self.lblTitle = tk.Label(self.frame, text="Adding New Book", bg="#fff", fg="#11112d", font=("Arial", 20, "bold"))
        self.lblTitle.place(relx=0.25, rely=0.02)

        self.title_entry = tk.Entry(self.frame, width=25, font=("Arial", 15), border=0, bg="#fff", fg="#000")
        self.title_entry.insert(0,'Title')
        self.title_entry.place(relx=0.5, rely=0.2)
        self.title_entry.bind('<FocusIn>', self.on_focus)
        self.title_entry.bind('<FocusOut>', self.on_exit)
        tk.Frame(self.frame, width=257,height=2,bg="#000").place(relx=0.5,rely=0.25)

        self.author_entry = tk.Entry(self.frame, width=25, font=("Arial", 15), border=0, bg="#fff", fg="#000")
        self.author_entry.insert(0,'Author')
        self.author_entry.place(relx=0.5, rely=0.3)
        self.author_entry.bind('<FocusIn>', self.on_focus1)
        self.author_entry.bind('<FocusOut>', self.on_exit1)
        tk.Frame(self.frame, width=257,height=2,bg="#000").place(relx=0.5,rely=0.35)

        self.cate_entry = tk.Entry(self.frame, width=25, font=("Arial", 15), border=0, bg="#fff", fg="#000")
        self.cate_entry.insert(0,'Category')
        self.cate_entry.place(relx=0.5, rely=0.4)
        self.cate_entry.bind('<FocusIn>', self.on_focus2)
        self.cate_entry.bind('<FocusOut>', self.on_exit2)
        tk.Frame(self.frame, width=257,height=2,bg="#000").place(relx=0.5,rely=0.45)

        self.dept_entry = tk.Entry(self.frame, width=25, font=("Arial", 15), border=0, bg="#fff", fg="#000")
        self.dept_entry.insert(0,'Quantity')
        self.dept_entry.place(relx=0.5, rely=0.5)
        self.dept_entry.bind('<FocusIn>', self.on_focus3)
        self.dept_entry.bind('<FocusOut>', self.on_exit3)
        tk.Frame(self.frame, width=257,height=2,bg="#000").place(relx=0.5,rely=0.55)


        self.btn = tk.Button(self.frame, text="ADD", padx=20, pady=7, font=("Arial", 10, "bold"), fg="#fff", bg="#3586ff", command=self.registerMember)
        self.btn.place(relx=0.57,rely=0.7, anchor="center")

                                                    
        self.root.mainloop()
                

    def on_focus(self, e):
        user = self.title_entry.get()
        if user == "Title":
            self.title_entry.delete(0,'end')

    def on_exit(self, e):
        name = self.title_entry.get()
        if name=="":
            self.title_entry.insert(0,'Title')


    def on_focus1(self,e):
        roll = self.author_entry.get()
        if roll == "Author":
            self.author_entry.delete(0,'end')

    def on_exit1(self,e):
        roll = self.author_entry.get()
        if roll=="":
            self.author_entry.insert(0,'Author')

    def on_focus2(self,e):
        dept = self.cate_entry.get()
        if dept == "Category":
            self.cate_entry.delete(0,'end')

    def on_exit2(self,e):
        dept = self.cate_entry.get()
        if dept=="":
            self.cate_entry.insert(0,'Category')

    def on_focus3(self,e):
        dept = self.dept_entry.get()
        if dept == "Quantity":
            self.dept_entry.delete(0,'end')

    def on_exit3(self,e):
        dept = self.dept_entry.get()
        if dept=="":
            self.dept_entry.insert(0,'Edition')

    def registerMember(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        category = self.cate_entry.get()
        edition = self.dept_entry.get()

        dbcon = con.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "university_librarydb"
            )
        mycursor = dbcon.cursor()
        query = "INSERT INTO books (title, author, category,edition) VALUES(%s, %s, %s,%s)"
        value = (title, author, category,edition, )
        mycursor.execute(query, value)
        dbcon.commit()

        count = mycursor.rowcount
        if count > 0:
            print("Successfully inserted")
            self.root.destroy()
            messagebox.showinfo("Adding New Book", "New Book List Successfully inserted")
        else:
            messagebox.showerror("Adding New Book", "Sorry, Cannot insert book record")
        


#RegisterMember(tk.Tk())        
            
        
