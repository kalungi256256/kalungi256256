# Get basic meal imformation.

child_meal_price = float(input("What is the peice of a child's meal? "))
print()
adult_meal_price = float(input("what is the price of an adult's meal?"))
# Ask the user for the number of chhildren and adults.
print()
num_children = int(input("HOW MANY CHILDREN ARE THERE?"))

num_adults = int(input("How many adults are there? "))
print()
#Ask user for the number and price of dessert.
dessert_price = float (input("Wthat is the price of desserts per person? "))
num_desserts = int(input("How many dessrets to order? "))
print()

#calculate all subtotals to obtain the total
child_subtotal= num_children * child_meal_price
adult_subtotal = num_adults * adult_meal_price
dessert_subtotal =num_desserts * dessert_price
subtotal= child_subtotal + adult_subtotal + dessert_subtotal
  # Display subtotals.
print(f"\nsubtotal: ${subtotal:.2f}")
  # request for  tax imforation
print()
sales_tax_rate = float(input("\n What is your sales tax rate? "))
sales_tax = subtotal *  sales_tax_rate /100
total =subtotal + sales_tax

print(f"sales_tax: ${sales_tax:.2f}"
      f"total: $total: .2f")
# Add Tip calculations.

tip_percentage = float(input("\nWhat percentage would you like to tip (0 for no tip)? "))
if tip_percentage > 0:
    tip_amount = total * tip_percentage / 100
    total_with_tip = total + tip_amount
    print(f"Tip Amount: ${tip_amount:.2f}")
    print(f"Total with Tip: ${total_with_tip:.2f}")
    total = total_with_tip

# Get payment and calculate change
payment = float(input("\nWhat is the payment amount? "))
change = payment - total
print(f"Change: ${change:.2f}")




  
 

















