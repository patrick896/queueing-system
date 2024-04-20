import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox as mb
import mysql.connector
import customtkinter as ctk
import pyttsx3

def call_out_counter_one():
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
    except mysql.connector.Error as err:
        mb.showerror('Database error', f'Error: {err}')
        return
    
    cursor = conn.cursor()
    
    # Fetch the latest task ID from the serving queue for COUNTER 1
    cursor.execute('SELECT task_id, priority FROM queue WHERE status = "PROCESSING" AND counter = "COUNTER 1" ORDER BY priority = "P" DESC, created_at ASC LIMIT 1')
    entry = cursor.fetchone()
    
    if entry:
        task_id, status = entry
        
        if status == "P":
            text = f"Priority queue number {task_id}, please proceed to counter 1."
        else:
            text = f"Queue number {task_id}, please proceed to counter 1."
        
        # Voice out the message
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    else:
        error ='No serving tasks in the queue for COUNTER 1.'
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(error)
        engine.runAndWait()

    cursor.close()
    conn.close()

def call_out_counter_two():
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
    except mysql.connector.Error as err:
        mb.showerror('Database error', f'Error: {err}')
        return
    
    cursor = conn.cursor()
    
    # Fetch the latest task ID from the serving queue for COUNTER 1
    cursor.execute('SELECT task_id, priority FROM queue WHERE status = "PROCESSING" AND counter = "COUNTER 2" ORDER BY priority = "P" DESC, created_at ASC LIMIT 1')
    entry = cursor.fetchone()
    
    if entry:
        task_id, status = entry
        
        if status == "P":
            text = f"Priority queue number {task_id}, please proceed to counter 2."
        else:
            text = f"Queue number {task_id}, please proceed to counter 2."
        
        # Voice out the message
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    else:
        error ='No serving tasks in the queue for COUNTER 2.'
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(error)
        engine.runAndWait()

    cursor.close()
    conn.close()


def serve_queue_two():
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
    except mysql.connector.Error as err:
        mb.showerror('Database error', f'Error: {err}')
        return
    
    cursor = conn.cursor()
    
    # Fetch the first entry from the queue table for COUNTER 1
    cursor.execute('SELECT task_id, priority, status FROM queue WHERE status IN ("PENDING", "PROCESSING") AND counter = "COUNTER 2" ORDER BY priority = "P" DESC, created_at ASC LIMIT 1')
    entry = cursor.fetchone()
    
    if entry:
        task_id, priority, status = entry
        
        # Update status to "processing" if it's "pending", and to "completed" if it's "processing"
        new_status = "PROCESSING" if status == "PENDING" else "COMPLETED"
        
        # Update status
        cursor.execute('UPDATE queue SET status = %s WHERE task_id = %s', (new_status, task_id))
        conn.commit()
        
        # Display task_id and priority in the serving_queue_frame
        stats2.configure(text=str(new_status))
        servingq2.configure(text=str(task_id))
        servingp2.configure(text=str(priority))
    else:
        mb.showinfo('Info', 'No pending tasks in the queue for COUNTER 2.')

    cursor.close()
    conn.close()

def serve_queue_one():
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
    except mysql.connector.Error as err:
        mb.showerror('Database error', f'Error: {err}')
        return
    
    cursor = conn.cursor()
    
    # Fetch the first entry from the queue table for COUNTER 1
    cursor.execute('SELECT task_id, priority, status FROM queue WHERE status IN ("PENDING", "PROCESSING") AND counter = "COUNTER 1" ORDER BY priority = "P" DESC, created_at ASC LIMIT 1')
    entry = cursor.fetchone()
    
    if entry:
        task_id, priority, status = entry
        
        # Update status to "processing" if it's "pending", and to "completed" if it's "processing"
        new_status = "PROCESSING" if status == "PENDING" else "COMPLETED"
        
        # Update status
        cursor.execute('UPDATE queue SET status = %s WHERE task_id = %s', (new_status, task_id))
        conn.commit()
        
        # Display task_id and priority in the serving_queue_frame
        stats1.configure(text=str(new_status))
        servingq1.configure(text=str(task_id))
        servingp1.configure(text=str(priority))
    else:
        mb.showinfo('Info', 'No pending tasks in the queue for COUNTER 1.')

    cursor.close()
    conn.close()




