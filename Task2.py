#Expense Tracker System Python Code
#created by: Nouria Bellamri
#Date: 20/09/2024

import json
import os
from datetime import datetime

#File to store users and expenses
USER_FILE = "user.json"

# Load data from JSON file
def load_data(file_name=USER_FILE):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return {}
    
# Save data to JSON file
def save_data(data, file_name=USER_FILE):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

# User Login Function
def login(file_name=USER_FILE):
    data = load_data(file_name)
    Username = input("Enter your username:")
    Password = input("Enter your password:")

    if Username in data and data[Username]["password"] == Password:
       print(f"Welcome, {Username}!")
       return Username
    else:
        print("Invalid Credentials!")
        return None
    
# User Registration
def register(file_name=USER_FILE):
    data = load_data(file_name)
    Username = input("Enter a new username:")

    if Username in data:
        print("Username already exists!")
        return None
        
    Password = input("Enter a password:")
    data[Username] = {"password": Password, "expenses": [], "budget": None}
    save_data(data, file_name)
    print("Registration successful, Please login.")
    return Username
    
#Add new expense
def add_expense(Username, description=None, amount=None, category=None, file_name=USER_FILE):
    data = load_data(file_name)

    if description is None:
       description = input("Enter expense description:")
    if amount is None:
       amount = float(input("Enter expense amount:"))
    if category is None:
       category = input("Enter category expense:")

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expense = {"description": description, "amount": amount, "category": category, "date_time": date_time}

    data[Username]["expenses"].append(expense)
    save_data(data)
    print("Expense added successfully!")

# Check budget limit
    if data[Username]["budget"]:
        total_expenses = sum(exp['amount'] for exp in data[Username]["expenses"])
        if total_expenses >= data[Username]["budget"]:
           print(f"Warning: You have exceeded your budget of ${data[Username]['budget']}!")
        elif total_expenses >= 0.9 * data[Username]["budget"]:
           print(f"Alert: You are nearing your budget limit (${data[Username]['budget']}).")

# Update expense
def update_expense(Username, expense_id=None, description=None, amount=None, category=None, file_name=USER_FILE):
    data = load_data(file_name)
    expenses = data[Username]["expenses"]

    if not expenses:
        print("No expenses to update.")
        return False
        
    if expense_id is None:
       print_expenses(Username, file_name)
       expense_id = int(input("Enter the ID of the expense you want to update:")) - 1

    if 0 <= expense_id < len(expenses):
        if description is None:
           description = input("Enter new description (leave blank to keep current):")
        if amount is None:
           amount = input("Enter new amount(leave blank to keep current)")
        if category is None:
           category = input("Enter new category (leave blank to keep current)")

        if description:
          expenses[expense_id]["description"] = description
        if amount:
          amount = float(amount) if amount else expenses[expense_id]["amount"]
          expenses[expense_id]["amount"] = amount
        if category:
          expenses[expense_id]["category"] = category

        save_data(data, file_name)
        print("Expense updated successfully!")
        return True
    else:
        print("Invalid expense ID!")
        return False

# Delete expense
def delete_expense(Username, expense_id=None, file_name=USER_FILE):
    data = load_data(file_name)
    expenses= data[Username]["expenses"]

    if not expenses:
        print("No expenses to delete.")
        return False
    
    if expense_id is None:    
       print_expenses(Username, file_name)
       expense_id = int(input("Enter the ID of the expense you want to delete:")) - 1

    if 0 <=expense_id < len(expenses):
        expenses.pop(expense_id)
        save_data(data, file_name)
        print("Expense deleted successfully!")
        return True
    else:
        print("Invalid expense ID!")
        return False

# View expenses
def print_expenses(Username, file_name=USER_FILE):
    data = load_data(file_name)
    expenses = data[Username]["expenses"]

    if not expenses:
        print("No expenses found.")
    else:
        for idx, expense in enumerate(expenses, 1):
            print(f"{idx}. {expense['description']} - ${expense['amount']} - {expense['category']} - {expense['date_time']}")

# Set budget
def set_budget(Username, budget=None, file_name=USER_FILE):
    data = load_data(file_name)
    while budget is None or budget <=0: #Ensure budget is positive
          budget = float(input("Enter your budget limit:"))
          if budget <= 0:
             print("Budget must be a positive value, Please try again.")
             
    data[Username]["budget"] = budget
    save_data(data, file_name)
    print(f"Budget of ${budget} set successfully!")

# Generate detailed expense report and optionally save to file
def generate_report(Username, file_name=USER_FILE):
    data = load_data(file_name)
    expenses = data [Username]["expenses"]

    if not expenses:
        print("No expenses to report.")
        return ""
        
    total_spent = sum(exp["amount"] for exp in expenses)
    report = f"\nExpenses Report for {Username}\n"
    report += f"Total spent: ${total_spent: .2f}\n"
    for idx, expense in enumerate(expenses, 1):
        report += f"{idx}. {expense['description']} - ${expense['amount']} - {expense['category']} - {expense['date_time']}\n"
        print(report)

    save_option = input("\nWould you like to save this report to a file? (yes/no):").lower()
    if save_option == "yes":
        report_file = f"{Username}_expense_report.txt"
        with open(report_file, "w") as f:
            f.write(report)
        print(f"Repport saved to {report_file}")
    return report

# Main Program
def main():
    print("Welcome to the Expense Tracker System!")

    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Choose an option:")

        if choice == "1":
            Username = login()
            if Username:
                while True:
                    print("\n1. Add Expense")
                    print("2. Update Expense")
                    print("3. Delete Expense")
                    print("4. View Expense")
                    print("5. Set Budget")
                    print("6. Generate Expense Report")
                    print("7. Logout")
                    user_choice = input("Choose an option:")

                    if user_choice == "1":
                        add_expense(Username)
                    elif user_choice == "2":
                        update_expense(Username)
                    elif user_choice == "3":
                        delete_expense(Username)
                    elif user_choice == "4":
                        print_expenses(Username)
                    elif user_choice == "5":
                        set_budget(Username)
                    elif user_choice == "6":
                        generate_report(Username)
                    elif user_choice == "7":
                        break
                    else:
                        print("Invalid option. Try again.")
        elif choice == "2":
            register()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
                

                        
    

