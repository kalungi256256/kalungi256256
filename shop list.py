# Initialize lists to store items and prices
items = []
prices = []

# Main program loop
while True:
    print("nPlease select one of the following:")
    print("1. Add item")
    print("2. View cart")
    print("3. Remove item")
    print("4. Compute total")
    print("5. Quit")

    action = input("Please enter an action: ")

    if action == "1":
        new_item = input("What item would you like to add? ")
        item_price = float(input(f"What is the price of '{new_item}'? $"))  # Prompt for the price
        items.append(new_item)
        prices.append(item_price)
        print(f"'{new_item}' has been added to the cart.")

    elif action == "2":
        if not items:
            print("Your cart is empty.")
        else:
            print("The contents of the shopping cart are:")
            for i, item in enumerate(items, start=1):
                print(f"{i}. {item} - ${prices[i-1]:.2f}")

    elif action == "3":
        if not items:
            print("Your cart is already empty.")
        else:
            print("Select the item to remove:")
            for i, item in enumerate(items, start=1):
                print(f"{i}. {item} - ${prices[i-1]:.2f}")
            index = int(input("Enter the index of the item to remove: ")) - 1
            if 0 <= index < len(items):
                removed_item = items.pop(index)
                removed_price = prices.pop(index)
                print(f"'{removed_item}' has been removed from the cart.")
            else:
                print("Invalid index. Please try again.")

    elif action == "4":
        total_price = sum(prices)
        print(f"The total price of all items in the cart is: ${total_price:.2f}")

    elif action == "5":
        print("Thank you for using the shopping cart. Goodbye!")
        break

    else:
        print("Invalid action. Please choose a valid option.")

