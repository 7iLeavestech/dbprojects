from flask import Flask, app, jsonify, request
import psycopg2

app = Flask(__name__)

# TODO Get rows from DB

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

@app.route('/tables', methods=['POST'])
def create_table():

    data = request.get_json()
    table_name = data['table_name']
    columns = data['columns']

    #code to establish a connection to database.
    conn = psycopg2.connect(dbname="studentdb",user="postgres",password="admin123",host="localhost",port="5432")
    cur = conn.cursor()

     # Create the table
    column_definitions = []
    for column in columns:
        column_definitions.append(f"{column['name']} {column['data_type']}")
    column_definitions_str = ", ".join(column_definitions)
    cur.execute(f"""CREATE TABLE {table_name} ({column_definitions_str});""")

    print(f"{table_name} table created"\sonify({'message': f'{table_name} table created successfully'}), 201

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

#TODO: Inserting multiple records
#TODO: Taking table name from user, currently db is hardcoded.

@app.route('/students', methods=['POST'])
def insert_data():
    # Get the data from the request body
    data = request.json

    name = data.get('name')
    address = data.get('address')
    age = data.get('age')
    number = data.get('number')
    
    conn = psycopg2.connect(dbname="studentdb",user="postgres",password="admin123",host="localhost",port="5432")
    cur = conn.cursor()
    cur.execute("""INSERT INTO students(name,address,age,number) VALUES (%s,%s,%s,%s)""",(name,address,age,number))
    print("student table created")
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Student inserted successfully'}), 201

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_data(student_id):
    # Connect to the database
    conn = psycopg2.connect(dbname="studentdb", user="postgres", password="admin123", host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute("select * from students where student_id=(%s)",(student_id, ))
    student = cur.fetchone()
    print(student)

    if student:
        print(f"Student to be deleted: ID {student[0]}, Name {student[1]}, Address {student[2]}, Age {student[3]}, Number {student[4]}")
        cur.execute("delete from students where student_id=%s", (student_id, ))
        conn.commit()
        conn.close()       
        return jsonify({'message': 'Student deleted successfully'}), 200
    
    conn.close()
    return jsonify({'message': 'Student record deletion failed'}), 404


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

@app.route('/students/<int:student_id>', methods=['PATCH'])
def update_partial_data(student_id):  
    # Connect to the database
    conn = psycopg2.connect(dbname="studentdb", user="postgres", password="admin123", host="localhost", port="5432")
    cur = conn.cursor()
    
    # Get the updated data from the request body
    data = request.json 

    # TODO: Can we update multiple fields at once?
    # Constructing and executing the SQL update statement
    for field_name, new_value in data.items():
        # Check if the field is present in the table        
        sql = f"UPDATE students SET {field_name} = %s WHERE student_id = %s"
        cur.execute(sql, (new_value, student_id))
        
        print(f"{field_name} updated successfully.")
    else:
        print("Invalid choice.")
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student updated successfully'}), 200

if __name__ == "__main__":
    app.run(port=4000, debug=True)