import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector as con

class AddNewBook: 
    def __init__(self, root):
        
        self.root = tk.Toplevel(root)
        self.root.title("University Library Management System")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.logo_image = Image.open("images/logo.jpg")
        self.logo_image = self.logo_image.resize((20,20))
        self.logo_img = ImageTk.PhotoImage(self.logo_image)
        self.root.iconphoto(False,self.logo_img)


        self.frame = tk.Frame(self.root, bg="#fff")
        self.frame.place(relwidth=1,relheight=1)

        self.bg_img = Image.open("images/book.png")
        self.bg_img = self.bg_img.resize((250,250))
        self.bg_photo = ImageTk.PhotoImage(self.bg_img)

        self.bg_label = tk.Label(self.frame, image=self.bg_photo, bg="#fff")
        self.bg_label.place(relx=0, rely=0.15)

        self.lblTitle = tk.Label(self.frame, text="Add New Book", bg="#fff", fg="#11112d", font=("Arial", 20, "bold"))
        self.lblTitle.place(relx=0.3, rely=0.02)

        self.txtBook = tk.Entry(self.frame, width=25, font=("Arial", 15), border=0, bg="#fff", fg="#000")
        self.txtBook.insert(0,'Book Title')
        self.txtBook.place(relx=0.5, rely=0.15)
        self.txtBook.bind('<FocusIn>', self.on_focus)
        self.txtBook.bind('<FocusOut>', self.on_exit)
        tk.Frame(self.frame, width=257,height=2,bg="#000").place(relx=0.5,rely=0.20)

        self.txtAuthor = tk.Entry(self.frame, width=25, font=("Arial", 15), border=0, bg="#fff", fg="#000")
        self.txtAuthor.insert(0,'Author Name')
        self.txtAuthor.place(relx=0.5, rely=0.3)
        self.txtAuthor.bind('<FocusIn>', self.on_focus1)
        self.txtAuthor.bind('<FocusOut>', self.on_exit1)
        tk.Frame(self.frame, width=257,height=2,bg="#000").place(relx=0.5,rely=0.35)

        self.txtCategory = tk.Entry(self.frame, width=25, font=("Arial", 15), border=0, bg="#fff", fg="#000")
        self.txtCategory.insert(0,'Category')
        self.txtCategory.place(relx=0.5, rely=0.45)
        self.txtCategory.bind('<FocusIn>', self.on_focus2)
        self.txtCategory.bind('<FocusOut>', self.on_exit2)
        tk.Frame(self.frame, width=257,height=2,bg="#000").place(relx=0.5,rely=0.50)

        self.txtEdition = tk.Entry(self.frame, width=25, font=("Arial", 15), border=0, bg="#fff", fg="#000")
        self.txtEdition.insert(0,'Edition')
        self.txtEdition.place(relx=0.5, rely=0.6)
        self.txtEdition.bind('<FocusIn>', self.on_focus3)
        self.txtEdition.bind('<FocusOut>', self.on_exit3)
        tk.Frame(self.frame, width=257,height=2,bg="#000").place(relx=0.5,rely=0.65)


        self.btn = tk.Button(self.frame, text="ADD", padx=20, pady=7, font=("Arial", 10, "bold"), fg="#fff", bg="#3586ff", command=self.addNewBook)
        self.btn.place(relx=0.57,rely=0.77, anchor="center")

                                                    
        self.root.mainloop()
                

    def on_focus(self, e):
        book = self.txtBook.get()
        if book == "Book Title":
            self.txtBook.delete(0,'end')

    def on_exit(self, e):
        book = self.txtBook.get()
        if book=="":
            self.txtBook.insert(0,'Book Title')


    def on_focus1(self,e):
        auth = self.txtAuthor.get()
        if auth == "Author Name":
            self.txtAuthor.delete(0,'end')

    def on_exit1(self,e):
        auth = self.txtAuthor.get()
        if auth=="":
            self.txtAuthor.insert(0,'Author Name')

    def on_focus2(self,e):
        category = self.txtCategory.get()
        if category == "Category":
            self.txtCategory.delete(0,'end')

    def on_exit2(self,e):
        category = self.txtCategory.get()
        if category=="":
            self.txtCategory.insert(0,'Category')
            
    def on_focus3(self,e):
        edition = self.txtEdition.get()
        if edition == "Edition":
            self.txtEdition.delete(0,'end')

    def on_exit3(self,e):
        edition = self.txtEdition.get()
        if edition=="":
            self.txtEdition.insert(0,'Edition')
    

    def addNewBook(self):
        book = self.txtBook.get()
        author = self.txtAuthor.get()
        category = self.txtCategory.get()
        edition = self.txtEdition.get()

        dbcon = con.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "university_librarydb"
            )
        mycursor = dbcon.cursor()
        query = "INSERT INTO books (title, author, category, edition) VALUES(%s, %s, %s, %s)"
        value = (book, author, category, edition, )
        mycursor.execute(query, value)
        dbcon.commit()

        count = mycursor.rowcount
        if count > 0:
            print("Successfully inserted")
            self.root.destroy()
            messagebox.showinfo("Add New Book", "New Book Successfully inserted")
        else:
            messagebox.showerror("Add New Book", "Sorry, Cannot add book")
        
#AddNewBook(tk.Tk())
        
            
        
