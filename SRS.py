
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk

import mysql.connector


#connection for Mysql using variable mydb
def connection():
    mydb = (mysql.connector.connect(host="localhost" , user="root" , passwd = "#220220022" , database="faraz"))
    return mydb

def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=20, pady=20)

def refreshEnqueued():
    enqueued_listbox.delete(0, END)
    for item in queue:
        enqueued_listbox.insert(END, item)

def refreshDequeued():
    dequeued_listbox.delete(0, END)
    for item in dequeued:
        dequeued_listbox.insert(END, item)


queue = []
dequeued = []

def enqueue(item):
    queue.append(item)
    refreshEnqueued()

# Apply dequeue to delete record from the database and dequeue list
def dequeue():
    if len(queue) > 0:
        dequeued_item = queue.pop(0)
        dequeued.append(dequeued_item)
        refreshEnqueued()
        refreshDequeued()
        return dequeued_item
    else:
        return None


window = Tk()
window.title("Student Registration System")
window.geometry("1830x840")
my_tree = ttk.Treeview(window)

#placeholders for entry
ph1 = tk.StringVar()
ph2 = tk.StringVar()
ph3 = tk.StringVar()
ph4 = tk.StringVar()
ph5 = tk.StringVar()

#placeholder set value function
def setph(word,num):
    if num ==1:
        ph1.set(word)
    if num ==2:
        ph2.set(word)
    if num ==3:
        ph3.set(word)
    if num ==4:
        ph4.set(word)
    if num ==5:
        ph5.set(word)








def read():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def add():
    std_id = str(std_idEntry.get())
    std_name = str(std_nameEntry.get())
    std_age = str(std_ageEntry.get())
    std_gender = str(std_genderEntry.get())
    std_add = str(std_addEntry.get())

    if (std_id == "" or std_id == " ") or (std_name == "" or std_name == " ") or (std_age == "" or std_age == " ") or (std_gender == "" or std_gender == " ") or (std_add == "" or std_add == " "):
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO student VALUES ('"+std_id+"','"+std_name+"','"+std_age+"','"+std_gender+"','"+std_add+"') ")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Stud ID already exist")
            return
    refreshTable()

    
    

def reset():
    decision = messagebox.askquestion("Warning!!", "Delete all data?")
    if decision != "yes":
        return
    else:
        try:
            mydb = connection()
            cursor = mydb.cursor()
            cursor.execute("DELETE FROM student")
            mydb.commit()
            mydb.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return
        refreshTable()


def delete():
    decision = messagebox.askquestion("Warning!!", "Delete the selected data?")
    if decision != "yes":
        return
    else:
        selected_item = my_tree.selection()[0]
        deleteData = str(my_tree.item(selected_item)['values'][0])
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM student WHERE std_id='" + str(deleteData) + "'")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Can't delete data")
            return
        messagebox.showinfo("Successful", "Data Deleted")
        refreshTable()

        # Remove item from the FIFO queue if it exists
        if queue and deleteData == queue[0][0]:
            dequeue()


def enqueueRecord():
    selected_items = my_tree.selection()
    if selected_items:
        selected_item = selected_items[0]
        # Retrieve the values from the selected item
        std_id = my_tree.item(selected_item, 'values')[0]
        std_name = my_tree.item(selected_item, 'values')[1]
        std_age = my_tree.item(selected_item, 'values')[2]
        std_gender = my_tree.item(selected_item, 'values')[3]
        std_add = my_tree.item(selected_item, 'values')[4]
        
        # Enqueue the selected record
        enqueue((std_id, std_name, std_age, std_gender, std_add))
        
        messagebox.showinfo("Enqueue", "Record enqueued successfully.")
    else:
        messagebox.showinfo("Error", "Please select a record.")
    


def dequeueRecord():
    dequeueData = dequeue()
    if dequeueData:
        messagebox.showinfo("Dequeue", "Dequeued Record:\n\n" + str(dequeueData))
    else:
        messagebox.showinfo("Dequeue", "The queue is empty.")

        
