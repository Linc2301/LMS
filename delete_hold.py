import pandas as pd
from tkinter import *
from tkinter import ttk
from sqlalchemy import create_engine, text
import mysql.connector as con

my_conn = create_engine("mysql+pymysql://root:@localhost/university_librarydb")

class DeleteHold:
    def __init__(self, root):
        self.root = Toplevel(root)
        self.root.title("Delete Hold")
        self.label = Label(self.root, text="Delete Hold Information", fg="#1c6f9c", font=("Times New Roman", 20,"bold"))
        self.label.pack()
        self.frame = Frame(self.root, width=900, height=400)
        self.frame.pack(expand=TRUE, fill=BOTH)
        
        self.tree = ttk.Treeview(self.frame, selectmode="browse")
        
        self.tree['columns'] = ('1', '2', '3', '4', '5', '6','7')
        self.tree['show'] = 'headings'

        self.tree.column('1', width=30, anchor='c')
        self.tree.column('2', width=150, anchor='c')
        self.tree.column('3', width=100, anchor='c')
        self.tree.column('4', width=150, anchor='c')
        self.tree.column('5', width=150, anchor='c')
        self.tree.column('6', width=150, anchor='c')
        self.tree.column('7', width=150, anchor='c')
        self.tree.heading('1', text='ID')
        self.tree.heading('2', text='Book ID')
        self.tree.heading('3', text='Title')
        self.tree.heading('4', text='Hold Quantity')
        self.tree.heading('5', text='Member Name')
        self.tree.heading('6', text='Roll Number')
        self.tree.heading('7', text='Date')
        self.update_treeview()

        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Place the treeview and scrollbar in the grid
        self.tree.grid(column=0, row=0, padx=20, pady=20, sticky='nsew')
        self.scrollbar.grid(column=1, row=0, sticky='ns')

        # Configure the frame to resize properly
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)


        self.select_button = Button(self.root, text="Delete Book", command=self.select_book)
        self.select_button.pack()

        self.root.mainloop()

    def update_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        r_set = pd.read_sql("SELECT * FROM holds", con=my_conn)
        result = r_set.values.tolist()

        for dt in result:
            self.tree.insert('', 'end', values=(dt[0], dt[1], dt[2], dt[3], dt[4],dt[5], dt[6]))

    def select_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            hold_id = item['values'][0]  # Fetch the 'id' from the first column
            self.delete_book(hold_id)
        else:
            print("Please select a book to delete.")

    
    def delete_book(self, hold_id):
        #name = name_var.set('')
        #roll_no = roll_var.set('')
        #department = department_var.set('')

        dbcon = con.connect(
            host="localhost",
            user="root",
            password="",
            database="university_librarydb"

        )
        
        # Update member information in the database
        query = "DELETE FROM holds WHERE id=%s"
        #params = {"name": name, "roll_no": roll_no, "department": department, "member_id": member_id}
        values = ( book_id, )
        """with my_conn.connect() as conn:
            conn.execute(query, params)"""
        mycursor = dbcon.cursor()
        mycursor.execute(query, values)
        dbcon.commit()
        
        # Refresh the treeview and close the update window
        self.update_treeview()
        #update_window.destroy()

# Assuming you have a Tkinter root window defined somewhere, you'd initialize UpdateMember like this:
# root = Tk()
# update_member_window = UpdateMember(root)
# root.mainloop()
