import psycopg2

"""
	Creates a new table named 'students' in the PostgreSQL database 'studentdb'.
	
	Establishes a connection to the database, creates a cursor object, and executes a SQL query to create the table.
	
	The table has the following columns:
	- student_id (serial primary key)
	- name (text)
	- address (text)
	- age (int)
	- number (text)
	
	Commits the changes and closes the database connection.
	
	Parameters:
	None
	
	Returns:
	None
"""
def create_table():
    #code to establish a connection to database.
    conn = psycopg2.connect(dbname="studentdb",user="postgres",password="root123#",host="localhost",port="5432")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE students(student_id serial primary key,name text,address text,age int,number text);""")
    print("student table created")
    conn.commit()
    conn.close()


"""
    Inserts a new student record into the 'students' table in the PostgreSQL database 'studentdb'.

    Prompts the user to enter the student's name, address, age, and phone number.
    
    Establishes a connection to the database, creates a cursor object, and executes an SQL query to insert the new record.
    
    Commits the changes and closes the database connection.

    Parameters:
        None

    Returns:
        None
"""
def insert_data():
    name = input("Enter name: ")
    address = input("Enter address: ")
    age = input("Enter age: ")
    number = input("Enter phone number: ")
    conn = psycopg2.connect(dbname="studentdb",user="postgres",password="admin123",host="localhost",port="5432")
    cur = conn.cursor()
    cur.execute("""INSERT INTO students(name,address,age,number) VALUES (%s,%s,%s,%s)""",(name,address,age,number))
    print("student table created")
    conn.commit()
    conn.close()

def delete_data():
    student_id = input("Enter id of the student to delete: ")
    
    # Connect to the database
    conn = psycopg2.connect(dbname="studentdb", user="postgres", password="admin123", host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute("select * from students where student_id=(%s)",(student_id, ))
    student = cur.fetchone()

    if student:
        print(f"Student to be deleted: ID {student[0]}, Name {student[1]}, Address {student[2]}, Age {student[3]}, Number {student[4]}")
        choice = input("Are you want to delete the student? (yes/no)") 
        if choice.lower() == "yes":
            cur.execute("delete from students where student_id=%s", (student_id, ))
            print("Student deleted successfully")
        else:
            print("Student not deleted")
    else:
        print("Student not found")

    conn.commit()
    conn.close()


"""
    Updates a student's record in the PostgreSQL database 'studentdb'.

    Prompts the user to enter the ID of the student to be updated and the field to be updated.
    
    Establishes a connection to the database, creates a cursor object, and executes an SQL query to update the record.
    
    Commits the changes and closes the database connection.

    Parameters:
        None

    Returns:
        None
"""    
def update_data():
 
    student_id = input("Enter the ID of the student to be updated: ")
    
    # Connect to the database
    conn = psycopg2.connect(dbname="studentdb", user="postgres", password="admin123", host="localhost", port="5432")
    cur = conn.cursor()
    
    # Available fields to update
	#Field name and prompt
    fields = {
        "1": ("name", "Enter the new name: "),
        "2": ("address", "Enter the new address: "),
        "3": ("age", "Enter the new age: "),
        "4": ("number", "Enter the new phone number: ")
    }
    
    print("Which field would you like to update?")
	#Loop through all the fields
    for key in fields:
		# Print the field name
        print(f"{key}: {fields[key][0]}")
		#Accept the choice from user
    field_choice = input("Enter the number of the field you want to update: ")
    
	#If the choice is present, then get the field name i.e name age to be updated
	# on the basis of above choice
    if field_choice in fields:
        field_name, prompt = fields[field_choice]
		# prompt. the user to enter the new value for field
        new_value = input(prompt)
        
        # Constructing and executing the SQL update statement
        sql = f"UPDATE students SET {field_name} = %s WHERE student_id = %s"
        cur.execute(sql, (new_value, student_id))
        
        print(f"{field_name} updated successfully.")
    else:
        print("Invalid choice.")
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    

def list_db():
    # Connect to the database
    conn = psycopg2.connect(dbname="studentdb", user="postgres", password="admin123", host="localhost", port="5432")
    cur = conn.cursor()

    # execute the query
    cur.execute("SELECT * FROM students")

    # fetch all the rows
    rows = cur.fetchall()

    # print the rows
    for row in rows:
        print(row)

    # close the cursor and connection
    cur.close()
    conn.close()

create_table()