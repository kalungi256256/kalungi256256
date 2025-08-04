# Mad Libs Game 

#Collect words from the user
adjective = input("Enter an adjective: ")
animal = input("Enter an animal: ")
verb1 = input("Enter a verb: ")
exclamation = input("Enter an exclamation: ")
verb2 = input("Enter another verb: ")
verb3 = input("Enter a third verb: ")

#Capitalize the exclamation to start the sentence
exclamation = exclamation.capitalize()

#Create the story using the collected words
print()
print("\nHere's the Mad Libs story:\n")
print()
print(f"The other day, I was really in trouble. It all started when I saw a very")
print(f'{adjective} {animal} {verb1} down the hallway. "{exclamation}!" I yelled. But all \n I could think to do was to {verb2} over and over. Miraculously,')
print("that caused it to stop, but not before it tried to {verb3}")
print("right in front of my family.") 
