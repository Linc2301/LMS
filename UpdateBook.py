import pandas as pd
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from sqlalchemy import create_engine, text
import mysql.connector as con
import textwrap

my_conn = create_engine("mysql+pymysql://root:@localhost/university_librarydb")

class UpdateBook:
    def __init__(self, root):
        self.root = Toplevel(root)
        self.root.title("University Library Management System")
        self.root.resizable(False, False)
        self.label = Label(self.root, text="List of Books", fg="#1c6f9c", font=("Times New Roman", 20))
        self.label.pack()
        
        self.frame = Frame(self.root, width=950, height=400)
        self.frame.pack(expand=TRUE, fill=BOTH)


        #self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        #self.scrollbar.pack(side=RIGHT, fill=Y)
        #self.scrollbar.config(command=self.tree.yview)
        
        
        self.tree = ttk.Treeview(self.frame, selectmode="browse")
        #self.tree.grid(column=1, row=1, padx=20, pady=20)
        self.tree.grid(column=0, row=0, padx=20, pady=20, sticky='nsew')
        self.tree['columns'] = ('1', '2', '3', '4', '5', '6', '7')
        self.tree['show'] = 'headings'

        self.tree.column('1', width=30, anchor='c')
        self.tree.column('2', width=300, anchor='c')
        self.tree.column('3', width=100, anchor='c')
        self.tree.column('4', width=150, anchor='c')
        self.tree.column('5', width=150, anchor='c')
        self.tree.column('6', width=100, anchor='c')
        self.tree.column('7', width=100, anchor='c')
        
        self.tree.heading('1', text='ID')
        self.tree.heading('2', text='Title')
        self.tree.heading('3', text='Author')
        self.tree.heading('4', text='Category')
        self.tree.heading('5', text='Edition')
        self.tree.heading('6', text='Quantity')
        self.tree.heading('7', text='Qty Balance')

        # Add vertical scrollbar
        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(column=1, row=0, sticky='ns')

        self.update_treeview()

        self.select_button = Button(self.root, text="Select Book", command=self.select_book)
        self.select_button.pack()

        self.root.mainloop()

    def update_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        r_set = pd.read_sql("SELECT * FROM books", con=my_conn)
        result = r_set.values.tolist()

        for dt in result:
            self.tree.insert('', 'end', values=(dt[0], self.wrap(dt[1]), self.wrap(dt[2]), self.wrap(dt[3]), dt[4], dt[5], dt[6]))

    def wrap(self, string, length=20):
        return '\n'.join(textwrap.wrap(string, length))

    def select_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            book_id = item['values'][0]  # Fetch the 'id' from the first column
            self.open_update_window(book_id)
        else:
            print("Please select a member to update.")

    def open_update_window(self, book_id):
        update_window = Toplevel(self.root)
        update_window.title("Edit Book Information")
        update_window.geometry("400x350")
        update_window.resizable(False, False)
        
        
        # Fetch member details
        book_data = pd.read_sql(f"SELECT * FROM books WHERE id={book_id}", con=my_conn).iloc[0]
        
        Label(update_window, text="Title").grid(row=0, column=0, padx=10, pady=10)
        Label(update_window, text="Author").grid(row=1, column=0, padx=10, pady=10)
        Label(update_window, text="Category").grid(row=2, column=0, padx=10, pady=10)
        Label(update_window, text="Edition").grid(row=3, column=0, padx=10, pady=10)
        Label(update_window, text="Quantity").grid(row=4, column=0, padx=10, pady=10)
        Label(update_window, text="Qty Balance").grid(row=5, column=0, padx=10, pady=10)
        
        book_var = StringVar(value=book_data['title'])
        auth_var = StringVar(value=book_data['author'])
        catego_var = StringVar(value=book_data['category'])
        edit_var = StringVar(value=book_data['edition'])
        qty_var = StringVar(value=book_data['quantity'])
        bal_var = StringVar(value=book_data['qty_balance'])

        Entry(update_window, textvariable=book_var, width=40).grid(row=0, column=1, padx=10, pady=10)
        Entry(update_window, textvariable=auth_var, width=40).grid(row=1, column=1, padx=10, pady=10)
        Entry(update_window, textvariable=catego_var, width=40).grid(row=2, column=1, padx=10, pady=10)
        Entry(update_window, textvariable=edit_var, width=40).grid(row=3, column=1, padx=10, pady=10)
        Entry(update_window, textvariable=qty_var, width=40).grid(row=4, column=1, padx=10, pady=10)
        Entry(update_window, textvariable=bal_var, width=40).grid(row=5, column=1, padx=10, pady=10)

        self.btn = Image.open("images/updatebtn.png")
        self.btn = self.btn.resize((100,50))
        self.btnimg = ImageTk.PhotoImage(self.btn)
        
        update_button = Button(update_window, image=self.btnimg, bd=0, cursor="hand2",
                               command=lambda: self.update_book(book_id, book_var, auth_var, catego_var, edit_var, qty_var, bal_var, update_window))
        update_button.grid(row=6, column=0, columnspan=2, pady=10)

    def update_book(self, book_id, book_var, auth_var, catego_var, edit_var,qty_var, bal_var, update_window):
        title = book_var.get()
        auth = auth_var.get()
        catego = catego_var.get()
        edit = edit_var.get()
        qty = qty_var.get()
        bal = bal_var.get()

        dbcon = con.connect(
            host="localhost",
            user="root",
            password="",
            database="university_librarydb"

        )
        
        # Update member information in the database
        query = "UPDATE books SET title=%s, author=%s, category=%s, edition=%s, quantity=%s, qty_balance=%s WHERE id=%s"
        values = (title, auth, catego, edit, qty, bal, book_id, )
        mycursor = dbcon.cursor()
        mycursor.execute(query, values)
        dbcon.commit()
        
        # Refresh the treeview and close the update window
        self.update_treeview()
        update_window.destroy()


            
        
