#shopping cart
items = []
prices = []

# Game loop
while True:
    #display menu options
    print("\n Please select the following: ")
    print("1. Add item")
    print ("2. Check cart")
    print("3. Remove item")
    print("4.total cost")
    print("5. Quit")

    action = input("What is your choice?: ")

    if action == "1":
        new_item = input("what item would you you like to add?: ")
        item_price = float(input(f" What is the price of ${new_item}?: $"))
    
        items.append(new_item) 
        prices.append(item_price)
        print(f"{new_item} of ${item_price} has been added to cart")

    elif action == "2":
        if not items:
            print('your cart is empty')
        else:
            print("Items in the cart are:")
        for i, items in  enumerate (items, start = 1):
            print(f"{i} .{items} -${prices[i]:.2f}")
    elif action == "3":
        if not items:
            print("Your cart is already empty")
        else:
            print("Select item to remove:")
            for i, item in enumerate(items, start=1):
                print(f"{i}. {item} - ${prices[i-1]:.2f}")
            try:
                index = int(input("Enter the index of the item you want to remove: ")) - 1
                if 0 <= index < len(items):
                    removed_item = items.pop(index)
                    removed_price = prices.pop(index)
                    print(f"{removed_item} has been removed from cart.")
                else:
                    print("Invalid index, Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    elif action == "4":
        total_price = sum(prices)
        print(f"The total price of all items in the cart is: ${total_price:.2f}")

    elif action == "5":
        print("Thank you for using the shopping cart. Goodbye!")
        break

    else:
        print("Invalid action. Please choose a valid option.") 

