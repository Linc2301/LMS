import pandas as pd
from tkinter import *
from tkinter import ttk
from sqlalchemy import create_engine, text
import mysql.connector as con

my_conn = create_engine("mysql+pymysql://root:@localhost/university_librarydb")

class UpdateMember:
    def __init__(self, root):
        self.root = Toplevel(root)
        self.root.title("Update Member")
        self.label = Label(self.root, text="Update Member Information", fg="#1c6f9c", font=("Times New Roman", 20,"bold"))
        self.label.pack()
        self.frame = Frame(self.root, width=900, height=400)
        self.frame.pack(expand=TRUE, fill=BOTH)
        
        self.tree = ttk.Treeview(self.frame, selectmode="browse")
        
        self.tree['columns'] = ('1', '2', '3', '4')
        self.tree['show'] = 'headings'

        self.tree.column('1', width=30, anchor='c')
        self.tree.column('2', width=150, anchor='c')
        self.tree.column('3', width=100, anchor='c')
        self.tree.column('4', width=150, anchor='c')
        self.tree.heading('1', text='ID')
        self.tree.heading('2', text='Name')
        self.tree.heading('3', text='Roll No')
        self.tree.heading('4', text='Department')

        self.update_treeview()

        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Place the treeview and scrollbar in the grid
        self.tree.grid(column=0, row=0, padx=20, pady=20, sticky='nsew')
        self.scrollbar.grid(column=1, row=0, sticky='ns')

        # Configure the frame to resize properly
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)


        self.select_button = Button(self.root, text="Select Member", command=self.select_member)
        self.select_button.pack()

        self.root.mainloop()

    def update_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        r_set = pd.read_sql("SELECT * FROM members", con=my_conn)
        result = r_set.values.tolist()

        for dt in result:
            self.tree.insert('', 'end', values=(dt[0], dt[1], dt[2], dt[3]))

    def select_member(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            member_id = item['values'][0]  # Fetch the 'id' from the first column
            self.open_update_window(member_id)
        else:
            print("Please select a member to update.")

    def open_update_window(self, member_id):
        update_window = Toplevel(self.root)
        update_window.title("Edit Member Information")
        
        # Fetch member details
        member_data = pd.read_sql(f"SELECT * FROM members WHERE id={member_id}", con=my_conn).iloc[0]
        
        Label(update_window, text="Name").grid(row=0, column=0, padx=10, pady=10)
        Label(update_window, text="Roll No").grid(row=1, column=0, padx=10, pady=10)
        Label(update_window, text="Department").grid(row=2, column=0, padx=10, pady=10)
        
        name_var = StringVar(value=member_data['name'])
        roll_var = StringVar(value=member_data['roll'])
        department_var = StringVar(value=member_data['department'])

        Entry(update_window, textvariable=name_var).grid(row=0, column=1, padx=10, pady=10)
        Entry(update_window, textvariable=roll_var).grid(row=1, column=1, padx=10, pady=10)
        Entry(update_window, textvariable=department_var).grid(row=2, column=1, padx=10, pady=10)

        """txtname = Entry(update_window, text=name_var).grid(row=0, column=1, padx=10, pady=10)
        txtroll = Entry(update_window, text=roll_var).grid(row=1, column=1, padx=10, pady=10)
        txtdept = Entry(update_window, text=department_var).grid(row=2, column=1, padx=10, pady=10)"""


        update_button = Button(update_window, text="Update", 
                               command=lambda: self.update_member(member_id, name_var, roll_var, department_var, update_window))
        update_button.grid(row=3, column=0, columnspan=2, pady=10)

    def update_member(self, member_id, name_var, roll_var, department_var, update_window):
        name = name_var.get()
        roll_no = roll_var.get()
        department = department_var.get()

        dbcon = con.connect(
            host="localhost",
            user="root",
            password="",
            database="university_librarydb"

        )
        
        # Update member information in the database
        query = "UPDATE members SET name=%s, roll=%s, department=%s WHERE id=%s"
        #params = {"name": name, "roll_no": roll_no, "department": department, "member_id": member_id}
        values = (name, roll_no, department, member_id, )
        """with my_conn.connect() as conn:
            conn.execute(query, params)"""
        mycursor = dbcon.cursor()
        mycursor.execute(query, values)
        dbcon.commit()
        
        # Refresh the treeview and close the update window
        self.update_treeview()
        update_window.destroy()

# Assuming you have a Tkinter root window defined somewhere, you'd initialize UpdateMember like this:
# root = Tk()
# update_member_window = UpdateMember(root)
# root.mainloop()