counter_one_window = None
counter_two_window = None
def open_counter_one():
    global counter_one_window,servingq1,servingp1,stats1
    if counter_one_window and counter_one_window.winfo_exists():
        mb.showinfo("Info", "Counter 1 window is already open.")
        return
    # Close admin login window if exists
    counter_one_window = tk.Toplevel()
    counter_one_window.title('counter1')
    counter_one_window.iconbitmap('img/soco.ico')
    counter_one_window.geometry("925x290+300+100")
    counter_one_window.resizable(False, False)
    counter_one_window.configure(bg="#fff")

    counter_label = tk.Label(counter_one_window, text="COUNTER 1",font=("Arial", 30,'bold'), background='#fff')
    counter_label.place(x=350, y=20)

    serving_queue_frame = ctk.CTkFrame(master=counter_one_window, width=300, height=150, fg_color="#fcb900")
    serving_queue_frame.place(x=100, y=85)

    serving_label = ctk.CTkLabel(serving_queue_frame, text='NOW SERVING', font=("Roboto", 17, 'bold'))
    serving_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    
    servingq1 = ctk.CTkLabel(serving_queue_frame, text='', font=("Roboto", 30, 'bold'))
    servingq1.place(relx=0.5, y=100, anchor=tk.CENTER)

    servingp1 = ctk.CTkLabel(serving_queue_frame, text='', font=("Roboto", 30, 'bold'))
    servingp1.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    stats1 = ctk.CTkLabel(serving_queue_frame, text='', font=("Roboto", 15, 'bold'))
    stats1.place(relx=0.5, y=125, anchor=tk.CENTER)

    servebutton_image = PhotoImage(file="img/nextb.png")
    serve_button = tk.Button(master=counter_one_window,  image=servebutton_image, compound=tk.TOP, cursor='hand2', text="SERVE QUEUE",fg='white',padx=15,pady=10,background='#Ff8c00', font=('Roboto', 13, 'bold'), anchor=tk.W,activebackground='#Ff8c00', command=serve_queue_one)
    serve_button.place(x=550, y=160, anchor=tk.CENTER)

    voiceout_image = PhotoImage(file="img/voice.png")
    voiceout_button = tk.Button(master=counter_one_window, image=voiceout_image, compound=tk.TOP, cursor='hand2', text="CALL OUT",fg='white',padx=15,pady=10,background='#Ff8c00', font=('Roboto', 13, 'bold'), anchor=tk.W,activebackground='#Ff8c00', command=call_out_counter_one)
    voiceout_button.place(x=750, y=160, anchor=tk.CENTER)

    counter_one_window.mainloop()

def open_counter_two():
    global counter_two_window,servingq2,servingp2,stats2
    if counter_two_window and counter_two_window.winfo_exists():
        mb.showinfo("Info", "Counter 2 window is already open.")
        return
    # Close admin login window if exists
    counter_two_window = tk.Toplevel()
    counter_two_window.title('counter2')
    counter_two_window.iconbitmap('img/soco.ico')
    counter_two_window.geometry("925x290+300+425")
    counter_two_window.resizable(False, False)
    counter_two_window.configure(bg="#fff")

    counter_label = tk.Label(counter_two_window, text="COUNTER 2", font=("Arial", 30, 'bold'), background='#fff')
    counter_label.place(x=350, y=20)

    serving_queue_frame = ctk.CTkFrame(master=counter_two_window, width=300, height=150, fg_color="#fcb900")
    serving_queue_frame.place(x=100, y=85)

    serving_label = ctk.CTkLabel(serving_queue_frame, text='NOW SERVING', font=("Roboto", 17, 'bold'))
    serving_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    servingq2 = ctk.CTkLabel(serving_queue_frame, text='', font=("Roboto", 30, 'bold'))
    servingq2.place(relx=0.5, y=100, anchor=tk.CENTER)

    servingp2 = ctk.CTkLabel(serving_queue_frame, text='', font=("Roboto", 30, 'bold'))
    servingp2.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    stats2 = ctk.CTkLabel(serving_queue_frame, text='', font=("Roboto", 15, 'bold'))
    stats2.place(relx=0.5, y=125, anchor=tk.CENTER)

    servebutton_image = PhotoImage(file="img/nextb.png")
    serve_button = tk.Button(master=counter_two_window, image=servebutton_image, compound=tk.TOP, cursor='hand2',
                             text="SERVE QUEUE", fg='white', padx=15, pady=10, background='#Ff8c00',
                             font=('Roboto', 13, 'bold'), anchor=tk.W, activebackground='#Ff8c00', command=serve_queue_two)
    serve_button.place(x=550, y=160, anchor=tk.CENTER)

    voiceout_image = PhotoImage(file="img/voice.png")
    voiceout_button = tk.Button(master=counter_two_window, image=voiceout_image, compound=tk.TOP, cursor='hand2',
                                text="CALL OUT", fg='white', padx=15, pady=10, background='#Ff8c00',
                                font=('Roboto', 13, 'bold'), anchor=tk.W, activebackground='#Ff8c00', command=call_out_counter_two)
    voiceout_button.place(x=750, y=160, anchor=tk.CENTER)

    counter_two_window.mainloop()



