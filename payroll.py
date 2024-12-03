import mysql.connector as mc
from datetime import datetime

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
    working_days = int(input("Enter Total Working Days: "))
    
    hra = 0.08 * salary  # 8% of salary
    pf_employee = 0.12 * salary  # 12% of salary from the employee
    pf_company = 0.12 * salary  # 12% of salary from the company
    pf_total = pf_employee + pf_company
    date_of_joining = datetime.now().strftime('%Y-%m-%d')  # Current time
    medical_leave = 15

    # Calculate DA based on joining month
    da = 0
    joining_month = datetime.now().month
    if joining_month <= 6:  # Before or in June
        da = 0.28 * salary
    else:  # After July
        da = 0.14 * salary
    
    # Insert query
    query = f"""INSERT INTO {table} 
    (emp_id, name, position, salary, department, PF, DA, HRA, medical_leave, working_days, date_of_joining) 
    VALUES ({emp_id}, '{name}', '{position}', {salary}, '{department}', {pf_total}, {da}, {hra}, {medical_leave}, {working_days}, '{date_of_joining}');
    """
    try:
        cursor.execute(query)
        connection.commit()
        print("Employee added successfully!")
    except mc.Error as err:
        print(f"Error: {err}")

# Display all employees
def display_employees(connection):
    cursor = connection.cursor()
    query = f"SELECT * FROM {table};"
    cursor.execute(query)
    results = cursor.fetchall()
    print("\n--- Employee Records ---")
    print("ID | Name | Position | Salary | Department | PF | DA | HRA | Medical Leave | Working Days | Date of Joining")
    for row in results:
        print(" | ".join(map(str, row)))

# Update employee info
def update_info(connection):
    cursor = connection.cursor()
    emp_id = int(input("Enter Employee ID to update: "))
    print("Choose the field to update:")
    print("1. Name")
    print("2. Department")
    print("3. Position")
    print("4. Salary")
    print("5. Date of Joining")
    print("6. Medical Leave Days")

    choice = int(input("Enter your choice (1-6): "))

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

        # Fetch the existing date_of_joining to calculate DA
        cursor.execute(f"SELECT date_of_joining FROM {table} WHERE emp_id = {emp_id};")
        result = str(cursor.fetchone()[0])
        if not result:
            print("Employee not found.")
            return
        joining_month = int(result.split("-")[1])

        # Calculate DA based on existing date_of_joining
        if joining_month <= 6:
            new_da = float(0.28 * new_salary)
        else:
            new_da = float(0.14 * new_salary)

        # Recalculate HRA and PF
        hra = 0.08 * new_salary
        pf_employee = 0.12 * new_salary
        pf_company = 0.12 * new_salary
        pf_total = pf_employee + pf_company

        query = f"""
        UPDATE {table} 
        SET salary = {new_salary}, HRA = {hra}, PF = {pf_total}, DA = {new_da} 
        WHERE emp_id = {emp_id};
        """
    elif choice == 5:
        new_date = input("Enter New Date of Joining (YYYY-MM-DD): ")
        try:
            joining_month = int(new_date.split("-")[1])

            # Determine new DA based on updated date
            cursor.execute(f"SELECT salary FROM {table} WHERE emp_id = {emp_id};")
            salary = cursor.fetchone()[0]  # Fetch current salary of the employee
            
            if joining_month <= 6:  # Before or in June
                new_da = float(0.28 * salary)
            else:  # After or in July
                new_da = float(0.14 * salary)

            query = f"""
            UPDATE {table} 
            SET date_of_joining = '{new_date}', DA = {new_da} 
            WHERE emp_id = {emp_id};
            """
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
    elif choice == 6:
        new_medical_leave = int(input("Enter New Medical Leave Days: "))
        query = f"UPDATE {table} SET medical_leave = {new_medical_leave} WHERE emp_id = {emp_id};"
    else:
        print("Invalid choice.")
        return

    try:
        cursor.execute(query)
        connection.commit()
        print("Record updated successfully!")
    except mc.Error as err:
        print(f"Error: {err}")

