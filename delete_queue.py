import mysql.connector
from tkinter import messagebox as mb


def delete_all_queues():
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='queue_db')
    except mysql.connector.Error as err:
        print('Database error:', err)
        return

    cursor = conn.cursor()
    
    try:

        cursor.execute("SELECT COUNT(*) FROM queue")
        num_queues = cursor.fetchone()[0]
        
        if num_queues == 0:
            mb.showerror("error","Queue is empty")
            return
        # Confirm deletion with user
        confirm_deletion = mb.askyesno("Confirm Deletion", "Are you sure you want to delete all queues?")
        
        if not confirm_deletion:
            print("Deletion cancelled.")
            return
        
        # Delete all rows from the queue table
        delete_query = "DELETE FROM queue"
        cursor.execute(delete_query)
        
        # Reset auto increment ID
        reset_query = "SET @autoid := 0;"
        cursor.execute(reset_query)
        
        update_query = "UPDATE queue SET task_id = @autoid := (@autoid + 1);"
        cursor.execute(update_query)
        
        alter_query = "ALTER TABLE queue AUTO_INCREMENT = 1;"
        cursor.execute(alter_query)
        
        # Commit the changes
        conn.commit()
        
        print("All queues deleted successfully and auto ID reset.")
        
    except mysql.connector.Error as err:
        print("Error:", err)
        conn.rollback()  # Rollback changes if there's an error
    
    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()