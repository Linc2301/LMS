import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector as con
import MainPage


def SignIn():
    username = user.get()
    password = password1.get()

    condb = con.connect(
                host="localhost",
                user="root",
                password="",
                database="university_librarydb"
            )
    mycursor = condb.cursor()
    query = "SELECT * FROM users WHERE name=%s AND password=%s"
    value = (username, password )
    mycursor.execute(query, value)
    result = mycursor.fetchone()

    if result:
        open_mainPage()
    else:
        messagebox.showerror("Login", "User name or password is incorrect. Please try again")
        user_entry.delete(0, tk.END)
        pwd_entry.delete(0, tk.END)
    '''
    if username=="admin" and password=="232002":
        screen = Toplevel(root)
        screen.title("Welcome")
        screen.geometry("925x500+300+200")
        screen.configure(bg="white")

        Label(screen, text="Welcome to the application",bg="#fff", font=("Arial", 20)).pack(expand=True)
        screen.mainloop()
    elif username!="admin" and password!="232002":
        messagebox.showerror("Invalid","Username or Password is incorrect.")

    elif password!="232002":
        messagebox.showerror("Invalid","Password is incorrect.")

    elif username!="admin":
        messagebox.showerror("Invalid","Username is incorrect.")
    '''
def open_mainPage():
        root.destroy()
        MainPage.MainPage()

root = tk.Tk()
root.title("Login")
root.geometry("925x500+300+200")
root.configure(bg="#fff")
root.resizable(False,False)

img = tk.PhotoImage(file="C:\\Users\\Lenovo\\Desktop\\Python Project\\Login\\login.png")
tk.Label(root,image=img,bg="white").place(x=50,y=50)


frame = tk.Frame(root,width=350,height=350,bg='white')
frame.place(x=480,y=70)

heading=tk.Label(frame,text="Login",fg="#57a1f8",bg="white",font=("Times",50,'bold'))
heading.place(x=100,y=5)

#username
def on_enter(e):
    user1 = user.get()
    if user1 == "Username":
        user.delete(0,'end')
def on_exit(e):
    name=user.get()
    if name=="":
        user.insert(0,'Username')

user = tk.Entry(frame,width=25,fg="black",border=0,bg="white",font=("Times",15))
user.place(x=30,y=100)
user.insert(0,'Username')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_exit)
tk.Frame(frame,width=295,height=2,bg='black').place(x=25,y=127)

#password
def on_enter(e):
    passwd = password1.get()
    if passwd == "Password":
        password1.delete(0,'end')
       

def on_exit(e):
    passw=password1.get()
    if passw=="":
        password1.insert(0,'Password')
        password1.config(show="")
def pwdHide(e):
      password1.config(show="*")
password1 = tk.Entry(frame,width=25,fg="black",border=0,bg="white",font=("Times",15))
password1.place(x=30,y=150)
password1.insert(0,'Password')
password1.bind('<FocusIn>',on_enter)
password1.bind('<FocusOut>',on_exit)
password1.bind('<KeyRelease>', pwdHide)
tk.Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

#login button
tk.Button(frame,width=39,height=2,pady=7,text='Sign in',bg='#57a1f8',border=0,fg='white',command=SignIn).place(x=35,y=204)
label=tk.Label(frame,text="Don't have any accounts?",fg='black',bg='white',font=("Times",10))
label.place(x=75,y=270)

sign_up = tk.Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='#57a1f8')
sign_up.place(x=215,y=270)
root.mainloop()

