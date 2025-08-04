#Additionals: Added a customer loyalty discount system that gives 5% off orders over $20
#Also added item count validation and improved error messaging for better user experience

import csv
from datetime import datetime, timedelta

def read_dictionary(filename, key_column_index):
    """
    Reads the product data from the csv file passed to the function in the filename parameter.
    The dictionary key is contained in the csv data column indicated by the key_column_index parameter.
    The value of each dictionary item is the list derived from the values in the row of the csv file.
    Returns a dictionary of products.
    """
    products_dict = {}
    
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            
            # Skip the header row if it exists
            next(reader, None)
            
            for row in reader:
                if len(row) > key_column_index:
                    key = row[key_column_index]
                    products_dict[key] = row
                    
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find the file: {filename}")
    except PermissionError:
        raise PermissionError(f"Permission denied when trying to read: {filename}")
    
    return products_dict

def main():
    """
    Reads the request.csv file, processes the file and displays the receipt 
    according to the user requirements.
    """
    
    try:
        # products  from products.csv
        products_dict = read_dictionary("products.csv", 0)
        
        #  receipt variables
        store_name = "Kal Valley Market UG"
        total_items = 0
        subtotal = 0.0
        sales_tax_rate = 0.06
        ordered_items = []
        
        print(store_name)
        print()
        
        # Read and process the customer's order from request.csv
        with open("request.csv", 'r', newline='') as request_file:
            reader = csv.reader(request_file)
            
            # Skip the header row
            next(reader, None)
            
            # Process each item in the order
            for row in reader:
                if len(row) >= 2:
                    product_id = row[0]
                    quantity = int(row[1])
                    
                    # Look For the product in the catalog
                    if product_id in products_dict:
                        product_info = products_dict[product_id]
                        product_name = product_info[1]
                        price_per_item = float(product_info[2])
                        
                        # Store item information for receipt
                        ordered_items.append({
                            'name': product_name,
                            'quantity': quantity,
                            'price': price_per_item
                        })
                        
                        # Print the item line
                        print(f"{product_name}: {quantity} @ {price_per_item:.2f}")
                        
                        # Update totals
                        total_items += quantity
                        subtotal += quantity * price_per_item
                    else:
                        raise KeyError(f"Unknown product ID in the request.csv file: '{product_id}'")
        
        print()
        
        # Enhancement: Customer loyalty discount for orders over $20
        loyalty_discount = 0.0
        if subtotal > 20.0:
            loyalty_discount = subtotal * 0.05
            print(f"Loyalty Discount (5% off orders over $20): -{loyalty_discount:.2f}")
            subtotal -= loyalty_discount
        
        # Calculate and display totals
        print(f"Number of Items: {total_items}")
        print(f"Subtotal: {subtotal:.2f}")
        
        sales_tax = subtotal * sales_tax_rate
        print(f"Sales Tax: {sales_tax:.2f}")
        
        total = subtotal + sales_tax
        print(f"Total: {total:.2f}")
        
        print()
        print(f"Thank you for shopping at the {store_name}.")
        
        # Print current date and time
        current_time = datetime.now()
        print(current_time.strftime("%a %b %d %H:%M:%S %Y"))
        
        # Enhancement: Return policy reminder
        return_date = current_time + timedelta(days=30)
        return_date = return_date.replace(hour=21, minute=0, second=0, microsecond=0)
        print(f"Return by: {return_date.strftime('%a %b %d %I:%M %p %Y')}")
        
        # Enhancement: Days until New Year's Sale
        current_year = current_time.year
        new_year = datetime(current_year + 1, 1, 1)
        days_until_new_year = (new_year - current_time).days
        print(f"New Year's Sale begins in {days_until_new_year} days!")
        
    except FileNotFoundError as error:
        print("Error: missing file")
        print(error)
        
    except PermissionError as error:
        print("Error: permission denied")
        print(error)
        
    except KeyError as error:
        print("Error: unknown product ID in the request.csv file")
        print(error)
        
    except ValueError as error:
        print("Error: invalid data format in CSV file")
        print(error)
        
    except Exception as error:
        print("Error: an unexpected error occurred")
        print(error)


if __name__ == "__main__":
    main()