import pandas as pd
from tkinter import *
from tkinter import ttk
from sqlalchemy import create_engine

my_conn = create_engine("mysql+pymysql://root:@localhost/university_librarydb")

class ViewMember:
    def __init__(self, root):
        self.root = Toplevel(root)
        self.root.title("Member List")
        self.label = Label(self.root, text="Member List", fg="#1c6f9c", font=("Times New Roman", 20,"bold"))
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
        self.tree.heading('1', text='id')
        self.tree.heading('2', text='Name')
        self.tree.heading('3', text='Roll No')
        self.tree.heading('4', text='Class')

        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Place the treeview and scrollbar in the grid
        self.tree.grid(column=0, row=0, padx=20, pady=20, sticky='nsew')
        self.scrollbar.grid(column=1, row=0, sticky='ns')

        # Configure the frame to resize properly
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        self.refresh_button = Button(self.root, text="Refresh", command=self.update_treeview)

        #self.refresh_button.pack()

        self.update_treeview()

        self.root.mainloop()

    def update_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        r_set = pd.read_sql("Select * from members", con=my_conn)
        result = r_set.values.tolist()

        for  dt in result:
            self.tree.insert('', 'end', values=( dt[0], dt[1], dt[2],dt[3] ))

# Assuming you have a Tkinter root window defined somewhere, you'd initialize ViewMember like this:
# root = Tk()
# view_member_window = ViewMember(root)
# root.mainloop()