def select():
    try:
        selected_item = my_tree.selection()[0]
        std_id = str(my_tree.item(selected_item)['values'][0])
        std_name = str(my_tree.item(selected_item)['values'][1])
        std_age = str(my_tree.item(selected_item)['values'][2])
        std_gender = str(my_tree.item(selected_item)['values'][3])
        std_add = str(my_tree.item(selected_item)['values'][4])

        setph(std_id,1)
        setph(std_name,2)
        setph(std_age,3)
        setph(std_gender,4)
        setph(std_add,5)
    except:
        messagebox.showinfo("Error", "Please select a data row")

def search():
    std_id = str(std_idEntry.get())
    std_name = str(std_nameEntry.get())
    std_age = str(std_ageEntry.get())
    std_gender = str(std_genderEntry.get())
    std_add = str(std_addEntry.get())

    mydb = connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM student WHERE std_id='"+
    std_id+"' or std_name='"+
    std_name+"' or std_age='"+
    std_age+"' or std_gender='"+
    std_gender+"' or std_add='"+
    std_add+"' ")
    
    try:
        result = cursor.fetchall()

        for num in range(0,5):
            setph(result[0][num],(num+1))

        mydb.commit()
        mydb.close()
    except:
        messagebox.showinfo("Error", "No data found")

def update():
    selectedstd_id = ""

    try:
        selected_item = my_tree.selection()[0]
        selectedstd_id = str(my_tree.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error", "Please select a data row")

    std_id = str(std_idEntry.get())
    std_name = str(std_nameEntry.get())
    std_age = str(std_ageEntry.get())
    std_gender = str(std_genderEntry.get())
    std_add = str(std_addEntry.get())

    if (std_id == "" or std_id == " ") or (std_name == "" or std_name == " ") or (std_age == "" or std_age == " ") or (std_gender == "" or std_gender == " ") or (std_add == "" or std_add == " "):
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            mydb = connection()
            cursor = mydb.cursor()
            cursor.execute("UPDATE student SET std_id='"+
            std_id+"', std_name='"+
            std_name+"', std_age='"+
            std_age+"', std_gender='"+
            std_gender+"', std_add='"+
            std_add+"' WHERE std_id='"+
            selectedstd_id+"' ")
            mydb.commit()
            mydb.close()
        except:
            messagebox.showinfo("Error", "Stud ID already exist")
            return
    refreshTable()

    

label = Label(window, text="STUDENT REGISTRATION SYSTEM (CRUD)", font=('Arial Bold', 30), bg="black", fg="white", borderwidth=4, relief="solid")
label.grid(row=0, column=0, columnspan=8, rowspan=2, padx=50, pady=40)

enqueued_label = Label(window, text="Enqueued Records", font=('Arial Bold', 20))
enqueued_label.grid(row=7, column=6, columnspan=2, padx=5, pady=5)

enqueued_listbox = Listbox(window, width=30, height=10, font=('Arial', 12))
enqueued_listbox.grid(row=8, column=6, columnspan=2, rowspan=11, padx=20, pady=20)

dequeued_label = Label(window, text="Dequeued Records", font=('Arial Bold', 20))
dequeued_label.grid(row=7, column=9, columnspan=2, padx=5, pady=5)

dequeued_listbox = Listbox(window, width=30, height=10, font=('Arial', 12))
dequeued_listbox.grid(row=8, column=9, columnspan=2, rowspan=11, padx=20, pady=20)


menubar = Menu(window)
window.config(menu=menubar)
std_menu= Menu(menubar, tearoff=False)
std_menu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=std_menu)

edit_menu = Menu(menubar, tearoff=False)
edit_menu.add_command(label="Enqueue", command=enqueueRecord)
menubar.add_separator()
edit_menu.add_command(label="Dequeue", command=dequeueRecord)
menubar.add_cascade(label="Edit", menu=edit_menu)

