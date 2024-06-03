# todo : add more options on select query

import sqlite3
import re


class ExpenseManager:
    def __init__(self):
        self.conn = sqlite3.connect('./Expenses.db')
        self.cursor = self.conn.cursor()

    def create_expense_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Expenses(
            Expense_Id INTEGER NOT NULL,
            Expense_Amount REAL NOT NULL,
            Expense_Category VARCHAR(100) NOT NULL,
            Expense_Date DATE NOT NULL,
            Expense_Detail TEXT NOT NULL,
            PRIMARY KEY (Expense_Id)
            );
        """
        self.cursor.execute(sql)
        self.conn.commit()
        print("Table Created")

    def insert_expense(self):
        sql = """
            INSERT INTO Expenses(Expense_Amount, Expense_Category, Expense_Date , Expense_Detail)
            values (?,?,?,?)
        """
        while True:
            try:
                amount = float(input("Enter amount : "))
                category = input("Enter expense category : ")
                date = input("Enter expense date (YYYY-MM-DD): ")
                result = re.search(r"^\d{4}\-\d{2}\-\d{2}$", date)
                if not result:
                    raise ValueError("Invalid date format")
                detail = input("Enter expense detail : ")
                self.cursor.execute(sql, (amount, category, date, detail))
                self.conn.commit()
            except Exception as error:
                print(error)
            else:
                print("Expense added successfully")
                break


    def delete_expense(self):
        sql = """
        DELETE FROM Expenses WHERE Expense_Id = ?
        """
        value = int(input("Enter expense id : "))
        self.cursor.execute(sql, (value,))
        self.conn.commit()
        print("Expense successfully deleted")

    def select_expense(self):
        sql = """
        SELECT * FROM Expenses
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def update_expense(self):
        sql = """
        UPDATE Expenses SET Expense_Amount = ?, Expense_Category = ?, Expense_Date = ?, Expense_Detail = ?
        WHERE Expense_Id = ?
        """
        while True:
            try:
                e_id = int(input("Enter Expense_Id you want to update : "))
                amount = float(input("Enter amount : "))
                category = input("Enter expense category : ")
                date = input("Enter expense date (YYYY-MM-DD): ")
                result = re.search(r"^\d{4}\-\d{2}\-\d{2}$", date)
                if not result:
                    raise ValueError("Invalid date format")
                detail = input("Enter expense detail : ")
                self.cursor.execute(sql, (amount, category, date, detail, e_id))
                self.conn.commit()

            except Exception as error:
                print(error)

            else:
                print("Expense updated successfully")
                break


if __name__ == '__main__':
    manager = ExpenseManager()
    manager.create_expense_table()

    while True:
        print("""
        1. Add Expense
        2. Show Expenses
        3. Delete Expense
        4. Update Expense
        5. Exit
        """)

        try:
            command = int(input("Enter your choice : "))
            if command not in range(1, 6):
                raise ValueError("Invalid choice")
        except Exception as e:
            print(e)
        else:
            if command == 1:
                manager.insert_expense()

            elif command == 2:
                rows = manager.select_expense()
                if rows is not None:
                    for row in rows:
                        print(row)
                else:
                    print("No expense available")

            elif command == 3:
                manager.delete_expense()

            elif command == 4:
                manager.update_expense()

            else:
                print("Program successfully closed.")
                manager.conn.close()
                break
