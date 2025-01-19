import pandas as pd
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import mysql.connector as con
from sqlalchemy import create_engine

# Replace with your database engine connection
my_conn = create_engine("mysql+pymysql://root:@localhost/university_librarydb")

class ReturnBook:
    def __init__(self, root):
        self.root = Toplevel(root)
        self.root.title("Return Book")

        self.label = Label(self.root, text="Return Book", fg="#1c6f9c", font=("Times New Roman", 20, "bold"))
        self.label.pack()

        # Frame for treeview and search entry
        self.search_frame = Frame(self.root)
        self.search_frame.pack(pady=10)
    
        # Frame for treeview
        self.frame = Frame(self.root, width=900, height=400)
        self.frame.pack(expand=True, fill=BOTH)

        # Treeview to display borrowed books
        self.tree = ttk.Treeview(self.frame, selectmode="browse")
        self.tree['columns'] = ('1', '2', '3', '4', '5', '6')
        self.tree['show'] = 'headings'

        # Setting column properties
        self.tree.column('1', width=30, anchor='c')
        self.tree.column('2', width=150, anchor='c')
        self.tree.column('3', width=100, anchor='c')
        self.tree.column('4', width=150, anchor='c')
        self.tree.column('5', width=150, anchor='c')
        self.tree.column('6', width=150, anchor='c')
        self.tree.heading('1', text='Borrow ID')
        self.tree.heading('2', text='Book ID')
        self.tree.heading('3', text='Title')
        self.tree.heading('4', text='Quantity')
        self.tree.heading('5', text='Member Name')
        self.tree.heading('6', text='Roll No')
        self.update_treeview()

        # Adding scrollbar
        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.grid(column=0, row=0, padx=20, pady=20, sticky='nsew')
        self.scrollbar.grid(column=1, row=0, sticky='ns')

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        # Return book button
        self.return_button = Button(self.root, text="Return Book", command=self.return_book)
        self.return_button.pack(pady=10)
    def update_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        r_set = pd.read_sql("SELECT * FROM borrowers", con=my_conn)
        result = r_set.values.tolist()

        for dt in result:
            self.tree.insert('', 'end', values=(dt[0], dt[1], dt[2], dt[3], dt[4],dt[5], dt[6]))
    '''
    def search_borrowed_books(self):
        # Clear treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        roll_no = self.search_entry.get()
    
        if not roll_no:
            messagebox.showwarning("Input Error", "Please enter a member roll number.")
            return
    
        # Fetch borrowed books data
        query = f"SELECT * FROM borrowers WHERE member_roll = '{roll_no}'"
        r_set = pd.read_sql(query, con=my_conn)
        result = r_set.values.tolist()

        if not result:
            messagebox.showinfo("No Records", "No borrowed books found for the given roll number.")
            return

        # Insert data into treeview
        for dt in result:
            self.tree.insert('', 'end', values=(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5]))
    '''
    def return_book(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a book to return.")
            return

        item = self.tree.item(selected_item)
        borrow_id = item['values'][0]
        book_id = item['values'][1]
        return_qty = item['values'][3]

        # Database connection
        dbcon = con.connect(
            host="localhost",
            user="root",
            password="",
            database="university_librarydb"
        )

        cursor = dbcon.cursor()

        # Delete the borrow record
        cursor.execute("DELETE FROM borrowers WHERE id = %s", (borrow_id,))
        dbcon.commit()

        # Update the book's qty_balance
        cursor.execute("UPDATE books SET qty_balance = qty_balance + %s WHERE id = %s", (return_qty, book_id))
        dbcon.commit()

        messagebox.showinfo("Return Success", "Book successfully returned.")
        #self.search_borrowed_books()  # Refresh treeview

        dbcon.close()

# Example usage:
# root = Tk()
# return_book_window = ReturnBook(root)
# root.mainloop()
