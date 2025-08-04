# This is an interactive text adventure game where your choices determine your fate on an alien planet.
# Creativity: I added multiple levels, surprise endings, and let two friends play test it for feedback—they enjoyed the suspense and challenge!

# Set game state.
game_won = False
game_over = False
gt ="try again"
# game intro.
print(
    "\nEMERGENCY TRANSMISSION\n".upper() +
    "Your ship has crashed on a deadly Alien world!"
    " You're the only survivor, The crew is gone...."
    " The wreckage burns around you, and strange movements in the shadows....!\n"
)

print(f"\n welcome to Alien Planet Adventure\n".upper())
print(" Your ship has crushed on an alien planet")
print ("Your the only survivor left on the ship.")
print ("Find the possible way out of the ship before Aliens finds you and get destroyed\n")

print("\nlevel 1\n".upper())
print("\n You wake up hurt and all the crew members are dead")
print("The space ship is broken and on fire")
print (" You need to escape but pain is allover your body")
print()
# The player has three choices to make of either check, Search And sit to go to the next level.
# The player will have to carefully choose in oder to succeed.
choice1 = input("\n Do you want to FIND the aid kit or STAY seated or SHOOT your self?: ").lower()
# choice 1 step 1

if choice1 == "find":
    print("\n You have found the aid box ")
    print("You have successfully found the the aid box and your heathy is restored")
    
elif choice1 == "stay":
    print(" Your healthy got low ").strip()
    print("You are dead")
    print("Game Over")
    print(f"{gt}".capitalize())
    game_over = True
    exit()
elif choice1 == "shoot":
    print("You shot yourself and you are dead")
    print("Game Over")
    print(f"{gt}".capitalize())    
else:
    print("Invalid Choice")
    print(f"{gt}".capitalize())
    exit()
    
choice2 = input("\nDo you want to  CHECK for the door key or SEND the signal to rescue team: ").lower()

    # choice 2 step 2.

if choice2 == "check":
    print("Good work, found the key and the door is unlocked")
    print("You have successfully unlocked the door and you are out of the ship")
    print("The Aliens came in searching but you were already out of the ship")
    print ("\nCongratulations you made it to the next level\n")

elif choice2 == "send":
    print("The team received the signals but  Aliens found you inside and killed you!")
    print ("You are dead")
    print("Game over!")
    print(f"{gt}".capitalize())
    game_over = True
    exit()
    

else:
    print("Invalid choice ")
    print(f"{gt}".capitalize())
    game_over = True
    exit()
    
print("\nlevel 2\n".upper())
#level 2 the player is out of the ship and finds himself in an Alien Zone.
print("\nYou are now out of the ship finding yourself in the middle of the forest")
print("later on realized that the forest is surrounded by Aliens")
print()
print( "Suddenly the communicator batteries get low and you can't communicate to the rescue team")

choice3 = input("\n Do you want to SEARCH for the communicator battery  or STAY hiding?: ").lower()

if choice3 == "search":
    print("\n You head the journey back to crashed ship for the communicator battery")
    print("You have to find the battery to make it  work back on the ship")

elif choice3 == "stay":
    print("The Aliens tracked and found you in your hiding place and killed you!")
    print("You are dead!")
    print("Game over!")
    print(f"{gt}".capitalize())
    game_over = True
    exit()
    
    
else:
    print("invalid choice")
    print(f"{gt}".capitalize())
    exit()
    
#The player goes back to the ship to check for the battery.
# Remember the ship is under the Alien surveillance.
print("\nOn your way back!, Your ambushed by a crew of the Aliens")
# choose to "Run"or "Hand"

choice4 = input("\nTry to RUN and hide first or HAND over yourself  to the Aliens: ").lower()

if choice4 == "run":
    print("You have successfully managed to hide and the  Aliens went a wrong way")
    print("Waiting till dark and proceed the journey back to the space ship")
    print(" Reaching the ship and sneaked inside the ship to get the communicator battery")
    print("\ncongratulations you made it to the next level\n")
elif choice4 == "hand":
    print("The Aliens capture to their territory and get jailed ")
    print("No help to get coz the team doesn't know where you are")
    print ("Game over!")
    print(f"{gt}".capitalize())
    game_over = True
    exit()
else:
    print("invalid option")
    print(f"{gt}".capitalize())
    game_over = True
    exit()
    # Level 3 Rush Hour.
    #level 3 the player is inside the ship again to pick the communicator battery.
    #This is the final stage and the player has to work hard to escape from Alien planet.

print("\nYour are now back to the ship to pick the the battery ")
print("You make it to the storage chamber to pick the battery and surprisingly found an automated machine Gun too!")
print()
choice5 = input("\nDo you want to PICK the gun too or only pick the battery and LEAVE?: ").lower()
# Choose "pick"or "leave".

if choice5=="pick":
    print((
        "\nGreat you picked both the battery and Machine gun, "
        "the communicator beeps to life and the team is on the way. "
        "Aliens from all corridors and bullets are flying everywhere. "
        "You fight your last stand and the team is in place for rescue. "
        "\nCONGRATULATIONS SURVIVOR YOU MADE IT HOME"
    ).upper())
elif choice5 == "leave":
        print("You picked the battery and sent the signals to the team ")
        print("On the way out the Aliens attacked you and since you were defenseless , you were captured")
        print("Game Over!")
        print ("Thank you for playing")
        print(f"{gt}".capitalize())
        game_over = True
        exit()
else:
        print("invalid choice")
        print(f"{gt}".capitalize())
        game_over = True
        exit()

if game_over != True:
    print("You will always be remembered as a Hero")
    print("Game over!Thanks for playing ").strip()