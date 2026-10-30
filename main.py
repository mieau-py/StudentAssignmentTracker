
from database import test_connection
from todo import (
    add_assignment,
    view_assignments,
    update_assignment,
    delete_assignment,
)

def main():
    print("=" * 40)
    print("   STUDENT ASSIGNMENT TRACKER")
    print("=" * 40)

    if not test_connection():
        print("Please fix the database connection before continuing.")
        return

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Add Assignment")
        print("2. View Assignments")
        print("3. Update Assignment")
        print("4. Delete Assignment")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_assignment()
        elif choice == "2":
            view_assignments()
        elif choice == "3":
            update_assignment()
        elif choice == "4":
            delete_assignment()
        elif choice == "5":
            print("Thank you for using Student Assignment Tracker!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
