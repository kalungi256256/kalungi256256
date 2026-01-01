# Meal Price Calculator
# Created by Hyeyendele Rashidi
# Welcome to the Meal Price Calculator!
# This program helps a cashier calculate the total cost of two different meal types,
# including tax and customer change. It's a simple way to practice real-life math
from colorama import Fore, Style, init

init(autoreset=True)

# Prompt for the price of each meal
meal_price1 = float(input(Fore.GREEN + "Enter the price of the first meal: $" + Style.RESET_ALL))
meal_price2 = float(input(Fore.GREEN + "Enter the price of the second meal: $" + Style.RESET_ALL))

# Prompt for how many people order each meal
quantity1 = int(input(Fore.CYAN + "Enter the number of people ordering the first meal: " + Style.RESET_ALL))
quantity2 = int(input(Fore.CYAN + "Enter the number of people ordering the second meal: " + Style.RESET_ALL))

# Prompt for sales tax rate
sales_tax_rate = float(input(Fore.CYAN + "Enter the sales tax rate (as a percentage, e.g., 8 for 8%): " + Style.RESET_ALL))

# Calculate subtotal
subtotal = (meal_price1 * quantity1) + (meal_price2 * quantity2)

# Calculate sales tax amount
sales_tax_amount = subtotal * (sales_tax_rate / 100)

# Calculate total amount
total_amount = subtotal + sales_tax_amount

# Prompt for payment amount
payment_amount = float(input(Fore.YELLOW + "Enter the payment amount: $" + Style.RESET_ALL))

# Calculate change amount
change_amount = payment_amount - total_amount

# Display formatted results
print("\n" + Fore.MAGENTA + "------------------------------")
print("          RECEIPT")
print("------------------------------" + Style.RESET_ALL)
print(Fore.GREEN + f"Subtotal:       ${subtotal:,.2f}" + Style.RESET_ALL)
print(Fore.CYAN + f"Sales Tax:      ${sales_tax_amount:,.2f}" + Style.RESET_ALL)
print(Fore.YELLOW + f"Total Amount:   ${total_amount:,.2f}" + Style.RESET_ALL)
print(Fore.BLUE + f"Payment:        ${payment_amount:,.2f}" + Style.RESET_ALL)
print(Fore.GREEN + f"Change:         ${change_amount:,.2f}" + Style.RESET_ALL)
print(Fore.MAGENTA + "------------------------------" + Style.RESET_ALL)
print(Fore.CYAN + "Thank you for dining with us!")
print(Fore.LIGHTMAGENTA_EX + "Have a great day! 😊" + Style.RESET_ALL)
