import psycopg2
import os

# ---------- Database Connection ----------
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "emsdb"),       # default = emsdb
            user=os.getenv("DB_USER", "postgres"),      # default = postgres
            password=os.getenv("DB_PASSWORD", "password"),  # set in environment
            host=os.getenv("DB_HOST", "localhost"),     # default = localhost
            port=os.getenv("DB_PORT", "5432")           # default = 5432
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        exit()

# ---------- Functions ----------
def add_employee(conn, name, age, department, salary):
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO employees (name, age, department, salary) VALUES (%s, %s, %s, %s)",
            (name, age, department, salary)
        )
        conn.commit()
        cur.close()
        print("Employee added successfully!")
    except Exception as e:
        print("Error adding employee:", e)

def view_employees(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees")
        rows = cur.fetchall()
        print("\n--- Employee Records ---")
        for row in rows:
            print(row)
        cur.close()
    except Exception as e:
        print("Error fetching employees:", e)

def search_employee(conn, emp_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees WHERE id=%s", (emp_id,))
        row = cur.fetchone()
        if row:
            print("\nFound:", row)
        else:
            print("Employee not found!")
        cur.close()
    except Exception as e:
        print("Error searching employee:", e)

def update_employee(conn, emp_id, name, age, department, salary):
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE employees 
            SET name=%s, age=%s, department=%s, salary=%s 
            WHERE id=%s
        """, (name, age, department, salary, emp_id))
        conn.commit()
        cur.close()
        print("Employee updated successfully!")
    except Exception as e:
        print("Error updating employee:", e)

def delete_employee(conn, emp_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
        conn.commit()
        cur.close()
        print("Employee deleted successfully!")
    except Exception as e:
        print("Error deleting employee:", e)

# ---------- Menu with match-case ----------
def menu():
    conn = connect_db()
    while True:
        print("\n===== Employee Management System =====")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Exit")

        choice = input("Enter choice: ")

        match choice:
            case "1":
                try:
                    name = input("Enter name: ")
                    age = int(input("Enter age: "))
                    dept = input("Enter department: ")
                    salary = float(input("Enter salary: "))
                    add_employee(conn, name, age, dept, salary)
                except ValueError:
                    print("Invalid input for age/salary!")

            case "2":
                view_employees(conn)

            case "3":
                try:
                    emp_id = int(input("Enter Employee ID: "))
                    search_employee(conn, emp_id)
                except ValueError:
                    print("Invalid Employee ID!")

            case "4":
                try:
                    emp_id = int(input("Enter Employee ID to update: "))
                    name = input("Enter new name: ")
                    age = int(input("Enter new age: "))
                    dept = input("Enter new department: ")
                    salary = float(input("Enter new salary: "))
                    update_employee(conn, emp_id, name, age, dept, salary)
                except ValueError:
                    print("Invalid input!")

            case "5":
                try:
                    emp_id = int(input("Enter Employee ID to delete: "))
                    delete_employee(conn, emp_id)
                except ValueError:
                    print("Invalid Employee ID!")

            case "6":
                print("Exiting system...")
                conn.close()
                break

            case _:
                print("Invalid choice, try again!")

# ---------- Run ----------
if __name__ == "__main__":
    menu()
