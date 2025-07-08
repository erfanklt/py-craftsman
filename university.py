# Import required libraries
import mysql.connector  # For database connectivity
import emoji  # For emoji support in output messages
import re  # For input validation using regular expressions

# ---------------------- Student Class ----------------------
class Student:
    """
    Student class to represent a university student
    Stores personal information and generates a unique student code
    """
    def __init__(self, first_name, last_name, national_id, birth_year, email):
        self.first_name = first_name
        self.last_name = last_name
        self.national_id = national_id
        self.birth_year = birth_year
        self.email = email
        self.student_code = self.generate_student_code()

    def generate_student_code(self):
        return f"{self.national_id}{self.birth_year}"

# ------------------ Input Validation Functions ------------------

def is_valid_name(name):
    return re.fullmatch(r"[A-Za-z]+", name)

def is_valid_national_id(nid):
    return re.fullmatch(r"\d{10}", nid)

def is_valid_birth_year(year):
    return re.fullmatch(r"(13[0-9]{2}|140[0-4])", year)

def is_valid_email(email):
    return re.fullmatch(r"[\w\.-]+@[\w\.-]+\.\w{2,}", email)

# ---------------------------------------------------------------

def insert_student_to_db(student):
    try:
        connect = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="university_db"
        )
        cursor = connect.cursor()
        query = "INSERT INTO students_table (name , family , national_id , birth_year , email , code)\
            VALUES (%s , %s, %s, %s, %s, %s)"
        data = (student.first_name, student.last_name, student.national_id, student.birth_year, student.email, student.student_code)
        cursor.execute(query, data)
        connect.commit()
        print("Student registration completed", emoji.emojize(":check_mark_button:", language="alias"))
    except mysql.connector.Error as err:
        print("We have an error", emoji.emojize(":cross_mark:", language="alias"), ":", f"{err}")
    finally:
        if connect.is_connected():
            cursor.close()
            connect.close()

def show_all_students():
    try:
        connect = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="university_db"
        )
        cursor = connect.cursor()
        query = "SELECT code , name , family FROM students_table"
        cursor.execute(query)
        result = cursor.fetchall()
        print("List of students", emoji.emojize(":clipboard:", language="alias"), ":\n")
        print("-" * 40)
        for row in result:
            code, name, family = row
            print(emoji.emojize(":mortar_board:", language="alias"), f"Code: {code} | First Name: {name} | Last Name: {family}")
        print("-" * 40)
    except mysql.connector.Error as err:
        print("We have an error", emoji.emojize(":cross_mark:", language="alias"), ":", f"{err}")
    finally:
        if connect.is_connected():
            cursor.close()
            connect.close()

def register_student():
    print(emoji.emojize(":pencil: Please enter student information", language="alias"))

    while True:
        first_name = input("Name: ")
        if is_valid_name(first_name):
            break
        print(emoji.emojize(":cross_mark: Invalid name. Use only English letters. :cross_mark:", language="alias"))

    while True:
        last_name = input("Family: ")
        if is_valid_name(last_name):
            break
        print(emoji.emojize(":cross_mark: Invalid family name. Use only English letters. :cross_mark:", language="alias"))

    while True:
        national_id = input("National ID: ")
        if is_valid_national_id(national_id):
            break
        print(emoji.emojize(":cross_mark: Invalid National ID. Must be exactly 10 digits. :cross_mark:", language="alias"))

    while True:
        birth_year = input("Birth Year (Shamsi): ")
        if is_valid_birth_year(birth_year):
            break
        print(emoji.emojize(":cross_mark: Invalid birth year. Must be between 1300 and 1404. :cross_mark:", language="alias"))

    while True:
        email = input("Email: ")
        if is_valid_email(email):
            break
        print(emoji.emojize(":cross_mark: Invalid email format. :cross_mark:", language="alias"))

    student = Student(first_name, last_name, national_id, birth_year, email)
    insert_student_to_db(student)

def delete_student_by_national_id():
    national_id = input("Enter National ID to delete: ")

    if not re.fullmatch(r"\d{10}", national_id):
        print(emoji.emojize(":cross_mark: Invalid national ID format. Must be exactly 10 digits. :cross_mark:", language="alias"))
        return

    try:
        connect = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="university_db"
        )
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM students_table WHERE national_id = %s", (national_id,))
        result = cursor.fetchone()

        if not result:
            print(emoji.emojize(":warning: No student found with this National ID. :warning:", language="alias"))
            return

        confirm = input("Are you sure you want to delete this student? (yes/no): ").lower()
        if confirm != "yes":
            print(emoji.emojize(":cross_mark: Deletion cancelled. :cross_mark:", language="alias"))
            return

        cursor.execute("DELETE FROM students_table WHERE national_id = %s", (national_id,))
        connect.commit()

        print(emoji.emojize(":check_mark_button: Student successfully deleted. :check_mark_button:", language="alias"))

    except mysql.connector.Error as err:
        print(emoji.emojize(":cross_mark: Database error :cross_mark: ", language="alias") + f"{err}")

    finally:
        if connect.is_connected():
            cursor.close()
            connect.close()

def main():
    print(emoji.emojize(":man_student: Welcome to the Student Management System :books:", language="alias"))

    while True:
        print("\n" + "-" * 40)
        print(emoji.emojize(":gear: Menu Options:", language="alias"))
        print("1.", emoji.emojize(":memo:", language="alias"), "Register new student")
        print("2.", emoji.emojize(":clipboard:", language="alias"), "Show all students")
        print("3.", emoji.emojize(":wastebasket:", language="alias"), "Delete student by National ID")
        print("4.", emoji.emojize(":door:", language="alias"), "Exit")
        print("-" * 40)

        choice = input("Select an option (1-4): ")

        if choice == "1":
            register_student()
        elif choice == "2":
            show_all_students()
        elif choice == "3":
            delete_student_by_national_id()
        elif choice == "4":
            print(emoji.emojize("Exiting... Goodbye! :waving_hand:", language="alias"))
            break
        else:
            print(emoji.emojize(":cross_mark: Invalid option. Please choose 1 to 4. :cross_mark:", language="alias"))

# Entry point
if __name__ == "__main__":
    main()
