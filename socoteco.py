import customtkinter as ctk
import mysql.connector
from tkinter import messagebox as mb
import tkinter as tk
from tkinter import PhotoImage
from tkinter import *
from tkinter import ttk
import sys
from staffs import create_staff_login_window
from queueing import queuepage
from delete_queue import delete_all_queues
from display import display

admin_logged_in = False  # Flag to track admin login status
add_window = None
staff_tree = None
admin_login_window = None


def adminlog():
    global admin_logged_in, admin_login_window
    
    if admin_logged_in:
        mb.showerror('Error', 'Already logged in as admin')
        return
    
    adminuser = admin_user.get()
    adminpass = admin_password.get()
    
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
    except:
        mb.showerror('Database error', 'You are not connected to server(localhost)')
    else:
        print('Connection Established')
        print('Enter your Username and password')
    
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (adminuser, adminpass))

    myresult = cur.fetchone()
    if myresult:
        if myresult[5] == 'admin':
            mb.showinfo('Login Successfully', "Welcome, Admin")
            admin_logged_in = True
            admin_dashboard()
            admin_login_window.destroy()  # Close admin login window after successful login
        else:
            mb.showerror("Login Failed", "Invalid username or password")
    else:
        mb.showerror('Error', 'Invalid username or password')
        cur.close()
        conn.close()

    

