# Meal Price Calculator

# Ask for the price of a child's meal
child_meal_price = float(input("What is the price of a child's meal? "))

# Ask for the price of an adult's meal
adult_meal_price = float(input("What is the price of an adult's meal? "))

# Ask for the number of children
num_children = int(input("How many children are there? "))

# Ask for the number of adults
num_adults = int(input("How many adults are there? "))

# Calculate subtotal
subtotal = (child_meal_price * num_children) + (adult_meal_price * num_adults)
print("\nSubtotal: ${:.2f}\n".format(subtotal))

# Ask for the sales tax rate
sales_tax_rate = float(input("What is the sales tax rate? "))

# Calculate sales tax
sales_tax = (subtotal * sales_tax_rate) / 100
print("Sales Tax: ${:.2f}".format(sales_tax))

# Calculate total
total = subtotal + sales_tax
print("Total: ${:.2f}\n".format(total))

# Ask for the payment amount
payment_amount = float(input("What is the payment amount? "))

# Calculate change
change = payment_amount - total
print("Change: ${:.2f}".format(change))

def child_meal(child_num, child_meal_price):
    total = child_num * child_meal_price
    return total

def adult_meal(adult_num, adult_meal_price):
    total = adult_num * adult_meal_price
    return total

def sub_total(child_total,adult_total):
    total_sub = child_total + adult_total
    return total_sub

def main():
    child_meal_price = float(input("What is the price of a child's meal? "))
    adult_meal_price = float(input("What is the price of an adult's meal? "))
    num_children = int(input("How many children are there? "))
    num_adults = int(input("How many adults are there? "))

    child_total = child_meal(num_children,child_meal_price)
    adult_total = adult_meal(num_adults,adult_meal_price)
    total_sub = sub_total(child_total,adult_total)
    print(f"${total_sub:.2f}")
    
if __name__"__main__:



