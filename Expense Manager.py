# todo : handle application potential bugs on inputs

import sqlite3


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
        amount = float(input("Enter amount : "))
        category = input("Enter expense category : ")
        date = input("Enter expense date (YYYY-MM-DD): ")
        detail = input("Enter expense detail : ")

        self.cursor.execute(sql, (amount, category, date, detail))
        self.conn.commit()
        print("Expense added successfully")

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
        e_id = int(input("Enter Expense_Id you want to update : "))
        amount = float(input("Enter new amount : "))
        category = input("Enter expense category : ")
        date = input("Enter expense date : ")
        detail = input("Enter expense detail : ")
        self.cursor.execute(sql, (amount, category, date, detail, e_id))
        self.conn.commit()
        print("Expense updated successfully")


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
                table = manager.select_expense()
                for i in table:
                    print(i)

            elif command == 3:
                manager.delete_expense()

            elif command == 4:
                manager.update_expense()

            else:
                print("Program successfully closed.")
                manager.conn.close()
                break