std_idLabel = Label(window, text="Student_ID", font=('Arial Bold', 20))
std_nameLabel = Label(window, text="Student_Name", font=('Arial Bold', 20))
std_ageLabel = Label(window, text="Student_Age", font=('Arial Bold', 20))
std_genderLabel = Label(window, text="Student_Gender", font=('Arial Bold', 20))
std_addLabel = Label(window, text="Student_Address", font=('Arial Bold', 20))

std_idLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
std_nameLabel.grid(row=4, column=0, columnspan=1, padx=50, pady=5)
std_ageLabel.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
std_genderLabel.grid(row=6, column=0, columnspan=1, padx=50, pady=5)
std_addLabel.grid(row=7, column=0, columnspan=1, padx=50, pady=5)

std_idEntry = Entry(window, width=55, bd=5, font=('Arial', 15), textvariable = ph1)
std_nameEntry = Entry(window, width=55, bd=5, font=('Arial', 15), textvariable = ph2)
std_ageEntry = Entry(window, width=55, bd=5, font=('Arial', 15), textvariable = ph3)
std_genderEntry = Entry(window, width=55, bd=5, font=('Arial', 15), textvariable = ph4)
std_addEntry = Entry(window, width=55, bd=5, font=('Arial', 15), textvariable = ph5)

std_idEntry.grid(row=3, column=1, columnspan=4, padx=5, pady=0)
std_nameEntry.grid(row=4, column=1, columnspan=4, padx=5, pady=0)
std_ageEntry.grid(row=5, column=1, columnspan=4, padx=5, pady=0)
std_genderEntry.grid(row=6, column=1, columnspan=4, padx=5, pady=0)
std_addEntry.grid(row=7, column=1, columnspan=4, padx=5, pady=0)

addBtn = Button(
    window, text="Add", padx=65, pady=25, width=10,
    bd=15, font=('Arial Bold', 15), bg="#84F894", command=add)
updateBtn = Button(
    window, text="Update", padx=65, pady=25, width=10,
    bd=15, font=('Arial Bold', 15), bg="#84E8F8", command=update)
deleteBtn = Button(
    window, text="Delete", padx=65, pady=25, width=10,
    bd=15, font=('Arial Bold', 15), bg="#FF9999", command=delete)
searchBtn = Button(
    window, text="Search", padx=65, pady=25, width=10,
    bd=15, font=('Arial Bold', 15), bg="#F4FE82", command=search)
resetBtn = Button(
    window, text="Reset", padx=65, pady=25, width=10,
    bd=15, font=('Arial Bold', 15), bg="#F398FF", command=reset)
selectBtn = Button(
    window, text="Select", padx=65, pady=25, width=10,
    bd=15, font=('Arial Bold', 15), bg="#EEEEEE", command=select)

addBtn.grid(row=3, column=5, columnspan=1, rowspan=2)
updateBtn.grid(row=5, column=5, columnspan=1, rowspan=2)
deleteBtn.grid(row=7, column=5, columnspan=1, rowspan=2)
searchBtn.grid(row=9, column=5, columnspan=1, rowspan=2)
resetBtn.grid(row=11, column=5, columnspan=1, rowspan=2)
selectBtn.grid(row=13, column=5, columnspan=1, rowspan=2)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial Bold', 12),bg='black',fg='white' )

my_tree['columns'] = ("Stud ID","Firstname","Age","Gender","Address")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Stud ID", anchor=W, width=170)
my_tree.column("Firstname", anchor=W, width=150)
my_tree.column("Age", anchor=W, width=150)
my_tree.column("Gender", anchor=W, width=165)
my_tree.column("Address", anchor=W, width=150)

my_tree.heading("Stud ID", text="Student ID", anchor=W)
my_tree.heading("Firstname", text="Student name", anchor=W)
my_tree.heading("Age", text="Age", anchor=W)
my_tree.heading("Gender", text="Gender", anchor=W)
my_tree.heading("Address", text="Address", anchor=W)

my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=20, pady=20)



refreshTable()

window.mainloop()