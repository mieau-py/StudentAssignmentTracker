
from mysql.connector import Error
from database import get_connection


def add_assignment():
    print("\n--- Add Assignment ---")

    subject = input("Enter subject: ").strip()
    title = input("Enter assignment title: ").strip()
    description = input("Enter description (optional): ").strip()
    due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip()

    if not subject or not title:
        print("Subject and title cannot be empty.")
        return

    if due_date == "":
        due_date = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO assignments
            (subject, title, description, due_date)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (subject, title, description or None, due_date)
        )

        connection.commit()
        print("Assignment added successfully!")

    except Error as error:
        print(f"Error adding assignment: {error}")

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()


def view_assignments():
    print("\n--- View Assignments ---")

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT id, subject, title, description, due_date, status
            FROM assignments
            ORDER BY id
        """

        cursor.execute(query)
        assignments = cursor.fetchall()

        if not assignments:
            print("No assignments found.")
        else:
            for assignment in assignments:
                print("\n------------------------------")
                print(f"ID: {assignment[0]}")
                print(f"Subject: {assignment[1]}")
                print(f"Title: {assignment[2]}")
                print(f"Description: {assignment[3] or 'None'}")
                print(f"Due date: {assignment[4] or 'None'}")
                print(f"Status: {assignment[5]}")
            print("\n------------------------------")

    except Error as error:
        print(f"Error viewing assignments: {error}")

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()


def update_assignment():
    print("\n--- Update Assignment ---")

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, subject, title, description, due_date, status "
            "FROM assignments ORDER BY id"
        )
        assignments = cursor.fetchall()

        if not assignments:
            print("No assignments to update.")
            return

        for assignment in assignments:
            print(
                f"ID: {assignment[0]} | "
                f"Subject: {assignment[1]} | "
                f"Title: {assignment[2]} | "
                f"Status: {assignment[5]}"
            )

        assignment_id = input(
            "\nEnter the ID of the assignment to update: "
        ).strip()

        if not assignment_id.isdigit():
            print("Please enter a valid numeric ID.")
            return

        cursor.execute(
            "SELECT subject, title, description, due_date, status "
            "FROM assignments WHERE id = %s",
            (int(assignment_id),)
        )
        current = cursor.fetchone()

        if current is None:
            print("Assignment ID not found.")
            return

        print("Press Enter to keep the current value.")
        print("For description or due date, type NONE to clear it.")

        subject_input = input(
            f"Subject [{current[0]}]: "
        ).strip()
        title_input = input(
            f"Title [{current[1]}]: "
        ).strip()
        description_input = input(
            f"Description [{current[2] or 'None'}]: "
        ).strip()
        due_date_input = input(
            f"Due date [{current[3] or 'None'}] (YYYY-MM-DD): "
        ).strip()
        status_input = input(
            f"Status [{current[4]}] (Pending/Completed): "
        ).strip()

        subject = subject_input or current[0]
        title = title_input or current[1]

        if description_input.upper() == "NONE":
            description = None
        elif description_input:
            description = description_input
        else:
            description = current[2]

        if due_date_input.upper() == "NONE":
            due_date = None
        elif due_date_input:
            due_date = due_date_input
        else:
            due_date = current[3]

        if status_input == "":
            status = current[4]
        elif status_input.lower() == "pending":
            status = "Pending"
        elif status_input.lower() == "completed":
            status = "Completed"
        else:
            print("Invalid status. Use Pending or Completed.")
            return

        query = """
            UPDATE assignments
            SET subject = %s, title = %s, description = %s,
                due_date = %s, status = %s
            WHERE id = %s
        """

        cursor.execute(
            query,
            (
                subject,
                title,
                description,
                due_date,
                status,
                int(assignment_id)
            )
        )

        connection.commit()
        print("Assignment updated successfully!")

    except Error as error:
        print(f"Error updating assignment: {error}")

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()


def delete_assignment():
    print("\n--- Delete Assignment ---")

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, subject, title FROM assignments ORDER BY id"
        )
        assignments = cursor.fetchall()

        if not assignments:
            print("No assignments to delete.")
            return

        for assignment in assignments:
            print(
                f"ID: {assignment[0]} | "
                f"Subject: {assignment[1]} | "
                f"Title: {assignment[2]}"
            )

        assignment_id = input(
            "\nEnter the ID of the assignment to delete: "
        ).strip()

        if not assignment_id.isdigit():
            print("Please enter a valid numeric ID.")
            return

        cursor.execute(
            "SELECT title FROM assignments WHERE id = %s",
            (int(assignment_id),)
        )
        assignment = cursor.fetchone()

        if assignment is None:
            print("Assignment ID not found.")
            return

        confirm = input(
            f"Delete '{assignment[0]}'? Type YES to confirm: "
        ).strip()

        if confirm == "YES":
            cursor.execute(
                "DELETE FROM assignments WHERE id = %s",
                (int(assignment_id),)
            )
            connection.commit()
            print("Assignment deleted successfully!")
        else:
            print("Deletion cancelled.")

    except Error as error:
        print(f"Error deleting assignment: {error}")

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()
