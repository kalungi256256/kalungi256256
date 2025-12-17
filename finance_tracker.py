import csv
import os
import datetime


# Data Management Functions


def load_transactions(filename):
    """Read transaction data from CSV file."""
    transactions = []
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found.")

    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["Amount"] = float(row["Amount"])
            transactions.append(row)
    return transactions


def save_transactions(transactions, filename):
    """Write processed transactions to CSV."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["Date", "Description", "Amount", "Type", "Category"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)



# Data Processing Functions


def calculate_monthly_totals(transactions):

    """Compute monthly income and expense totals."""
    totals = {}

    for t in transactions:
        date = datetime.datetime.strptime(t["Date"], "%Y-%m-%d ")

        month_key = f"{date.year}-{date.month:02d}"

        if month_key not in totals:
            totals[month_key] = {"Income": 0.0, "Expense": 0.0}

        if t["Type"] == "Income":
            totals[month_key]["Income"] += t["Amount"]

        else:
            totals[month_key]["Expense"] += abs(t["Amount"])
    return totals


def generate_category_breakdown(transactions):
    """Calculate spending by category."""
    breakdown = {}
    for t in transactions:
        if t["Type"] == "Expense":
            breakdown[t["Category"]] = breakdown.get(t["Category"], 0) + abs(t["Amount"])
    return breakdown



# Utility Functions


def format_currency(amount):
    """Display monetary amounts consistently."""

    return f"${amount:,.2f}"



# Main Program


def main():
    filename = "transactions.csv"
    transactions = load_transactions(filename)

    # Calculate totals
    monthly_totals = calculate_monthly_totals(transactions)

    total_income = sum(month["Income"] for month in monthly_totals.values())

    total_expenses = sum(month["Expense"] for month in monthly_totals.values())

    total_savings = total_income - total_expenses

    # Most expensive transaction
    expenses_only = [t for t in transactions if t["Type"] == "Expense"]

    most_expensive = max(expenses_only, key=lambda x: abs(x["Amount"])) if expenses_only else None

    # Top spending category
    category_totals = generate_category_breakdown(transactions)

    top_category = max(category_totals.items(), key=lambda x: x[1]) if category_totals else None

    # Print summary
    print("\n==== Personal Finance Summary ====")

    print(f"Total Income:   {format_currency(total_income)}")
    
    print(f"Total Expenses: {format_currency(total_expenses)}")

    print(f"Total Savings:  {format_currency(total_savings)}")

    if most_expensive:
        print(f"Most Expensive Transaction: {most_expensive['Description']} "
              
              f"({format_currency(abs(most_expensive['Amount']))})")

    if top_category:
        print(f"Top Spending Category: {top_category[0]} "
              
              f"({format_currency(top_category[1])})")

    print("🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙🪙\n")


if __name__ == "__main__":
    main()
