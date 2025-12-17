"""Simple meal calculator.

This script prompts the user for child and adult meal prices and counts,
dessert price and quantity, then computes subtotal, sales tax, tip (optional),
and change after payment. Prompts and outputs are kept simple for a CLI.

Inputs:
 - child/adult meal price (float)
 - number of children/adults (int)
 - dessert price per person and count (float/int)
 - sales tax rate (percent as float)
 - tip percentage (percent as float)
 - payment amount (float)

Outputs:
 - prints subtotal, sales tax, total, tip (if any), and change
"""

# Prompt for meal prices and counts
child_meal_price = float(input("What is the price of a child's meal? "))
print()
adult_meal_price = float(input("What is the price of an adult's meal? "))
print()
# Ask the user for the number of children and adults
num_children = int(input("How many children are there? "))
num_adults = int(input("How many adults are there? "))
print()
# Ask user for the dessert price and quantity
dessert_price = float(input("What is the price of desserts per person? "))
num_desserts = int(input("How many desserts to order? "))
print()

# Calculate subtotals for each category
child_subtotal = num_children * child_meal_price
adult_subtotal = num_adults * adult_meal_price
dessert_subtotal = num_desserts * dessert_price
subtotal = child_subtotal + adult_subtotal + dessert_subtotal

# Display the subtotal (formatted to 2 decimal places)
print(f"\nSubtotal: ${subtotal:.2f}")
print()

# Request sales tax information (user supplies a percent, e.g. 7.5)
sales_tax_rate = float(input("What is your sales tax rate (as a percent)? "))
sales_tax = subtotal * sales_tax_rate / 100
total = subtotal + sales_tax

# Display sales tax and total
print(f"Sales tax: ${sales_tax:.2f}")
print(f"Total: ${total:.2f}")

# Tip calculations: if the user enters a tip percentage > 0,
# compute the tip amount and add it to the running total.
tip_percentage = float(input("\nWhat percentage would you like to tip (0 for no tip)? "))
if tip_percentage > 0:
    tip_amount = total * tip_percentage / 100
    total_with_tip = total + tip_amount
    print(f"Tip Amount: ${tip_amount:.2f}")
    print(f"Total with Tip: ${total_with_tip:.2f}")
    total = total_with_tip

# Get payment from the customer and calculate change
payment = float(input("\nWhat is the payment amount? "))
change = payment - total
print(f"Change: ${change:.2f}")
