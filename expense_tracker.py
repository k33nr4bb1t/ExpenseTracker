# useful Link to youtube: https://www.youtube.com/watch?v=HTD86h69PtE&t=1935s

import calendar
from datetime import datetime
from expense import Expense

def main():
    print("👿 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000
    
    # Get user input for expense
    expense = get_user_input()
    # print(expense)
    
    # Write their expenses to a file.
    save_expense_to_file(expense, expense_file_path)
    
    # Read file and summarize expenses.
    summarize_expenses(expense_file_path, budget)
    

def get_user_input():
    print(f"Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    
    
    # Eingabe des Datums
    while True:
        date_string = input("Bitte geben Sie ein Datum im Format 'YYYY-MM-DD' ein: ")
               
        if not date_string:
            date_string = datetime.now().date()
            print("Es wurde kein Datum eingegeben. Verwende das aktuelle Datum:", date_string.strftime("%Y-%m-%d"))
            break
        
        is_valid, date_obj = validate_date(date_string)

        if is_valid:
            print("Eingabe ist ein gültiges Datum:", date_obj)
            break
        else:
            print("Ungültige Datumseingabe. Bitte verwenden Sie das Format 'YYYY-MM-DD'.")

    # print(f"You've entered {expense_name}, {expense_amount}")
    
    expense_categories = [
        "Food", 
        "Home", 
        "Work",
        "Fun",
        "Misc"
    ]
    
    # Eingabe der Category
    
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")
        
        value_range = f"[1 - {len(expense_categories)}]"
        
        ## add an try statement instead of just breaking down the application        
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
        
        if selected_index in range(0, len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount, date=date_string)
            return new_expense
        else:
            print("Invalid category. Please try again!")

def save_expense_to_file(expense:Expense, expense_file_path):
    print(f"Save User Expense: {expense} to File {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category},{expense.date}\n")

def summarize_expenses(expense_file_path, budget):
    print(f"Summarize User Expenses")
    
    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            stripped_line = line.strip()
            expense_name, expense_amount, expense_category, date_string = stripped_line.split(",")
            print(expense_name, expense_amount, expense_category, date_string)
            line_expense = Expense(
                name=expense_name, amount=float(expense_amount), category=expense_category, date=date_string
            )
            # print(line_expense)
            expenses.append(line_expense)
            
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
            
    # print(amount_by_category)
    
    print("Expenses ByCategory:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: {amount:.2f}€")
        
    total_spent = sum([x.amount for x in expenses])
    print(f"You've spent {total_spent}€ this month!")
    
    remaining_budget = budget - total_spent
    print(f"Remaining budget is {remaining_budget:.2f}€ this month!")
    
    # get the current date
    now = datetime.now()
    
    # get the number of days in the current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    
    #Calculate the remaining number of days in the current month
    remaining_days = days_in_month - now.day
    
    # Remaining days in the current month
    print(f"Remaining days in the month: {remaining_days}!")
    
    daily_budget = remaining_budget/remaining_days
    print(green(f"Budget per day is: {daily_budget:.2f}€"))

def green(text):
    return f"\033[92m{text}\033[0m"

def validate_date(date_string):
    try:
        # Versuchen Sie, das Datum in ein datetime-Objekt zu konvertieren
        datetime_obj = datetime.strptime(date_string, "%Y-%m-%d")
        return True, datetime_obj
    except ValueError:
        return False, None

# Dieses Konstrukt sorgt dafür, dass main() nur ausgeführt wird, wenn das Skript nicht importiert wird
if __name__ == "__main__":
    main()