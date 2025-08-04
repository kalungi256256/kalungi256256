def main():
    # Create and print a list named fruit.
    fruit_list = ["pear", "banana", "apple", "mango"]
    print(f"original: {fruit_list}")

    # Reverse and print the list
    fruit_list.reverse()
    print(f"reversed: {fruit_list}")

    # Append "orange" to the end and print
    fruit_list.append("orange")
    print(f"append orange: {fruit_list}")

    # Find "apple" and insert "cherry" before it
    index = fruit_list.index("apple")
    fruit_list.insert(index, "cherry")
    print(f"insert cherry: {fruit_list}")

    # Remove "banana" and print
    fruit_list.remove("banana")
    print(f"remove banana: {fruit_list}")

    # Pop the last element and print both the element and list
    popped = fruit_list.pop()
    print(f"pop {popped}: {fruit_list}")

    # Sort and print the list
    fruit_list.sort()
    print(f"sorted: {fruit_list}")

    # Clear and print the list
    fruit_list.clear()
    print(f"cleared: {fruit_list}")

# Call main to start the program
if __name__ == "__main__":
    main()