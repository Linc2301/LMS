import pandas as pd
from tkinter import *
from tkinter import ttk
from sqlalchemy import create_engine

my_conn = create_engine("mysql+pymysql://root:@localhost/university_librarydb")

class DeleteMember:
    def __init__(self, root):
        self.root = Toplevel(root)
        self.root.title("Delete Member")
        self.label = Label(self.root, text="Delete Member", fg="#1c6f9c", font=("Times New Roman", 20))
        self.label.pack()
        self.frame = Frame(self.root, width=900, height=400)
        self.frame.pack(expand=TRUE, fill=BOTH)
        
        self.tree = ttk.Treeview(self.frame, selectmode="browse")
        self.tree.grid(column=1, row=1, padx=20, pady=20)
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

        self.select_button = Button(self.root, text="Delete Member", command=self.select_member)
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
            self.delete_member(member_id)
        else:
            print("Please select a member to delete.")

    def delete_member(self, member_id):
        query = "DELETE FROM members WHERE id=%s"
        with my_conn.connect() as conn:
            conn.execute(query, (member_id,))  # Execute the delete query

        # Refresh the treeview
        self.update_treeview()
        print(f"Member with ID {member_id} deleted successfully.")

# Assuming you have a Tkinter root window defined somewhere, you'd initialize DeleteMember like this:
# root = Tk()
# delete_member_window = DeleteMember(root)
# root.mainloop()
