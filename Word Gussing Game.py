
# This is a simple word guessing game where the player has to guess a secret word.
#creativity features are random selection of words and maximum number of guesses allowed.
import random
# Game state.
word_list =["mosiah", "Jonisha", "joseph", "nephi", "alma", "mormon", "lehi", "ether", "moroni", "jacob"]
secret_word = random.choice(word_list)
max_guesses = 6 # Maximum number of guesses allowed
guess_count = 0
game_over = False

# Welcoming message.
print("Welcome to a word guessing Game")
print(f"\nYour hint is: {len(secret_word)} letters.")

# Main game loop
while not game_over:
    print("Your hint is: _ _ _ _ _ _ ")  # Displaying the hint as underscores
    guess = input("What is your guess?: ").lower()
    guess_count += 1

    # Check if guess has the correct length
    if len(guess) != len(secret_word):
        print(f"Sorry, the guess must have {len(secret_word)} letters.")
        continue

    # Check whether the guess is correct
    if guess == secret_word:
        game_over = True
        print("Congratulations you made it!")
        print(f"Wow, it only took you {guess_count} guesses.")
        break
        Exit()

    # Hint part
    hint = []
    for i in range(len(secret_word)):
        if guess[i] == secret_word[i]:
            hint.append(guess[i].upper())
        elif guess[i] in secret_word:
            hint.append(guess[i].lower())
        else:
            hint.append("_")
    print(f"Your hint is: {''.join(hint)}")