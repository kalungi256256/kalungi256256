import random
print("Welcome to a number guessing game baby!")

# Game loop
play_again = "yes"

while play_again == "yes":
    guesses = 0  # Reset guesses for each new game
    print("\nOK now, think of a number between 1 and 100.".upper())
    secret_number = random.randint(1, 100)

    # Guess loop
    while True:
        try:
            guess = int(input("What's your guess?: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        guesses += 1

        if guess == secret_number:
            print("Oh yeah you got it!")
            print(f"Wow, it took you {guesses} guesses.")
            break
        elif guess > secret_number:
            print("Lower")
        else:
            print("Higher")    

    play_again = input("Would you like to play again? (yes/no): ").lower()

print("That was great, see you again!")
