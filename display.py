import tkinter as tk
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox as mb
import mysql.connector
import sys


display_window = False

def display():

    global display_window
    
    if display_window and display_window.winfo_exists():
        mb.showerror('Error', 'Display window is already open')
        return

    # Create a new window
    display_window = tk.Toplevel()
    display_window.title("SOCOTECO II")
    display_window.geometry("925x550+300+180")
    display_window.iconbitmap("img/soco.ico")
    display_window.resizable(False, False)
    display_window.configure(bg="#EFBC9B")

    # Create labels for the counter headers
    tk.Label(display_window, text="COUNTER 1", font=("Arial", 30, 'bold'), background='#EFBC9B').grid(row=0, column=0, padx=55, pady=10)
    tk.Label(display_window, text="COUNTER 2", font=("Arial", 30, 'bold'), background='#EFBC9B').grid(row=0, column=1, padx=55, pady=10)

    # Create frames for the counters
    frame1_display = ctk.CTkFrame(master=display_window, width=350, height=420, corner_radius=30, cursor="hand2", fg_color="#FBF3D5")
    frame1_display.grid(row=1, column=0, padx=55, pady=10)

    frame2_display = ctk.CTkFrame(master=display_window, width=350, height=420, corner_radius=30, cursor="hand2", fg_color="#FBF3D5")
    frame2_display.grid(row=1, column=1, padx=55, pady=10)

    # Create a label for the date and time
    timedate_label = ctk.CTkLabel(master=frame1_display, text="", font=("Arial", 20))
    timedate_label.place(x=75, rely=.9)

    timedate2_label = ctk.CTkLabel(master=frame2_display, text="", font=("Arial", 20))
    timedate2_label.place(x=75, rely=.9)

    pay_label = ctk.CTkLabel(master=frame1_display, text="PAY BILLS", font=("Arial", 20, 'bold'))
    pay_label.place(relx=0.5, y=25, anchor='center')

    complain_label = ctk.CTkLabel(master=frame2_display, text="COMPLAIN", font=("Arial", 20, 'bold'))
    complain_label.place(relx=0.5, y=25, anchor='center')

    nowservingframe1 = ctk.CTkFrame(master=frame1_display, width=250, height=200, corner_radius=10, cursor="hand2", fg_color="#D6DAC8")
    nowservingframe1.place(x=50, y=50)

    ctk.CTkLabel(master=nowservingframe1, text='NOW SERVING',font=("Arial", 12)).place(relx=0.5, rely=0.1, anchor='center')

   # Set the recursion limit before calling the recursive function
    sys.setrecursionlimit(2000)  # Adjust the limit as needed

    def update_serving1():
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            cursor = conn.cursor()

            # Execute a query to fetch one task ID and priority from the queue table where status is 'PROCESSING' and counter is 'COUNTER 1'
            query = "SELECT task_id, priority FROM queue WHERE status = 'PROCESSING' AND counter = 'COUNTER 1' LIMIT 1"
            cursor.execute(query)

            # Fetch the result (task ID and priority)
            result = cursor.fetchone()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Check if a result was returned
            if result:
                task_id, priority = result  # Unpack the result into task_id and priority

                # Update the servingqueue1 label with the fetched task ID
                servingqueue1.configure(text=str(task_id))

                # Update the servingp1 label based on the priority
                if priority == 'P':
                    servingp1.configure(text=f"{priority}")
                else:
                    servingp1.configure(text="")

            else:
                # If no task is being processed, set default text in servingqueue1 and clear servingp1
                servingqueue1.configure(text="--")
                servingp1.configure(text="")

            # Schedule the next update after 1 second (1000 ms)
            servingqueue1.after(1000, update_serving1)

        except mysql.connector.Error as err:
            print(f"Failed to connect to MySQL database: {err}")

    # Create the label for showing the priority and queue
    servingp1 = ctk.CTkLabel(master=nowservingframe1, text='', font=("Arial", 30))
    servingp1.place(relx=0.5, rely=0.3, anchor='center')

    # Create the label for showing the serving queue
    servingqueue1 = ctk.CTkLabel(master=nowservingframe1, text='', font=("Arial", 55))
    servingqueue1.place(relx=0.5, rely=0.5, anchor='center')

    # Call the function initially to start updating the serving queue and priority
    update_serving1()


   # Create a ttk.Style object
    style = ttk.Style()
    custom_font = ('ROBOTO', 12, )
    headfont = ('ROBOTO', 18, )
    # Create a custom style for the Treeview
    style.configure('NoBorder.Treeview', borderwidth=0, relief='flat', background="#FBF3D5",font=custom_font)

    # Also, set padding and other properties to remove any space around the Treeview
    style.layout('NoBorder.Treeview', [('Treeview.treearea', {'sticky': 'nswe'})])
    style.configure('Treeview.Heading', font=headfont)
    # Apply the custom style to the serving1_pending_view widget
    serving1_pending_view = ttk.Treeview(frame1_display, columns=("task_id", "priority"), show="headings", height=5, style='NoBorder.Treeview')

    # Configure the columns
    serving1_pending_view.heading("task_id", text="QUEUE")
    serving1_pending_view.heading("priority", text="STATUS")

    # Set column widths
    serving1_pending_view.column("task_id", width=160,anchor='center')
    serving1_pending_view.column("priority", width=160,anchor='center')

    # Place the serving1_pending_view widget in the frame
    serving1_pending_view.place(x=15, rely=0.6)

    # Step 4: Function to fetch data from the database and populate the serving1_pending_view
    def fetch_and_populate_serving1_pending_view():
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            cursor = conn.cursor()

            # Execute a query to fetch task_id and priority from the queue table where status is 'PENDING' and counter is 'COUNTER 1'
            query = "SELECT task_id, priority FROM queue WHERE status = 'PENDING' AND counter = 'COUNTER 1'"
            cursor.execute(query)

            # Fetch all results
            results = cursor.fetchall()

            # Clear existing data from the serving1_pending_view
            for item in serving1_pending_view.get_children():
                serving1_pending_view.delete(item)

            # Check if there are results
            if results:
                # Separate results into two lists based on priority
                priority_p = []
                priority_np = []

                for task_id, priority in results:
                    if priority == "P":
                        priority_p.append((task_id, priority))
                    else:
                        priority_np.append((task_id, priority))

                # First, insert tasks with priority "P" into the Treeview
                for task_id, priority in priority_p:
                    # Prepend a bullet character to the task_id
                    bullet_task_id = f"• {task_id}"
                    serving1_pending_view.insert('', 'end', values=(bullet_task_id, priority))

                # Then, insert tasks with priority "NP" into the Treeview
                for task_id, priority in priority_np:
                    # Prepend a bullet character to the task_id
                    bullet_task_id = f"• {task_id}"
                    serving1_pending_view.insert('', 'end', values=(bullet_task_id, priority))

            else:
                # If there are no pending tasks, insert a row with "None" for each column
                serving1_pending_view.insert('', 'end', values=("--", "--"))

            # Close the cursor and connection
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Failed to connect to MySQL database: {err}")


        # Schedule the next update after 1 second (1000 ms)
        serving1_pending_view.after(1000, fetch_and_populate_serving1_pending_view)

    # Call the function initially to start populating the serving1_pending_view
    fetch_and_populate_serving1_pending_view()


    nowservingframe2 = ctk.CTkFrame(master=frame2_display, width=250, height=200, corner_radius=10, cursor="hand2", fg_color="#D6DAC8")
    nowservingframe2.place(x=50, y=50)

    ctk.CTkLabel(master=nowservingframe2, text='NOW SERVING',font=("Arial", 12)).place(relx=0.5, rely=0.1, anchor='center')

    def update_serving2():
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            cursor = conn.cursor()

            # Execute a query to fetch one task ID and priority from the queue table where status is 'PROCESSING' and counter is 'COUNTER 2'
            query = "SELECT task_id, priority FROM queue WHERE status = 'PROCESSING' AND counter = 'COUNTER 2' LIMIT 1"
            cursor.execute(query)

            # Fetch the result (task ID and priority)
            result = cursor.fetchone()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Check if a result was returned
            if result:
                task_id, priority = result  # Unpack the result into task_id and priority

                # Update the servingqueue2 label with the fetched task ID
                servingqueue2.configure(text=str(task_id))

                # Update the servingp2 label based on the priority
                if priority == 'P':
                    servingp2.configure(text=f"{priority}")
                else:
                    servingp2.configure(text="")

            else:
                # If no task is being processed, set default text in servingqueue2 and clear servingp2
                servingqueue2.configure(text="--")
                servingp2.configure(text="")

            # Schedule the next update after 1 second (1000 ms)
            servingqueue2.after(1000, update_serving2)

        except mysql.connector.Error as err:
            print(f"Failed to connect to MySQL database: {err}")

    # Create the label for showing the priority and queue
    servingp2 = ctk.CTkLabel(master=nowservingframe2, text='', font=("Arial", 30))
    servingp2.place(relx=0.5, rely=0.3, anchor='center')

    # Create the label for showing the serving queue
    servingqueue2 = ctk.CTkLabel(master=nowservingframe2, text='', font=("Arial", 55))
    servingqueue2.place(relx=0.5, rely=0.5, anchor='center')

    # Call the function initially to start updating the serving queue and priority
    update_serving2()

    # Apply the same custom style to serving2_pending_view
    serving2_pending_view = ttk.Treeview(frame2_display, columns=("task_id", "priority"), show="headings", height=5, style='NoBorder.Treeview')

    # Configure the columns
    serving2_pending_view.heading("task_id", text="QUEUE")
    serving2_pending_view.heading("priority", text="STATUS")

    # Set column widths
    serving2_pending_view.column("task_id", width=160, anchor='center')
    serving2_pending_view.column("priority", width=160,anchor='center')

    # Place the serving2_pending_view widget in the frame
    serving2_pending_view.place(x=15, rely=0.6)

    def fetch_and_populate_serving2_pending_view():
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
            cursor = conn.cursor()

            # Execute a query to fetch task_id and priority from the queue table where status is 'PENDING' and counter is 'COUNTER 2'
            query = "SELECT task_id, priority FROM queue WHERE status = 'PENDING' AND counter = 'COUNTER 2'"
            cursor.execute(query)

            # Fetch all results
            results = cursor.fetchall()

            # Clear existing data from the serving2_pending_view
            for item in serving2_pending_view.get_children():
                serving2_pending_view.delete(item)

            # Check if there are results
            if results:
                # Separate results into two lists based on priority
                priority_p = []
                priority_np = []

                for task_id, priority in results:
                    if priority == "P":
                        priority_p.append((task_id, priority))
                    else:
                        priority_np.append((task_id, priority))

                # First, insert tasks with priority "P" into the Treeview
                for task_id, priority in priority_p:
                    # Prepend a bullet character to the task_id
                    bullet_task_id = f"• {task_id}"
                    serving2_pending_view.insert('', 'end', values=(bullet_task_id, priority))

                # Then, insert tasks with priority "NP" into the Treeview
                for task_id, priority in priority_np:
                    # Prepend a bullet character to the task_id
                    bullet_task_id = f"• {task_id}"
                    serving2_pending_view.insert('', 'end', values=(bullet_task_id, priority))

            else:
                # If there are no pending tasks, insert a row with "None" for each column
                serving2_pending_view.insert('', 'end', values=("--", "--"))

            # Close the cursor and connection
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Failed to connect to MySQL database: {err}")

        # Schedule the next update after 1 second (1000 ms)
        serving2_pending_view.after(1000, fetch_and_populate_serving2_pending_view)

    # Call the function initially to start populating the serving2_pending_view
    fetch_and_populate_serving2_pending_view()

    # Function to update the date and time in the label
    def update_time_date():
        current_time_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Update the text of both labels
        timedate_label.configure(text=current_time_date)
        timedate2_label.configure(text=current_time_date)
        # Schedule the function to run again in 1 second (1000 ms)
        timedate_label.after(1000, update_time_date)

    # Call the function initially to start updating the date and time
    update_time_date()

    display_window.mainloop()

    