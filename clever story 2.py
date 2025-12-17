# This program implements a Mad Libs game where the user provides words to fill in a story.
# Added creativity: Included an additional sentence in the story and allowed the user to input more words.

# Prompt the user for inputs

adjective = input("adjective: ").lower()
animal = input("animal: ").lower()
verb1 = input("verb1: ").lower()
exclamation = input("exclamation: ").capitalize().lower() 
 
verb2 = input("verb2: ").lower()
verb3 = input("verb3: ").lower()

# Additional inputs for an extended story
place = input("place: ").lower()
emotion = input("emotion: ").lower()

if animal != "zebra".lower() :
    print ('invalid animal')
else :""    

print("\nYour story is: \n".upper())
print(f"The other day, I was really  trouble. It all started when I saw a very "
	  f" {adjective} {animal} {verb1} down the {place}. {exclamation}! I yelled. But all "
	  f"I could think to do was to {verb2} over and over. {emotion}, "
	  f"that caused it to stop, but not before it tried to {verb3} "
	  f"right in front of my family.")