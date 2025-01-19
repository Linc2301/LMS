from tkinter import *
from PIL import Image,ImageTk
from datetime import datetime
import RegisterMember
import showmem
import updatemember
import deletemember
import AddNewBook
import UpdateBook
import DeleteBook
import search_book
import delete_borrower
import hold_book
import delete_hold
import return_book
class MainPage: 
    def __init__(self): 
        self.window = Tk()
        self.window.title("University Library Management System")
        self.window.state('zoomed')

        self.logo = Image.open("images/logo.jpg")
        self.logo = self.logo.resize((65,65))
        self.img = ImageTk.PhotoImage(self.logo)
        self.window.iconphoto(False,self.img)

        


        self.menu = Menu(self.window,tearoff=0)
        self.window.config(menu = self.menu)

        self.memberMenu = Menu(self.menu,tearoff=0)
        self.menu.add_cascade(label="Manage Members", menu = self.memberMenu)
        self.memberMenu.add_command(label="Register New Member", font=('Helvetica', 10), command=self.register_member)
        self.memberMenu.add_command(label="View Member Information", font=('Helvetica', 10),command=self.view_member)
        self.memberMenu.add_command(label="Update Member Information", font=('Helvetica', 10),command=self.update_member)
        self.memberMenu.add_command(label="Delete Members", font=('Helvetica', 10),command=self.delete_member)
        
        self.bookMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Manage Books", menu = self.bookMenu)
        self.bookMenu.add_command(label="Add New Books", font=('Helvetica', 10),command=self.add_books)
        self.bookMenu.add_command(label="Update Book Information", font=('Helvetica', 10),command=self.update_book)
        self.bookMenu.add_command(label="Delete Books", font=('Helvetica', 10),command=self.delete_books)
        self.bookMenu.add_command(label="Borrow Books", font=('Helvetica', 10),command=self.search_books)
        self.bookMenu.add_command(label="Delete Borrowers", font=('Helvetica', 10),command=self.delete_borrowers)
        self.bookMenu.add_command(label="Hold Books", font=('Helvetica', 10),command=self.hold_books)
        self.bookMenu.add_command(label="Delete Holds", font=('Helvetica', 10),command=self.delete_holds)



        self.transactionMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Issue Books", menu = self.transactionMenu)
        self.transactionMenu.add_command(label="Return Books", font=('Helvetica', 10,),command=self.return_books)
        self.transactionMenu.add_command(label="Renew Books", font=('Helvetica', 10))
        self.transactionMenu.add_command(label="Fine Calculation", font=('Helvetica', 10))


        self.frame = Frame(self.window, bg="#1c6f9c")
        self.frame.place(relx=0,rely=0,relwidth=1,relheight=0.1)
        self.lbl_logo = Label(self.frame, image=self.img)
        self.lbl_logo.place(relx=0,rely=0.05)

        self.lbl_header = Label(self.frame, text="University Library Management System", fg="#fff", bg="#1c6f9c", font=('Helvetica', 15))
        self.lbl_header.place(relx=0.05, rely=0.3)
        
            
        self.lbl_time = Label(self.frame, text="", fg="#fff", bg="#1c6f9c", font=('Helvetica', 14, "bold"))
        self.lbl_time.place(relx=0.8, rely=0.3)

        self.update_time()
        self.frame2 = Frame(self.window, bg="#fff")
        self.frame2.place(relx=0, rely=0.1)

        self.bg1_img = Image.open("images/cuhpaan.jpg")
        self.bg1_img = self.bg1_img.resize((1600,800))
        self.bg1_photo = ImageTk.PhotoImage(self.bg1_img)

        self.bg1_label = Label(self.frame2, image=self.bg1_photo, bg="#fff")
        self.bg1_label.pack()

        self.window.mainloop()


    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d  %I:%M:%S %p")
        self.lbl_time.config(text=current_time)
        self.frame.after(1000, self.update_time)

    def register_member(self):
        RegisterMember.RegisterMember(self.window)

    def view_member(self):
        showmem.ViewMember(self.window)

    def update_member(self):
        updatemember.UpdateMember(self.window)

    def delete_member(self):
        deletemember.DeleteMember(self.window)


    def add_books(self):
        AddNewBook.AddNewBook(self.window)

    def update_book(self):
        UpdateBook.UpdateBook(self.window)
        
    def delete_books(self):
        DeleteBook.DeleteBook(self.window)

    def search_books(self):
        search_book.SearchBook(self.window)
        
    def delete_borrowers(self):
        delete_borrower.DeleteBorrower(self.window)

    def hold_books(self):
        hold_book.HoldBook(self.window)

    def delete_holds(self):
        delete_hold.DeleteHold(self.window)
        
    def return_books(self):
        return_book.ReturnBook(self.window)

#MainPage()