# Take loan from PF
def take_loan(connection):
    cursor = connection.cursor()
    emp_id = int(input("Enter Employee ID to take loan: "))
    query = f"SELECT PF FROM {table} WHERE emp_id = {emp_id};"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        pf_amount = result[0]
        max_loan = 0.6 * pf_amount  # Maximum loan is 60% of PF
        print(f"Maximum loan you can take is: {max_loan}")
        loan_amount = float(input("Enter loan amount: "))

        if loan_amount <= max_loan:
            new_pf = pf_amount - loan_amount
            update_query = f"UPDATE {table} SET PF = {float(new_pf)} WHERE emp_id = {emp_id};"
            try:
                cursor.execute(update_query)
                connection.commit()
                print("Loan successfully taken.")
            except mc.Error as err:
                print(f"Error: {err}")
        else:
            print("Loan amount exceeds maximum limit.")
    else:
        print("Employee not found.")

# increase PF
def PF_increment(connection):
    cursor = connection.cursor()
    ct = datetime.now().strftime('%Y-%m-%d')
    cm = int(str(ct).split("-")[1])
    cy= int(str(ct).split("-")[0])
    cursor.execute(f"SELECT * FROM {table};")
    result = cursor.fetchall()
    
    for i in result:
        joining_month = int(str(i[10]).split("-")[1])
        join_year = int(str(i[10]).split("-")[0])
        if (cy==join_year):
            diff = cm-joining_month
            if (diff>0):
                e_pf = i[5]
                new_pf = (0.24+0.0825*diff)*i[3]
                if (e_pf!=new_pf):
                    query = f"""
                        UPDATE {table} 
                        SET PF = {float(new_pf)} 
                        WHERE emp_id = {i[0]};
                        """
                    cursor.execute(query)
                    connection.commit()

            else:
                new_pf = 0.24*float(i[3])
                query = f"""
                        UPDATE {table} 
                        SET PF = {new_pf} 
                        WHERE emp_id = {i[0]};
                        """
                cursor.execute(query)
                connection.commit()
        
        elif (join_year<cy):
            if (cy-join_year==1):
                total_months = 12-joining_month+ cm
            else:
                total_months = 12-joining_month+ (cy-join_year-1)*12+cm
                
            new_pf = (0.24+0.0825*total_months)*i[3]
            query = f"""
                        UPDATE {table} 
                        SET PF = {float(new_pf)} 
                        WHERE emp_id = {i[0]};
                        """
            cursor.execute(query)
            connection.commit()


# Show instructions
def show_instructions():
    print("\n--- Payroll Instructions ---")
    print("1. HRA is 8% of the salary.")
    print("2. PF is 12% from the company and 12% from the employee.")
    print("3. PF accrues 8.25% monthly interest from the company contribution.")
    print("4. DA is given twice a year (Jan-June and July-Dec) at 14%.")
    print("5. Maximum loan from PF is 60% of the current PF balance.")

# Delete an employee record
def delete_employee(connection):
    cursor = connection.cursor()
    emp_id = int(input("Enter Employee ID to delete: "))
    query = f"DELETE FROM {table} WHERE emp_id = {emp_id};"
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
        print("4. Take Loan")
        print("5. Show Instructions")
        print("6. Delete Employee")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_employee(connection)
        elif choice == "2":
            display_employees(connection)
        elif choice == "3":
            update_info(connection)
        elif choice == "4":
            take_loan(connection)
        elif choice == "5":
            show_instructions()
        elif choice == "6":
            delete_employee(connection)
        elif choice == "7":
            print("Exiting program. Goodbye!")
            connection.close()
            break
        else:
            print("Invalid choice. Please try again.")
        PF_increment(connection)

if __name__ == "__main__":
    main()
