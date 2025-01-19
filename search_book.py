import pandas as pd
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image,ImageTk
from sqlalchemy import create_engine
from tkinter import messagebox
import mysql.connector as con
from datetime import date


my_conn = create_engine("mysql+pymysql://root:@localhost/university_librarydb")

class SearchBook:
    def __init__(self, root):
        self.root = Toplevel(root)
        self.root.title("Search Book")
        
        self.label = Label(self.root, text="Search Book", fg="#1c6f9c", font=("Times New Roman", 20, "bold"))
        self.label.pack()

        # Search entry and button
        self.search_frame = Frame(self.root)
        self.search_frame.pack(pady=10)

        self.search_label = Label(self.search_frame, text="Enter Title or Author:")
        self.search_label.pack(side=LEFT, padx=5)

        self.search_entry = Entry(self.search_frame, width=30)
        self.search_entry.pack(side=LEFT, padx=5)

        self.search_button = Button(self.search_frame, text="Search", command=self.search_book)
        self.search_button.pack(side=LEFT, padx=5)

        # Frame for Treeview
        self.frame = Frame(self.root, width=900, height=400)
        self.frame.pack(expand=True, fill=BOTH)

        # Treeview and scrollbar
        self.tree = ttk.Treeview(self.frame, selectmode="browse")
        self.tree['columns'] = ('1', '2', '3', '4', '5', '6', '7')
        self.tree['show'] = 'headings'

        self.tree.column('1', width=30, anchor='c')
        self.tree.column('2', width=150, anchor='c')
        self.tree.column('3', width=100, anchor='c')
        self.tree.column('4', width=150, anchor='c')
        self.tree.column('5', width=150, anchor='c')
        self.tree.column('6', width=150, anchor='c')
        self.tree.column('7', width=150, anchor='c')
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

        # Place the treeview and scrollbar in the grid
        self.tree.grid(column=0, row=0, padx=20, pady=20, sticky='nsew')
        self.scrollbar.grid(column=1, row=0, sticky='ns')

        # Configure the frame to resize properly
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        self.refresh_button = Button(self.root, text="Refresh", command=self.update_treeview)
        #self.refresh_button.pack(pady=10)

        self.update_treeview()

        self.select_button = Button(self.root, text="Select Book", command=self.select_book)
        self.select_button.pack()

    def update_treeview(self):
        # Clear existing data in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Fetch all data from the books table
        r_set = pd.read_sql("SELECT * FROM books", con=my_conn)
        result = r_set.values.tolist()

        # Insert fetched data into the treeview
        for dt in result:
            self.tree.insert('', 'end', values=(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], dt[6]))

    def select_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            book_id = item['values'][0]  # Fetch the 'id' from the first column
            self.open_update_window(book_id)
        else:
            print("Please select a book to borrow.")
    def open_update_window(self, book_id):
        update_window = Toplevel(self.root)
        update_window.title("Borrow Book")
        update_window.geometry("400x350")
        update_window.resizable(False, False)
        
        
        # Fetch member details
        book_data = pd.read_sql(f"SELECT * FROM books WHERE id={book_id}", con=my_conn).iloc[0]

        Label(update_window, text="Book ID").grid(row=0, column=0, padx=10, pady=10)
        Label(update_window, text="Title").grid(row=1, column=0, padx=10, pady=10)
        Label(update_window, text="Borrow Quantity").grid(row=2, column=0, padx=10, pady=10)
        Label(update_window, text="Member Name").grid(row=3, column=0, padx=10, pady=10)
        Label(update_window, text="Roll No").grid(row=4, column=0, padx=10, pady=10)
        
        bookid_var = StringVar(value=book_data['id'])
        title_var = StringVar(value=book_data['title'])


        qty_bal = book_data['qty_balance']
        myqty = book_data['qty_balance']

        if qty_bal > 3 :
            qty_bal = 3
        else :
            qty_bal = book_data['qty_balance']
        
        bal_var = StringVar(value=qty_bal)
        myqty = StringVar(value=myqty)

        Entry(update_window, textvariable=bookid_var, width=40).grid(row=0, column=1, padx=10, pady=10)
        Entry(update_window, textvariable=title_var, width=40).grid(row=1, column=1, padx=10, pady=10)
        self.bal = tk.Entry(update_window, textvariable=bal_var, width=40)
        self.bal.grid(row=2, column=1, padx=10, pady=10)
        self.bal.bind("<FocusOut>", self.on_focus_out)
        member = Entry(update_window, width=40)
        member.grid(row=3, column=1, padx=10, pady=10)
        rollno = Entry(update_window, width=40)
        rollno.grid(row=4, column=1, padx=10, pady=10)

        self.btn = Image.open("images/save.png")
        self.btn = self.btn.resize((100,50))
        self.btnimg = ImageTk.PhotoImage(self.btn)
        
        borrow_button = Button(update_window, image=self.btnimg, bd=0, cursor="hand2",
                               command=lambda: self.borrow_book(book_id, title_var, bal_var, myqty, member, rollno, update_window))
        borrow_button.grid(row=5, column=0, columnspan=2, pady=10)

    def borrow_book(self, book_id, title_var, bal_var, myqty, member, rollno, update_window):
        id = book_id
        title = title_var.get()
        balance = bal_var.get()
        quantity_balance = myqty.get()
        mbr = member.get()
        roll = rollno.get()

        #print(id, " ", title, " ", balance, " ", mbr, " ", roll)

        dbcon = con.connect(
            host="localhost",
            user="root",
            password="",
            database="university_librarydb"

        )

        q1 = "SELECT id FROM members WHERE name=%s AND roll=%s"
        vals1 = (mbr, roll, )
        cursor1 = dbcon.cursor()
        cursor1.execute(q1, vals1)

        result1 = cursor1.fetchone()


        if result1 :
            q2 = "SELECT SUM(borrowqty) FROM borrowers WHERE member_name=%s AND member_roll=%s"
            vals2 = (mbr, roll, )
            cursor2 = dbcon.cursor()
            cursor2.execute(q2, vals2)

            result2 = cursor2.fetchone()

            if result2 and result2[0] is not None :
                result2 = int(result2[0])
            else :
                result2 = 0
            
            qty = int(balance)
            if result2 >= 3 or result2+qty > 3 :
                messagebox.showwarning("Limit Exceeded", f"Only maximum 3 books can borrow.")

                if self.root :
                    self.root.destroy()
            else :
                query = "INSERT INTO borrowers (book_id, title, borrowqty, member_name, member_roll, borrow_date) VALUES (%s,%s,%s,%s,%s,CURDATE())"
                values = (id, title, qty, mbr, roll, )
                mycursor = dbcon.cursor()
                mycursor.execute(query, values)
                dbcon.commit()


                quantity_balance = int(quantity_balance) - qty
                query1 = "UPDATE books SET qty_balance=%s WHERE id=%s"
                values1 = (quantity_balance, id, )
                mycursor1 = dbcon.cursor()
                mycursor1.execute(query1, values1)
                dbcon.commit()
                messagebox.showinfo("Borrow Success", f"Successfully borrowed!")

                if self.root :
                    self.root.destroy()
                
        else :
            messagebox.showwarning("Not Registered", f"You have not registered in the system. Please register")
            
        
        
        # Insert borrow information into the database
        """query = "UPDATE books SET title=%s, author=%s, category=%s, edition=%s, quantity=%s, qty_balance=%s WHERE id=%s"
        values = (title, auth, catego, edit, qty, bal, book_id, )
        mycursor = dbcon.cursor()
        mycursor.execute(query, values)
        dbcon.commit()
        
        # Refresh the treeview and close the update window
        self.update_treeview()
        update_window.destroy()"""
    
    def on_focus_out(self, event):
        max_chars = 3
        current_text = int(event.widget.get())
        ##messagebox.showwarning("Limit Exceeded", f"{current_text}")
        if current_text > max_chars :
            messagebox.showwarning("Limit Exceeded", f"Only maximum {max_chars} books can borrow.")
    
    def search_book(self):
        # Clear existing data in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Get search input
        search_text = self.search_entry.get()
        
        # Query to find books matching the search text in Title or Author fields
        query = f"SELECT * FROM books WHERE title LIKE '%%{search_text}%%' OR author LIKE '%%{search_text}%%'"
        r_set = pd.read_sql(query, con=my_conn)
        result = r_set.values.tolist()

        # Insert matching records into the treeview
        for dt in result:
            self.tree.insert('', 'end', values=(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], dt[6]))

# Assuming you have a Tkinter root window defined somewhere, you'd initialize ViewBook like this:
# root = Tk()
# view_book_window = ViewBook(root)
# root.mainloop()
