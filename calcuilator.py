# Meal Price Calculator
# Created by Hyeyendele Rashidi
# Welcome to the Meal Price Calculator!
# This program helps a cashier calculate the total cost of two different meal types,
# including tax and customer change. It's a simple way to practice real-life math


# Prompt for the price of each meal
meal_price1 = float(input("Enter the price of the first meal: $"))
meal_price2 = float(input("Enter the price of the second meal: $"))

# Prompt for how many people order each meal
quantity1 = int(input("Enter the number of people ordering the first meal: "))
quantity2 = int(input("Enter the number of people ordering the second meal: "))

# Prompt for sales tax rate
sales_tax_rate = float(input("Enter the sales tax rate (as a percentage, e.g., 8 for 8%): "))

# Calculate subtotal
subtotal = (meal_price1 * quantity1) + (meal_price2 * quantity2)

# Calculate sales tax amount
sales_tax_amount = subtotal * (sales_tax_rate / 100)

# Calculate total amount
total_amount = subtotal + sales_tax_amount

# Prompt for payment amount
payment_amount = float(input("Enter the payment amount: $"))

# Calculate change amount
change_amount = payment_amount - total_amount

# Display formatted results
print("\n------------------------------")
print("          RECEIPT")
print("------------------------------")
print(f"Subtotal:       ${subtotal:,.2f}")
print(f"Sales Tax:      ${sales_tax_amount:,.2f}")
print(f"Total Amount:   ${total_amount:,.2f}")
print(f"Payment:        ${payment_amount:,.2f}")
print(f"Change:         ${change_amount:,.2f}")
print("------------------------------")
print("Thank you for dining with us!")
print("Have a great day! 😊")
