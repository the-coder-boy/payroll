import mysql.connector as mc
db = None
table = None
# Connect to the MySQL database
def connect_db():
    try:
        connection = mc.connect(
            host="localhost",   
            user="root",         
            password="", 
            database=db  
        )
        return connection
    except mc.Error as err:
        print(f"Error: {err}")
        return None

# Add a new employee
def add_employee(connection):
    cursor = connection.cursor()
    emp_id = int(input("Enter Employee ID: "))
    name = input("Enter Employee Name: ")
    position = input("Enter Employee Position: ")
    salary = float(input("Enter Salary: "))
    department = input("Enter Department: ")
    query = f"INSERT INTO {table} VALUES ({emp_id}, '{name}', '{position}', '{salary}',' {department}');"
    try:
        cursor.execute(query)
        connection.commit()
        print("Employee added successfully!")
    except mc.Error as err:
        print(f"Error: {err}")

# Display all employees
def display_employees(connection):
    cursor = connection.cursor()
    query = f'SELECT * FROM {table}'
    cursor.execute(query)
    results = cursor.fetchall()
    print("\n--- Employee Records ---")
    print("ID | Name | Position | Salary | Department")
    for row in results:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

# Update employee info
def update_info(connection):
    cursor = connection.cursor()
    emp_id = int(input("Enter Employee ID to update: "))
    print("Choose the field to update:")
    print("1. Name")
    print("2. Department")
    print("3. Position")
    print("4. Salary")

    choice = int(input("Enter your choice (1-4): "))

    if choice == 1:
        new_name = input("Enter New Name: ")
        query = f"UPDATE {table} SET name = '{new_name}' WHERE emp_id = {emp_id};"
    elif choice == 2:
        new_department = input("Enter New Department: ")
        query = f"UPDATE {table} SET department = '{new_department}' WHERE emp_id = {emp_id};"
    elif choice == 3:
        new_position = input("Enter New Position: ")
        query = f"UPDATE {table} SET position = '{new_position}' WHERE emp_id = {emp_id};"
    elif choice == 4:
        new_salary = float(input("Enter New Salary: "))
        query = f"UPDATE {table} SET salary = {new_salary} WHERE emp_id = {emp_id};"
    else:
        print("Invalid choice.")
        exit()
    try:
        cursor.execute(query)
        connection.commit()
        if cursor.rowcount > 0:
            print("Salary updated successfully!")
        else:
            print("Employee not found.")
    except mc.Error as err:
        print(f"Error: {err}")

# Delete an employee record
def delete_employee(connection):
    cursor = connection.cursor()
    emp_id = int(input("Enter Employee ID to delete: "))
    query = f'DELETE FROM {table} WHERE emp_id = {emp_id};'
    try:
        cursor.execute(query)
        connection.commit()
        if cursor.rowcount > 0:
            print("Employee deleted successfully!")
        else:
            print("Employee not found.")
    except mc.Error as err:
        print(f"Error: {err}")

# Main menu
def main():
    global db
    global table
    db = input("Enter name of database - ")
    table = input("Enter name of table - ")
    connection = connect_db()
    if not connection:
        print("Failed to connect to the database. Exiting...")
        return
    while True:
        print("\n--- Payroll Management System ---")
        print("1. Add Employee")
        print("2. Display Employees")
        print("3. Update Info")
        print("4. Delete Employee")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_employee(connection)
        elif choice == "2":
            display_employees(connection)
        elif choice == "3":
            update_info(connection)
        elif choice == "4":
            delete_employee(connection)
        elif choice == "5":
            print("Exiting program. Goodbye!")
            connection.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