def admin_dashboard():
    global admin_dashboard_window
    global admin_login_window  # Access global variable
    
    if admin_login_window and admin_login_window.winfo_exists():  # Check if the window exists
        admin_login_window.destroy()  # Close admin login window if exists
    
    admin_dashboard_window = tk.Toplevel()
    admin_dashboard_window.geometry("1100x600+220+100")
    admin_dashboard_window.title("SOCOTECO")
    admin_dashboard_window.iconbitmap("img/soco.ico")
    admin_dashboard_window.resizable(False,False)
    admin_dashboard_window.configure(bg="#fff")

    notebook = ttk.Notebook(admin_dashboard_window)
    notebook.place(relx=0.5, y=325, width=1300, height=600, anchor=tk.CENTER)

    dashboard_frame = tk.Frame(notebook, bg="#F3C892")
    staff_frame = tk.Frame(notebook, bg="#F3C892")


    notebook.add(dashboard_frame)
    notebook.add(staff_frame)

    top_frame=ctk.CTkFrame(master=admin_dashboard_window, width=12000, height=60,fg_color="#Ff8c00")
    top_frame.place(x=0,y=0)

    log_out_image = PhotoImage(file="img/logout.png")
    log_out_button = tk.Button(master=top_frame, width=50, height=45,border=0, image=log_out_image, compound=tk.LEFT, cursor='hand2',pady=10, padx=10, background='#Ff8c00',activebackground='#FF8C00',command=close_admin_dashboard)
    log_out_button.place( x=1030,y=30, anchor=tk.W)

    admin_dashboard_frame = ctk.CTkFrame(master=admin_dashboard_window, width=300, height=700, fg_color="#fcb900",corner_radius=0)
    admin_dashboard_frame.place(x=0, y=0)


    def add():
        global add_window  # Access the global variable
        if not add_window or not add_window.winfo_exists():
            add_window = tk.Toplevel()
            add_window.title("SOCOTECO II")
            add_window.geometry("450x500+600+200")
            add_window.iconbitmap("img/soco.ico")
            add_window.resizable(False,False)
            add_window.configure(bg="#fff")

            def clear_placeholder(event, entry, placeholder):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg="black")

            def restore_placeholder(event, entry, placeholder):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg="grey")
            def clear_password_placeholder(event):
                if pword.get() == 'Enter Password':
                    pword.delete(0, tk.END)
                    pword.config(show="*")
                    pword.config(fg="black")

            def restore_password_placeholder(event):
                if not pword.get():
                    pword.config(show="")
                    pword.insert(0, 'Enter Password')
                    pword.config(fg="grey")

            tk.Button(add_window, width=5, pady=7, text='BACK', fg='black', command=close_add, cursor="hand2",).place(x=405, y=0)

            label = tk.Label(master=add_window, text="ADD ADMIN/STAFF",font=('Microsoft YaHei UI Light', 23, 'bold'),bg="#fff")
            label.place(x=80, y=20)

            fulln_placeholder = 'Enter Fullname'
            fulln = tk.Entry(master=add_window, width=25, fg="grey", border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
            fulln.insert(0, fulln_placeholder)
            fulln.bind("<FocusIn>", lambda event: clear_placeholder(event, fulln, fulln_placeholder))
            fulln.bind("<FocusOut>", lambda event: restore_placeholder(event, fulln, fulln_placeholder))
            fulln.place(x=115, y=110)
            tk.Frame(add_window, width=205, height=2, bg="black").place(x=115, y=137)

            uname_placeholder = 'Enter Username'
            uname = tk.Entry(master=add_window, width=25, fg="grey", border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
            uname.insert(0, uname_placeholder)
            uname.bind("<FocusIn>", lambda event: clear_placeholder(event, uname, uname_placeholder))
            uname.bind("<FocusOut>", lambda event: restore_placeholder(event, uname, uname_placeholder))
            uname.place(x=115, y=180)
            tk.Frame(add_window, width=205, height=2, bg="black").place(x=115, y=207)

            pword_placeholder = 'Enter Password'
            pword = tk.Entry(master=add_window, width=25, fg="grey", border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
            pword.insert(0, pword_placeholder)
            pword.bind("<FocusIn>", clear_password_placeholder)
            pword.bind("<FocusOut>", restore_password_placeholder)
            pword.place(x=115, y=250)
            tk.Frame(add_window, width=205, height=2, bg="black").place(x=115, y=277)

            contact_placeholder = 'Enter Contact'
            contact = tk.Entry(master=add_window, width=25, fg="grey", border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
            contact.insert(0, contact_placeholder)
            contact.bind("<FocusIn>", lambda event: clear_placeholder(event, contact, contact_placeholder))
            contact.bind("<FocusOut>", lambda event: restore_placeholder(event, contact, contact_placeholder))
            contact.place(x=115, y=320)
            tk.Frame(add_window, width=205, height=2, bg="black").place(x=115, y=347)
            
            role_label = tk.Label(master=add_window, text="Role:", bg='#fff', font=('Microsoft YaHei UI Light', 11))
            role_label.place(x=115, y=380)
            role_var = tk.StringVar(add_window)
            role_var.set("SELECT ROLE")  # Default role selection
            roles = ["ADMIN", "CASHIER","STAFF"]
            role_dropdown = tk.OptionMenu(add_window, role_var, *roles)
            role_dropdown.config(width=10, font=('Microsoft YaHei UI Light', 11))
            role_dropdown.place(x=155, y=375)

        def update_staff_treeview():
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            except mysql.connector.Error as err:
                print("Failed to connect to MySQL database:", err)
                return

            cur = conn.cursor()
            cur.execute("SELECT user_id, fullname, contact, role FROM users")
            data = cur.fetchall()

            staff_tree.delete(*staff_tree.get_children())

            if data:
                for index, row in enumerate(data):
                    if index % 2 == 0:
                        staff_tree.insert("", "end", values=row, tags=('even',))
                    else:
                        staff_tree.insert("", "end", values=row, tags=('odd',))
            else:
                mb.showinfo("All Data", "No data found")

            cur.close()
            conn.close()

        def adding():
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password="", database='queue_db')
            except mysql.connector.Error as err:
                mb.showerror('Database error', f'Error: {err}')
                return
            cur = conn.cursor()

            fuln = fulln.get()
            un = uname.get()
            pw = pword.get()
            con = contact.get()
            role = role_var.get()

            if fuln == "Enter Fullname":
                mb.showerror("Error", "Please Enter Fullname")
                return
            elif not fuln.isalpha():
                mb.showerror("Error", "Fullname should contain letters only")
            elif un == "Enter Username":
                mb.showerror("Error", "Please Enter Username")
                return
            elif pw == "Enter Password":
                mb.showerror("Error", "Please Enter Password")
                return
            elif con == "Enter Contact":
                mb.showerror("Error", "Please Enter Contact")
                return
            elif not con.isdigit():
                mb.showerror("Error", "Contact must be a number")
            elif len(con) != 11:
                mb.showerror("Error", "Contact should contain 11 digits only")
                return
            elif role == "SELECT ROLE":
                mb.showerror("Error", "Please Select Role")
                return
            else:
                cur.execute("SELECT * FROM users WHERE fullname =%s OR username = %s", (fuln,un))
                existing_acc = cur.fetchall()
                if existing_acc:
                    mb.showerror("Error", "User already exists")
                else:
                    try:
                        cur.execute("INSERT INTO users (fullname, username, password, contact, role) VALUES (%s, %s, %s, %s, %s)", (fuln, un, pw, con, role))
                        conn.commit()
                        mb.showinfo('Sign Up Successful', 'You have signed up successfully!')
                        update_staff_treeview()
                        close_add()  
                    except mysql.connector.Error as err:
                        mb.showerror('Sign Up Failed', f'Error: {err}')
                    finally:
                        cur.close()
                        conn.close()

        
        tk.Button(add_window, width=29, pady=7, text='ADD', bg="black", fg='white', command=adding, cursor="hand2", border=0).place(x=115, y=440)

        add_window.mainloop()

    add_image = PhotoImage(file="img/add-user.png")
    add_button = tk.Button(master=staff_frame, width=50, height=45, image=add_image, compound=tk.LEFT, cursor='hand2',pady=10, padx=10, background='#fff',activebackground='#fff',command=add)
    add_button.place( x=970,y=45, anchor=tk.W)

    def update_staff_treeview():
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            except mysql.connector.Error as err:
                print("Failed to connect to MySQL database:", err)
                return

            cur = conn.cursor()
            cur.execute("SELECT user_id, fullname, contact, role,date FROM users")
            data = cur.fetchall()

            staff_tree.delete(*staff_tree.get_children())

            if data:
                for index, row in enumerate(data):
                    if index % 2 == 0:
                        staff_tree.insert("", "end", values=row, tags=('even',))
                    else:
                        staff_tree.insert("", "end", values=row, tags=('odd',))
            else:
                mb.showinfo("All Data", "No data found")

            cur.close()
            conn.close()

    def delete():
    # Get the selected item from the Treeview
        selected_item = staff_tree.focus()
        if not selected_item:
            mb.showerror("Error", "Please select a row to delete")
            return
        
        # Get the values of the selected item
        values = staff_tree.item(selected_item, 'values')
        
        try:
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
        except mysql.connector.Error as err:
            mb.showerror('Database error', f'Error: {err}')
            return
        
        cur = conn.cursor()

        # Extract the user_id from the selected item
        user_id = values[0]

        # Delete the row from the database
        try:
            cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            conn.commit()
            mb.showinfo('Success', 'Row deleted successfully!')
            update_staff_treeview()
        except mysql.connector.Error as err:
            mb.showerror('Delete Failed', f'Error: {err}')
        finally:
            cur.close()
            conn.close()

    delete_image = PhotoImage(file="img/user.png")
    delete_button = tk.Button(master=staff_frame, width=50, height=45, image=delete_image, compound=tk.LEFT, cursor='hand2',pady=10, padx=10, background='#fff',activebackground='#fff',command=delete)
    delete_button.place( x=1090,y=45, anchor=tk.W)

    trash_image = PhotoImage(file="img/trash.png")
    trash_image_button = tk.Button(master=dashboard_frame,border=0,width=50, height=45, image=trash_image, compound=tk.LEFT, cursor='hand2',pady=10, padx=10, background='#F3C892',activebackground='#F3C892',command=delete_all_queues)
    trash_image_button.place( x=400,y=38, anchor=tk.W)

    
    current_queue_frame = ctk.CTkFrame(master=dashboard_frame, width=240, height=150, fg_color="#fff")
    current_queue_frame.place(x=420, y=70)

    queuelabel = ctk.CTkLabel(current_queue_frame, text='PROCESSING', font=("arial", 17, 'bold'))
    queuelabel.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    def update_process():
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            cursor = conn.cursor()

            # Execute a query to fetch one task ID from the queue table where status is 'PROCESSING'
            cursor.execute("SELECT task_id FROM queue WHERE status = 'PROCESSING' LIMIT 1")
            
            # Fetch the task ID
            task_id = cursor.fetchone()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Update the text of the label with the fetched task ID (if any)
            if task_id:
                process.configure(text=str(task_id[0]))
            else:
                process.configure(text="--")

            # Schedule the next update after 1 second (adjust as needed)
            process.after(1000, update_process)

        except mysql.connector.Error as err:
            print(f"Failed to connect to MySQL database: {err}")

    process = ctk.CTkLabel(current_queue_frame, text='', font=("arial", 35, 'bold'))
    process.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    update_process()


    transaction_frame = ctk.CTkFrame(master=dashboard_frame, width=240, height=150, fg_color="#fff")
    transaction_frame.place(x=940, y=70)

    def update_transaction():
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            cursor = conn.cursor()

            # Execute a query to fetch one task ID from the queue table where status is 'PROCESSING'
            cursor.execute("SELECT task_data FROM queue WHERE status = 'PROCESSING' LIMIT 1")
            
            # Fetch the task ID
            task_data = cursor.fetchone()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Update the text of the label with the fetched task ID (if any)
            if task_data:
                trans.configure(text=str(task_data[0]))
            else:
                trans.configure(text="--")

            # Schedule the next update after 1 second (adjust as needed)
            trans.after(1000, update_transaction)

        except mysql.connector.Error as err:
            print(f"Failed to connect to MySQL database: {err}")
    translabel = ctk.CTkLabel(transaction_frame, text='TRANSACTION', font=("arial", 17, 'bold'))
    translabel.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    trans = ctk.CTkLabel(transaction_frame, text='', font=("arial", 35, 'bold'))
    trans.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    update_transaction()

    counter_frame = ctk.CTkFrame(master=dashboard_frame, width=240, height=150, fg_color="#fff")
    counter_frame.place(x=680, y=70)

    def update_counter():
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            cursor = conn.cursor()

            # Execute a query to fetch one task ID from the queue table where status is 'PROCESSING'
            cursor.execute("SELECT counter FROM queue WHERE status = 'PROCESSING' LIMIT 1")
            
            # Fetch the task ID
            counterrs = cursor.fetchone()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Update the text of the label with the fetched task ID (if any)
            if counterrs:
                counters.configure(text=str(counterrs[0]))
            else:
                counters.configure(text="--")

            # Schedule the next update after 1 second (adjust as needed)
            counters.after(1000, update_counter)

        except mysql.connector.Error as err:
            print(f"Failed to connect to MySQL database: {err}")

    counterlabel = ctk.CTkLabel(counter_frame, text='COUNTER', font=("arial", 17, 'bold'))
    counterlabel.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    counters = ctk.CTkLabel(counter_frame, text='', font=("arial", 35, 'bold'))
    counters.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    update_counter()


    waiting_frame = ctk.CTkFrame(master=dashboard_frame, width=370, height=100, fg_color="#fff")
    waiting_frame.place(x=420, y=250)

    ssstyle = ttk.Style()
    custom_font = ('Roboto', 12)
    headfont = ('Roboto', 18)

    # Configure the Treeview style (background, border, etc.)
    ssstyle.configure('NoBorder.Treeview', borderwidth=0, relief='flat', background="#FBF3D5", font=custom_font)

    # Configure the Treeview heading style to use the custom font for headings
    ssstyle.configure('Treeview.Heading', font=headfont)

    # Also, set padding and other properties to remove any space around the Treeview
    ssstyle.layout('NoBorder.Treeview', [('Treeview.treearea', {'sticky': 'nswe'})])

    # Apply the custom style to the waiting_qtree_view widget
    waiting_qtree_view = ttk.Treeview(dashboard_frame, columns=("task_id", "status"), show="headings", height=8, style='NoBorder.Treeview')


    # Configure the columns
    waiting_qtree_view.heading("task_id", text="QUEUE")
    waiting_qtree_view.heading("status", text="STATUS")

    # Set column widths
    waiting_qtree_view.column("task_id", width=185, anchor='center')
    waiting_qtree_view.column("status", width=185, anchor='center')

    # Place the waiting_qtree_view widget in the frame
    waiting_qtree_view.place(x=420, y=342)

    def update_waiting_qtree_view():
        # Define the waiting_qtree_view function
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            cursor = conn.cursor()

            # Query to fetch task_id and status from the queue table where status is 'PENDING'
            query = "SELECT task_id, status FROM queue WHERE status = 'PENDING'"
            cursor.execute(query)

            # Fetch all results
            results = cursor.fetchall()


            # Clear existing data from the waiting_qtree_view
            for item in waiting_qtree_view.get_children():
                waiting_qtree_view.delete(item)

            # Check if there are results
            if results:
                # Insert results into the Treeview
                for task_id, status in results:
                    # Prepend a bullet point to each task_id
                    bullet_task_id = f"• {task_id}"
                    # Insert each task_id (with bullet) and status into the Treeview
                    waiting_qtree_view.insert('', 'end', values=(bullet_task_id, status))
            else:
                # If there are no pending tasks, insert a row with "None" for each column
                waiting_qtree_view.insert('', 'end', values=("--", "--"))

            # Close the cursor and connection
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Failed to connect to MySQL database: {err}")

        # Schedule the next update after 1 second (1000 ms)
        waiting_qtree_view.after(1000, update_waiting_qtree_view)

    # Call the function initially to start populating the waiting_qtree_view
    update_waiting_qtree_view()

    waitinglabel = ctk.CTkLabel(waiting_frame, text='WAITING', font=("arial", 17, 'bold'))
    waitinglabel.place(relx=0.5, rely=0.2, anchor=tk.CENTER)


    def update_total_label():
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            cursor = conn.cursor()

            # Execute a query to fetch all task IDs from the queue table
            cursor.execute("SELECT task_id FROM queue WHERE status = 'PENDING'")
            
            # Fetch all task IDs
            task_ids = cursor.fetchall()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Get the total count of task IDs
            total_count = len(task_ids)

            # Update the text of the label with the new total count
            total_label.configure(text=f'{total_count}')

            # Schedule the next update after 1 second (adjust as needed)
            total_label.after(1000, update_total_label)

        except mysql.connector.Error as err:
            print(f"Failed to connect to MySQL database: {err}")

    tk.Frame(waiting_frame, width=595, height=2, bg="black").place(rely=0.9)
    
    total_label = ctk.CTkLabel(waiting_frame, text='', font=("arial", 35, 'bold'))
    total_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    update_total_label()

    completed_frame = ctk.CTkFrame(master=dashboard_frame, width=370, height=100, fg_color="#fff")
    completed_frame.place(x=810, y=250)

    # Create a custom style for the Treeview
    ssstyle = ttk.Style()
    custom_font = ('Roboto', 12)
    headfont = ('Roboto', 18)

    # Configure the Treeview style (background, border, etc.)
    ssstyle.configure('NoBorder.Treeview', borderwidth=0, relief='flat', background="#FBF3D5", font=custom_font)
    ssstyle.configure('Treeview.Heading', font=headfont)
    ssstyle.layout('NoBorder.Treeview', [('Treeview.treearea', {'sticky': 'nswe'})])

    # Initialize completed_tree_view as a ttk.Treeview widget
    completed_tree_view = ttk.Treeview(dashboard_frame, columns=("task_id", "status"), show="headings", height=8, style='NoBorder.Treeview')

    # Configure the columns
    completed_tree_view.heading("task_id", text="QUEUE")
    completed_tree_view.heading("status", text="STATUS")
    completed_tree_view.column("task_id", width=185, anchor='center')
    completed_tree_view.column("status", width=185, anchor='center')

    # Place the completed_tree_view widget in the frame
    completed_tree_view.place(x=810, y=342)

    # Define the function update_completed_tree_view instead of using waiting_qtree_view
    def update_completed_tree_view():
        # Define the function to update the completed_tree_view
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            cursor = conn.cursor()

            # Query to fetch task_id and status from the queue table where status is 'PENDING'
            query = "SELECT task_id, status FROM queue WHERE status = 'COMPLETED'"
            cursor.execute(query)

            # Fetch all results
            results = cursor.fetchall()

            # Clear existing data from the completed_tree_view
            for item in completed_tree_view.get_children():
                completed_tree_view.delete(item)

            # Check if there are results
            if results:
                # Insert results into the Treeview
                for task_id, status in results:
                    # Prepend a bullet point to each task_id
                    bullet_task_id = f"• {task_id}"
                    # Insert each task_id (with bullet) and status into the Treeview
                    completed_tree_view.insert('', 'end', values=(bullet_task_id, status))

            else:
                # If there are no pending tasks, insert a row with "None" for each column
                completed_tree_view.insert('', 'end', values=("--", "--"))

            # Close the cursor and connection
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Failed to connect to MySQL database: {err}")

        # Schedule the next update after 1 second (1000 ms)
        completed_tree_view.after(1000, update_completed_tree_view)

    # Call the function initially to start populating the completed_tree_view
    update_completed_tree_view()

    tk.Frame(completed_frame, width=595, height=2, bg="black").place(rely=0.9)

    def uupdate_total_label():
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            cursor = conn.cursor()

            # Execute a query to fetch all task IDs from the queue table
            cursor.execute("SELECT task_id FROM queue WHERE status = 'COMPLETED'")
            
            # Fetch all task IDs
            task_idss = cursor.fetchall()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Get the total count of task IDs
            total_counts = len(task_idss)

            # Update the text of the label with the new total count
            totalcom_label.configure(text=f'{total_counts}')

            # Schedule the next update after 1 second (adjust as needed)
            totalcom_label.after(1000, uupdate_total_label)

        except mysql.connector.Error as err:
            print(f"Failed to connect to MySQL database: {err}")

    totalcom_label = ctk.CTkLabel(completed_frame, text='', font=("arial", 35, 'bold'))
    totalcom_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    uupdate_total_label()

    completedlabel = ctk.CTkLabel(completed_frame, text='COMPLETED', font=("arial", 17, 'bold'))
    completedlabel.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
    except:
        print("Failed to connect to MySQL database")
        sys.exit()

    cur = conn.cursor()
    cur.execute("SELECT user_id, fullname,contact, role, date FROM users")
    data = cur.fetchall()

    if data:

        style = ttk.Style()
        style.configure("Custom.Treeview", borderwidth=0, bordercolor="black", background="#F3C892", relief="flat", fieldbackground="cyan")
        style.layout("Custom.Treeview", [('Custom.Treeview.treearea', {'sticky': 'nswe'})])  # No border for the tree area
        staff_tree = ttk.Treeview(staff_frame,style="Custom.Treeview",columns=("user_id", "fullname","contact", "role",'date'), show="headings", height=18)
        staff_tree.place(x=410, y=100)

        staff_tree.column("user_id", width=155,anchor="center")
        staff_tree.column("fullname", width=155,anchor="center")
        staff_tree.column("contact", width=155,anchor="center")
        staff_tree.column("role", width=155,anchor="center")
        staff_tree.column("date", width=155,anchor="center")

        staff_tree.heading("user_id", text="ID")
        staff_tree.heading("fullname", text="FULLNAME")
        staff_tree.heading("contact", text="CONTACT")
        staff_tree.heading("role", text="ROLE ")
        staff_tree.heading("date", text="DATE ADDED ")

        # Define tag configurations for even and odd rows
        staff_tree.tag_configure('even', background='#Ff8c00')
        staff_tree.tag_configure('odd', background='#fff')

        for index, row in enumerate(data):
            # Apply tags to alternate rows based on index
            if index % 2 == 0:
                staff_tree.insert("", "end", values=row, tags=('even',))
            else:
                 staff_tree.insert("", "end", values=row, tags=('odd',))

        vsb = ttk.Scrollbar(staff_frame, orient="vertical", command=staff_tree.yview)
        vsb.pack(side="right", fill="y")
        staff_tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(staff_frame, orient="horizontal", command=staff_tree.xview)
        hsb.pack(side="bottom", fill="x")
        staff_tree.configure(xscrollcommand=hsb.set)

    else:
        mb.showinfo("All Data", "No data found")

    cur.close()
    conn.close()


    admin_user = PhotoImage(file="img/man.png")
    admin_user_label = tk.Label(admin_dashboard_frame, image=admin_user, bg='#fcb900')
    admin_user_label.place(x=148, y=90, anchor=tk.CENTER)

    tk.Frame(admin_dashboard_frame, width=350, height=2, bg="white").place(x=0, y=180)

    dashboard_image = PhotoImage(file="img/dashboard.png")
    dashboard_button = tk.Button(master=admin_dashboard_frame, width=280, height=45, image=dashboard_image, compound=tk.LEFT, cursor='hand2', text="DASHBOARD", pady=10, padx=10, background='#Ff8c00', font=('Microsoft YaHei UI Light', 13, 'bold'), anchor=tk.W,command=lambda: notebook.select(0))
    dashboard_button.place(x=0, y=230, anchor=tk.W)

    add_user_image = PhotoImage(file="img/adduser.png")
    add_user_button = tk.Button(master=admin_dashboard_frame, width=280, height=45, image=add_user_image, compound=tk.LEFT, cursor='hand2', text="STAFF MANAGEMENT", pady=10, padx=10, background='#Ff8c00', font=('Microsoft YaHei UI Light', 13, 'bold'), anchor=tk.W, command=lambda: notebook.select(1))
    add_user_button.place( y=310, anchor=tk.W)
    
    
    admin_dashboard_window.mainloop()

# Admin login window
admin_login_window = None

def admin_login():
    global admin_login_window, admin_user, admin_password
    if admin_login_window and admin_login_window.winfo_exists():
        mb.showerror('Error', 'Admin login window is already open')
        return
    admin_login_window = tk.Toplevel(front_window)
    admin_login_window.title('Admin Login')
    admin_login_window.iconbitmap('img/soco.ico')
    admin_login_window.geometry("925x500+300+200")
    admin_login_window.resizable(False, False)
    admin_login_window.configure(bg='#fff')

    admin_image = PhotoImage(file="img/adminbg.png")

    # Create a label to display the image
    admin_image_label = tk.Label(admin_login_window, image=admin_image, bg='#fff').place(x=10, y=10)

    admin_login_frame = tk.Frame(admin_login_window, width=350, height=350, bg="white")
    admin_login_frame.place(x=480, y=70)

    admin_label = tk.Label(master=admin_login_frame, text="ADMIN LOGIN", font=('Microsoft YaHei UI Light', 23, 'bold'), fg="black", bg="white")
    admin_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    def clear_username_placeholder(event):
        if admin_user.get() == 'Enter Username':
            admin_user.delete(0, tk.END)
            admin_user.config(fg="black")
        if not admin_password.get():
            admin_password.insert(0, 'Enter Password')
            admin_password.config(show="", fg="grey")

    def clear_password_placeholder(event):
        if admin_password.get() == 'Enter Password':
            admin_password.delete(0, tk.END)
            admin_password.config(show="*", fg="black")
        if not admin_user.get():
            admin_user.insert(0, 'Enter Username')
            admin_user.config(fg="grey")

    admin_user = tk.Entry(master=admin_login_frame, width=25, fg="grey", border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
    admin_user.place(x=30, y=80)
    admin_user.insert(0, 'Enter Username')  # Updated placeholder text
    admin_user.bind("<FocusIn>", clear_username_placeholder)

    tk.Frame(admin_login_frame, width=295, height=2, bg="black").place(x=25, y=107)

    admin_password = tk.Entry(master=admin_login_frame, width=25, fg="grey", border=0, bg="#fff", font=('Microsoft YaHei UI Light', 11))
    admin_password.place(x=30, y=150)
    admin_password.insert(0, 'Enter Password')  # Updated placeholder text
    admin_password.bind("<FocusIn>", clear_password_placeholder)

    tk.Frame(admin_login_frame, width=295, height=2, bg="black").place(x=25, y=177)

    tk.Button(admin_login_frame, width=41, pady=7, text='LOG IN', bg="black", fg='white', command=adminlog, cursor="hand2", border=0).place(x=26, y=234)

    exbutton = tk.Button(admin_login_window, text="Exit", width=10, command=close_window, cursor='hand2')
    exbutton.grid(row=1, column=1)

    admin_login_window.mainloop()


def close_window():
    admin_login_window.destroy()

def close_add():
    add_window.destroy()

def close_admin_dashboard():
    global admin_logged_in
    if mb.askyesno("Confirmation", "Are you sure you want to log out?"):
        admin_logged_in = False
        admin_dashboard_window.destroy()


def frontpage():
    global front_window
    front_window = tk.Tk()
    front_window.title('SOCOTECO II')
    front_window.iconbitmap('img/soco.ico')
    front_window.geometry("782x765+400+25")
    front_window.resizable(False, False)
    front_window.configure(bg='#fcb900')

    # Load the image
    image = PhotoImage(file="img/soco.png")

    # Create a label to display the image
    image_label = tk.Label(front_window, image=image, background='#fcb900')
    image_label.grid(row=0, column=0, columnspan=4)

    frame1 = ctk.CTkFrame(master=front_window, width=350, height=300, corner_radius=30, cursor="hand2", fg_color="white")
    frame1.grid(row=1, column=1, padx=20, pady=20)
    frame1.bind("<Button-1>", lambda event: create_staff_login_window())

    frame2 = ctk.CTkFrame(master=front_window, width=350, height=300, corner_radius=30, cursor="hand2", fg_color="white")
    frame2.bind("<Button-1>", lambda event: admin_login())
    frame2.grid(row=1, column=0, padx=20, pady=20)

    frame3 = ctk.CTkFrame(master=front_window, width=350, height=300, corner_radius=30, cursor="hand2", fg_color="white")
    frame3.grid(row=2, column=0, padx=20, pady=20)
    frame3.bind("<Button-1>", lambda event: queuepage())

    frame4 = ctk.CTkFrame(master=front_window, width=350, height=300, corner_radius=30, cursor="hand2", fg_color="white")
    frame4.grid(row=2, column=1, padx=20, pady=20)
    frame4.bind("<Button-1>", lambda event: display())

    admin_image = PhotoImage(file="img/settings.png")
    admin_image_label = tk.Label(frame2, image=admin_image, background="white")
    admin_image_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    admin_label = ctk.CTkLabel(frame2, text='ADMIN', font=("Arial", 35,'bold'))
    admin_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    counter_image = PhotoImage(file="img/counter.png")
    counter_image_label = tk.Label(frame1, image=counter_image, background="white")
    counter_image_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    counter_label = ctk.CTkLabel(frame1, text='COUNTER', font=("Arial", 35,'bold'))
    counter_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    monitor_image = PhotoImage(file="img/monitor.png")
    monitor_image_label = tk.Label(frame4, image=monitor_image, background="white")
    monitor_image_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    monitor_label = ctk.CTkLabel(frame4, text='DISPLAY', font=("Arial", 35,'bold'))
    monitor_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    queue_image = PhotoImage(file="img/queue.png")
    queue_image_label = tk.Label(frame3, image=queue_image, background="white")
    queue_image_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    queue_label = ctk.CTkLabel(frame3, text='QUEUE', font=("Arial", 35,'bold'))
    queue_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    # Add any other widgets or frames you need

    front_window.mainloop()

frontpage()