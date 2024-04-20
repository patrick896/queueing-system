import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox as mb
from tkinter import PhotoImage
import mysql.connector
import os


last_printed_queue_id = None

def printer():
    global last_printed_queue_id
    
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
        cursor = conn.cursor()

        # Fetch the latest added item from the queue
        cursor.execute("SELECT task_id, task_data, counter, priority FROM queue ORDER BY task_id DESC LIMIT 1")
        latest_item = cursor.fetchone()

        if latest_item:
            task_id, task_data, counter, priority = latest_item
            
            if last_printed_queue_id == task_id:
                mb.showinfo("Already Printed", "The latest queue details have already been printed.")
                return
            
            # Add validation for queue_label and counter
            if not task_data.strip() or not counter.strip():
                mb.showerror("Error", "Queue details cannot be printed because queue_label or counter is empty.")
                return

            # Write the details to the file
            with open("queue_details.txt", "a") as file:
                file.write(f"QUEUE NUMBER: {task_id}\nTRANSACTION: {task_data}\nCOUNTER: {counter}\nPRIORITY: {priority}\n\n")

            # Specify the path to the file to be printed
            file_to_print = "queue_details.txt"

            # Print the file
            os.startfile(file_to_print, "print")

            # Update the variable
            last_printed_queue_id = task_id

            # Optionally, you can show a message box indicating successful printing
            mb.showinfo("Print Success", "Queue details printed.")

        else:
            mb.showinfo("Empty Queue", "The queue is empty.")

    except mysql.connector.Error as e:
        mb.showerror('Database Error', f'Error: {e}')

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def handle_queue(priority=False):
    task_data = optionmenu.get()
    if task_data == "TRANSACTION":
        mb.showerror("error", "No transaction selected")
        return

    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
        cursor = conn.cursor()

        if task_data == "PAY BILL":
            counter = 'COUNTER 1'
            task_data = "Pay Bill"
        elif task_data == "COMPLAIN":
            counter = 'COUNTER 2'
            task_data = "Complain"

        # Set priority if necessary
        priority_value = 'NP'
        if priority:
            priority_value = 'P'

        # Insert task into the database
        cursor.execute("INSERT INTO queue (task_data, counter, status, priority) VALUES (%s, %s, %s, %s)",
                       (task_data, counter, 'pending', priority_value))
        conn.commit()

        # Fetch the task_id
        cursor.execute("SELECT LAST_INSERT_ID()")
        task_id = cursor.fetchone()[0]

        # Fetch the counter
        cursor.execute("SELECT counter FROM queue WHERE task_id = %s", (task_id,))
        counter = cursor.fetchone()[0]
        
        if priority:
            cursor.execute("SELECT priority FROM queue WHERE task_id = %s", (task_id,))
            p = cursor.fetchone()[0]
            p_label.configure(text=str(p))
        else:
            p_label.configure(text='')

        mb.showinfo("Success", f"Your queue is: {task_id}")
        transaction.set("TRANSACTION")

        # Update the number_label with the task_id
        cter_label.configure(text=str(counter))
        number_label.configure(text=str(task_id))

    except mysql.connector.Error as e:
        mb.showerror('Database Error', f'Error: {e}')
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

queue_page = None  # Global variable to track the existence of the queue page window

def queuepage():
    global queue_page, optionmenu, transaction, number_label, cter_label,p_label
    
    if queue_page and queue_page.winfo_exists():
        mb.showerror('Error', 'Queue page window is already open')
        return
    
    queue_page = tk.Toplevel()
    queue_page.title('QUEUE')
    queue_page.iconbitmap('img/soco.ico')
    queue_page.geometry("960x380+310+200")
    queue_page.resizable(False, False)
    queue_page.configure(bg='#fff')

    frame1 = ctk.CTkFrame(master=queue_page, width=300, height=150, fg_color="#fcb900")
    frame1.grid(row=0, column=0, pady=25, padx=10)

    frame2 = ctk.CTkFrame(master=queue_page, width=300, height=150, fg_color="#fcb900")
    frame2.grid(row=0, column=1, pady=25, padx=10)
    
    frame3 = ctk.CTkFrame(master=queue_page, width=300, height=150, fg_color="#fcb900")
    frame3.grid(row=0, column=2, pady=25, padx=10)

    frame4 = ctk.CTkFrame(master=queue_page, width=300, height=150, fg_color="#Ff8c00")
    frame4.grid(row=1, column=0, pady=10, padx=10)

    frame5 = ctk.CTkFrame(master=queue_page, width=300, height=150, fg_color="#Ff8c00")
    frame5.grid(row=1, column=1, pady=10, padx=10)

    frame6 = ctk.CTkFrame(master=queue_page, width=300, height=150, fg_color="#Ff8c00")
    frame6.grid(row=1, column=2, pady=10, padx=10)

    transaction_label = ctk.CTkLabel(frame1, text='TRANSACTION', font=("Roboto", 17, 'bold'))
    transaction_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    queue_label = ctk.CTkLabel(frame2, text='QUEUE', font=("Roboto", 17, 'bold'))
    queue_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    number_label = ctk.CTkLabel(frame2, text='', font=("Roboto", 45, 'bold'))
    number_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    p_label = ctk.CTkLabel(frame2, text='', font=("Roboto", 45, 'bold'))
    p_label.place(relx=0.1, rely=0.5, anchor=tk.CENTER)

    counter_label = ctk.CTkLabel(frame3, text='COUNTER', font=("Roboto", 17, 'bold'))
    counter_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    cter_label = ctk.CTkLabel(frame3, text='', font=("Roboto", 45, 'bold'))
    cter_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    transaction = ctk.StringVar(value="TRANSACTION")
    optionmenu = ctk.CTkOptionMenu(master=frame1, values=["PAY BILL", "COMPLAIN"], variable=transaction,
                                    width=250, height=40, fg_color='white', text_color='black', button_color='white',
                                    dropdown_fg_color='white', dropdown_hover_color='#fcb900', button_hover_color='white')
    optionmenu.place(x=22, y=55)

    getqueue_image = PhotoImage(file="img/power.png")
    getqueue_button = tk.Button(master=frame4, width=120,border=0, height=75, image=getqueue_image, compound=tk.TOP, cursor='hand2', text="GET QUEUE",fg='white',pady=10,background='#Ff8c00', font=('Roboto', 13, 'bold'), anchor=tk.W,activebackground='#Ff8c00',command=lambda: handle_queue())
    getqueue_button.place(x=165, y=75, anchor=tk.CENTER)

    pqueue_image = PhotoImage(file="img/power.png")
    pqueue_button = tk.Button(master=frame5, width=120,border=0, height=75, image=pqueue_image, compound=tk.TOP, cursor='hand2', text="PRIORITY",fg='white',pady=10,background='#Ff8c00', font=('Roboto', 13, 'bold'), anchor=tk.W,activebackground='#Ff8c00',command=lambda: handle_queue(priority=True))
    pqueue_button.place(x=165, y=75, anchor=tk.CENTER)

    printer_image = PhotoImage(file="img/printer.png")
    printer_button = tk.Button(master=frame6, width=120,border=0, height=75, image=printer_image, compound=tk.TOP, cursor='hand2', text="PRINT",fg='white',pady=10,background='#Ff8c00', font=('Roboto', 13, 'bold'), anchor=tk.W,activebackground='#Ff8c00', command=printer)
    printer_button.place(x=180, y=75, anchor=tk.CENTER)

    queue_page.mainloop()