def clear_entry_fields():
    staff_user.delete(0, tk.END)
    staff_user.insert(0, 'Enter Username')
    staff_user.config(fg="grey")
    staff_password.delete(0, tk.END)
    staff_password.insert(0, 'Enter Password')
    staff_password.config(show="", fg="grey")
    counter_var.set("")  # Reset counter selection

def stafflog():
    staffuser = staff_user.get()
    staffpassword = staff_password.get()
    counter_choice = counter_var.get()  # Get the selected counter value

    # Check if neither counter is selected
    if not counter_choice:
        mb.showerror('Error', 'Please select a counter!')
        return

    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
    except mysql.connector.Error as err:
        mb.showerror('Database error', f'Error: {err}')
        return

    print('Connection Established')
    print('Enter your Username and password')

    cur = conn.cursor()

    cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (staffuser, staffpassword))

    myresult = cur.fetchone()
    if myresult:
        role = myresult[5]  # Assuming role is stored at index 5 in the database
        if role == 'cashier' or counter_choice == "COUNTER 1":
            mb.showinfo('Login Successfully', f"Welcome, {role.capitalize()}")
            clear_entry_fields()
            open_counter_one()
        elif role == 'cashier' or counter_choice == "COUNTER 2":
            mb.showinfo('Login Successfully', f"Welcome, {role.capitalize()}")
            clear_entry_fields()
            open_counter_two()
        else:
            mb.showinfo('Login Successfully', f"Welcome, {role.capitalize()}")
            # Handle redirection for other roles if needed  # Clear entry fields after successful login
    else:
        mb.showerror('Error', 'Invalid username or password')
        clear_entry_fields()  # Clear entry fields after unsuccessful login

    cur.close()
    conn.close()



def create_staff_login_window():
    global staff_login_window, staff_user, staff_password,counter_var
    
    staff_login_window = tk.Toplevel()
    staff_login_window.title('Staff Login')
    staff_login_window.iconbitmap('img/soco.ico')
    staff_login_window.geometry("925x500+300+200")
    staff_login_window.resizable(False, False)
    staff_login_window.configure(bg='#fff')

    staff_image = PhotoImage(file="img/staff.png")

    # Create a label to display the image
    staff_image_label = tk.Label(staff_login_window, image=staff_image, bg='#fff')
    staff_image_label.place(x=-80, y=45)

    staff_login_frame = tk.Frame(staff_login_window, width=350, height=350, bg="white")
    staff_login_frame.place(x=480, y=70)

    staff_label = tk.Label(master=staff_login_frame, text="STAFF LOGIN", font=('Microsoft YaHei UI Light', 23, 'bold'), fg="black", bg="white")
    staff_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    def clear_username_placeholder(event):
        if staff_user.get() == 'Enter Username':
            staff_user.delete(0, tk.END)
            staff_user.config(fg="black")
        if not staff_password.get():
            staff_password.insert(0, 'Enter Password')
            staff_password.config(show="", fg="grey")

    def clear_password_placeholder(event):
        if staff_password.get() == 'Enter Password':
            staff_password.delete(0, tk.END)
            staff_password.config(show="*", fg="black")
        if not staff_user.get():
            staff_user.insert(0, 'Enter Username')
            staff_user.config(fg="grey")

    staff_user = tk.Entry(master=staff_login_frame, width=25, fg="grey", border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
    staff_user.place(x=30, y=80)
    staff_user.insert(0, 'Enter Username')  # Updated placeholder text
    staff_user.bind("<FocusIn>", clear_username_placeholder)

    tk.Frame(staff_login_frame, width=295, height=2, bg="black").place(x=25, y=107)

    staff_password = tk.Entry(master=staff_login_frame, width=25, fg="grey", border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
    staff_password.place(x=30, y=150)
    staff_password.insert(0, 'Enter Password')  # Updated placeholder text
    staff_password.bind("<FocusIn>", clear_password_placeholder)

    tk.Frame(staff_login_frame, width=295, height=2, bg="black").place(x=25, y=177)
    
    counter_label = tk.Label(staff_login_frame, text="COUNTER:", font=("Roboto", 12), bg="white")
    counter_label.place(x=30, y=200)
    counter_var = tk.StringVar()
    counter_combobox = tk.OptionMenu(staff_login_frame, counter_var, "COUNTER 1", "COUNTER 2")
    counter_combobox.config(font=("Roboto", 12), bg="white")
    counter_combobox.place(x=120, y=195)


    tk.Button(staff_login_frame, width=41, pady=7, text='LOG IN', bg="black", fg='white', cursor="hand2", command=stafflog, border=0).place(x=26, y=234)

    # Function to handle closing the staff login window
    def close_window():
        staff_login_window.destroy()

    # Button to close the staff login window
    exbutton = tk.Button(staff_login_window, text="Exit", width=10, command=close_window, cursor='hand2')
    exbutton.grid(row=1, column=1)

    # Call the mainloop to run the staff login window
    staff_login_window.mainloop()
