"""
Adventure Game: The Lost Temple
I added a scoring system that tracks your performance and multiple Easter egg endings for high scores.
I showed this to my roommate and sister who loved competing to discover all the different endings!
"""

print("\n" + "="*50)
print("          THE LOST TEMPLE ADVENTURE")
print("="*50)
print("You stand before the entrance of an ancient temple.")
print("Legends say it holds great treasures but also great dangers.")
print("Your choices will determine your fate...")

score = 0
level = 1

# Level 1: Entrance Choice
print(f"\n--- Level {level}: The Entrance ---")
print("Before you are three mysterious doorways:")
print("A shimmering GOLD door, a sturdy STONE door, and a hidden PASSAGE behind vines.")

choice1 = input("Which do you choose? (GOLD/STONE/PASSAGE): ").strip().upper()

if choice1 == "GOLD":
    score += 10
    level += 1
    print(f"\nYou push open the heavy GOLD door. It creaks loudly!")
    print("Inside, you find a room filled with glittering treasures.")
    
    # Level 2: Gold Room
    print(f"\n--- Level {level}: Treasure Room ---")
    print("In the center sits a magnificent DIAMOND on a pedestal.")
    print("To the left, ancient COINS spill from a chest.")
    print("On the right wall, you notice a mysterious SYMBOL.")
    print("Behind you, the door remains OPEN.")
    
    choice2 = input("What do you investigate? (DIAMOND/COINS/SYMBOL/LEAVE): ").strip().upper()
    
    if choice2 == "DIAMOND":
        score += 20
        level += 1
        print(f"\nAs you reach for the DIAMOND, the floor trembles!")
        print("A hidden mechanism activates...")
        
        # Level 3: Diamond Trap
        print(f"\n--- Level {level}: The Trap ---")
        print("Spikes shoot from the walls! You have seconds to react.")
        print("You can DODGE left, JUMP back, or GRAB the diamond and RUN.")
        
        choice3 = input("What's your move? (DODGE/JUMP/GRAB): ").strip().upper()
        
        if choice3 == "DODGE":
            score += 30
            print("\nYou expertly dodge the spikes and slip through a hidden exit!")
            print("You escape with your life but no treasure. A cautious adventurer survives!")
            ending = "Safe Escape"
        elif choice3 == "JUMP":
            score += 40
            print("\nYou leap backward as the spikes retract suddenly.")
            print("The diamond was a decoy! The real treasure was the COINS all along.")
            print("You fill your pockets and escape wealthy!")
            ending = "Wealthy Explorer"
        elif choice3 == "GRAB":
            score += 50
            print("\nYou snatch the diamond and sprint as the room collapses behind you!")
            print("You emerge with the legendary treasure - the adventure of a lifetime!")
            ending = "Legendary Hero"
        else:
            print("\nYour hesitation costs you! The spikes find their mark.")
            print("Game Over - more decisive action was needed.")
            ending = "Indecisive Demise"
            
    elif choice2 == "COINS":
        score += 15
        level += 1
        print(f"\nYou scoop up handfuls of ancient COINS.")
        print("Suddenly, you hear grinding stone behind you...")
        
        # Level 3: Coin Room
        print(f"\n--- Level {level}: Guard's Wrath ---")
        print("A stone guardian awakens! It blocks your exit.")
        print("You can FIGHT with a nearby sword, BRIBE it with coins, or look for an ESCAPE route.")
        
        choice3 = input("How do you respond? (FIGHT/BRIBE/ESCAPE): ").strip().upper()
        
        if choice3 == "FIGHT":
            score += 25
            print("\nYou bravely fight the guardian! After a fierce battle, it crumbles to dust.")
            print("You escape with coins and honor!")
            ending = "Valiant Warrior"
        elif choice3 == "BRIBE":
            score += 35
            print("\nYou offer the guardian a handful of coins. It examines them curiously.")
            print("The guardian steps aside and even points you toward a secret exit with more treasure!")
            ending = "Diplomatic Treasure Hunter"
        elif choice3 == "ESCAPE":
            score += 20
            print("\nYou spot a small crack in the wall and squeeze through.")
            print("You escape with some coins but leave most behind.")
            ending = "Cautious Survivor"
        else:
            print("\nThe guardian doesn't understand your actions and attacks!")
            print("Game Over - clear choices lead to better outcomes.")
            ending = "Confused Adventurer"
            
    elif choice2 == "SYMBOL":
        score += 25
        level += 1
        print(f"\nThe SYMBOL glows as you touch it! A secret passage opens.")
        print("You enter a library filled with ancient knowledge.")
        
        # Level 3: Library
        print(f"\n--- Level {level}: Hall of Knowledge ---")
        print("You see three ancient TOMES, a glowing ORB, and a MAP of the temple.")
        
        choice3 = input("What do you study? (TOMES/ORB/MAP): ").strip().upper()
        
        if choice3 == "TOMES":
            score += 45
            print("\nThe tomes contain forgotten magic! You learn spells of protection and wealth.")
            print("You become the most knowledgeable wizard in the land!")
            ending = "Archmage"
        elif choice3 == "ORB":
            score += 35
            print("\nThe orb shows you visions of the temple's construction.")
            print("You discover the location of the true royal treasure chamber!")
            ending = "Visionary Explorer"
        elif choice3 == "MAP":
            score += 30
            print("\nThe map reveals all the temple's secrets and safe passages.")
            print("You navigate safely to the greatest treasures and escape unharmed!")
            ending = "Master Navigator"
        else:
            print("\nWhile you hesitate, the secret door closes behind you.")
            print("Trapped forever in the library - at least you have good reading material!")
            ending = "Eternal Scholar"
            
    elif choice2 == "LEAVE":
        score += 5
        print("\nYou wisely leave the tempting treasures behind.")
        print("Sometimes the greatest treasure is your own life.")
        ending = "Wise Retreat"
        
    else:
        print("\nYour confusion in the treasure room attracts cursed spirits!")
        print("Game Over - the temple rewards decisive adventurers.")
        ending = "Cursed by Indecision"
        
elif choice1 == "STONE":
    score += 5
    level += 1
    print(f"\nThe STONE door is heavy but yields to your push.")
    print("You enter a dim corridor that slopes downward.")
    
    # Level 2: Stone Corridor
    print(f"\n--- Level {level}: Ancient Corridor ---")
    print("The corridor splits three ways:")
    print("A brightly lit path to the LEFT with strange noises.")
    print("A dark, quiet path to the RIGHT that smells of earth.")
    print("A ladder leading DOWN into darkness.")
    
    choice2 = input("Which path? (LEFT/RIGHT/DOWN): ").strip().upper()
    
    if choice2 == "LEFT":
        score += 15
        level += 1
        print(f"\nYou follow the LEFT path into a chamber with glowing crystals.")
        print("The crystals pulse with energy and form patterns on the walls.")
        
        # Level 3: Crystal Chamber
        print(f"\n--- Level {level}: Crystal Nexus ---")
        print("The patterns seem to tell a story. You can:")
        print("TOUCH the largest crystal, STUDY the patterns, or FOLLOW the light beam.")
        
        choice3 = input("What action do you take? (TOUCH/STUDY/FOLLOW): ").strip().upper()
        
        if choice3 == "TOUCH":
            score += 40
            print("\nEnergy flows through you! The crystals recognize you as worthy.")
            print("They grant you ancient knowledge and a piece of the crystal itself!")
            ending = "Crystal Sage"
        elif choice3 == "STUDY":
            score += 30
            print("\nYou decipher the patterns - they're a star map!")
            print("This discovery will revolutionize astronomy!")
            ending = "Celestial Scholar"
        elif choice3 == "FOLLOW":
            score += 25
            print("\nThe light beam leads to a hidden chamber filled with crystal artifacts!")
            print("You collect rare specimens that scholars will study for generations.")
            ending = "Artifact Collector"
        else:
            print("\nThe crystals react to your uncertainty and dim.")
            print("The chamber darkens, leaving you lost in the temple.")
            ending = "Lost in Darkness"
            
    elif choice2 == "RIGHT":
        score += 10
        level += 1
        print(f"\nThe RIGHT path leads to an underground garden.")
        print("Bioluminescent plants illuminate strange flora and fauna.")
        
        # Level 3: Underground Garden
        print(f"\n--- Level {level}: Sunless Garden ---")
        print("You see: GLOWING flowers, a still POOL, and strange FRUIT on vines.")
        
        choice3 = input("What do you investigate? (FLOWERS/POOL/FRUIT): ").strip().upper()
        
        if choice3 == "FLOWERS":
            score += 35
            print("\nThe flowers release a pollen that grants you visions!")
            print("You see the future and return to guide humanity to prosperity!")
            ending = "Prophetic Gardener"
        elif choice3 == "POOL":
            score += 30
            print("\nThe pool's water has miraculous healing properties!")
            print("You bring samples back that revolutionize medicine!")
            ending = "Healing Discoverer"
        elif choice3 == "FRUIT":
            score += 20
            print("\nThe fruit is delicious and grants you enhanced strength!")
            print("You become a legendary hero with your new abilities!")
            ending = "Enhanced Champion"
        else:
            print("\nYou wander aimlessly until the garden's magic confuses you.")
            print("You become a permanent resident of the sunless garden.")
            ending = "Eternal Gardener"
            
    elif choice2 == "DOWN":
        score += 20
        level += 1
        print(f"\nYou climb DOWN into a vast cavern.")
        print("Ancient machinery hums with power - this is the temple's heart!")
        
        # Level 3: Temple Core
        print(f"\n--- Level {level}: The Temple's Heart ---")
        print("Massive gears turn around a central CONTROL panel.")
        print("You can: ACTIVATE the machinery, SHUT it down, or STUDY the mechanisms.")
        
        choice3 = input("What do you do? (ACTIVATE/SHUT/STUDY): ").strip().upper()
        
        if choice3 == "ACTIVATE":
            score += 50
            print("\nThe temple awakens fully! It recognizes you as its new master!")
            print("You command an ancient power that shapes the world!")
            ending = "Temple Master"
        elif choice3 == "SHUT":
            score += 40
            print("\nYou safely shut down the ancient machinery.")
            print("The temple settles into peaceful dormancy - a danger averted!")
            ending = "Prudent Guardian"
        elif choice3 == "STUDY":
            score += 45
            print("\nYou understand the temple's workings and make careful notes.")
            print("Your research advances technology by centuries!")
            ending = "Mechanical Genius"
        else:
            print("\nYour confusion causes a systems malfunction!")
            print("The temple begins to collapse around you!")
            ending = "System Failure"
            
    else:
        print("\nYou hesitate at the crossroads until the corridor ceiling collapses.")
        print("Game Over - sometimes you must choose a path to move forward.")
        ending = "Crushed by Indecision"
        
elif choice1 == "PASSAGE":
    score += 15
    level += 1
    print(f"\nYou squeeze through the hidden PASSAGE behind the vines.")
    print("It leads to the temple's living quarters, untouched for centuries.")
    
    # Level 2: Living Quarters
    print(f"\n--- Level {level}: Ancient Living Quarters ---")
    print("You find personal artifacts of the temple builders:")
    print("A JOURNAL on a desk, a collection of TOOLS, and a family SHRINE.")
    
    choice2 = input("What do you examine? (JOURNAL/TOOLS/SHRINE): ").strip().upper()
    
    if choice2 == "JOURNAL":
        score += 25
        level += 1
        print(f"\nThe JOURNAL contains the temple builders' final words.")
        print("They speak of a great purpose for the temple...")
        
        # Level 3: Journal Revelations
        print(f"\n--- Level {level}: The Truth ---")
        print("The journal reveals the temple was built to preserve knowledge")
        print("during an approaching cataclysm. You can:")
        print("PRESERVE the knowledge, USE the temple's power, or WARN everyone.")
        
        choice3 = input("What is your choice? (PRESERVE/USE/WARN): ").strip().upper()
        
        if choice3 == "PRESERVE":
            score += 45
            print("\nYou dedicate your life to preserving and expanding the knowledge.")
            print("You become the temple's new guardian for future generations!")
            ending = "Knowledge Guardian"
        elif choice3 == "USE":
            score += 35
            print("\nYou use the temple's power to prevent the coming disaster!")
            print("You save countless lives and are hailed as a savior!")
            ending = "Humanity's Savior"
        elif choice3 == "WARN":
            score += 40
            print("\nYou spread the warning and the world prepares successfully!")
            print("The disaster is mitigated thanks to your efforts!")
            ending = "Harbinger of Preparation"
        else:
            print("\nUnable to decide, you do nothing as the predicted disaster arrives.")
            print("The temple becomes your tomb as the world changes outside.")
            ending = "Failed Messenger"
            
    elif choice2 == "TOOLS":
        score += 20
        level += 1
        print(f"\nThe TOOLS are made of unknown metals that never rust.")
        print("They seem to have special properties...")
        
        # Level 3: Ancient Tools
        print(f"\n--- Level {level}: Master Crafters ---")
        print("With these tools, you could: BUILD new devices, REPAIR the temple, or LEARN their secrets.")
        
        choice3 = input("How will you use them? (BUILD/REPAIR/LEARN): ").strip().upper()
        
        if choice3 == "BUILD":
            score += 40
            print("\nYou create inventions that revolutionize technology!")
            print("Your name is remembered among the great inventors!")
            ending = "Visionary Inventor"
        elif choice3 == "REPAIR":
            score += 35
            print("\nYou restore the temple to its original glory!")
            print("It becomes a center of learning and wonder for all!")
            ending = "Temple Restorer"
        elif choice3 == "LEARN":
            score += 30
            print("\nYou discover the secret of the eternal metals!")
            print("Your findings change material science forever!")
            ending = "Materials Master"
        else:
            print("\nThe tools remain mysterious as you fail to understand their purpose.")
            print("A great opportunity wasted through uncertainty.")
            ending = "Missed Opportunity"
            
    elif choice2 == "SHRINE":
        score += 30
        level += 1
        print(f"\nThe SHRINE radiates peaceful energy.")
        print("You feel a connection to the temple builders' spirits.")
        
        # Level 3: Spiritual Connection
        print(f"\n--- Level {level}: Beyond the Veil ---")
        print("The spirits offer guidance. You can:")
        print("COMMUNE with them, seek their BLESSING, or learn their WISDOM.")
        
        choice3 = input("What do you seek? (COMMUNE/BLESSING/WISDOM): ").strip().upper()
        
        if choice3 == "COMMUNE":
            score += 50
            print("\nYou join the spirits in their eternal vigil!")
            print("You become a guardian spirit of the temple forever!")
            ending = "Eternal Guardian"
        elif choice3 == "BLESSING":
            score += 45
            print("\nThe spirits bless you with protection and insight!")
            print("You live an extraordinary life helping others!")
            ending = "Blessed Soul"
        elif choice3 == "WISDOM":
            score += 40
            print("\nThe spirits share ancient wisdom that transforms your understanding!")
            print("You become the wisest person of your age!")
            ending = "Enlightened Sage"
        else:
            print("\nThe spirits fade away, disappointed by your lack of purpose.")
            print("You leave with only vague memories of the encounter.")
            ending = "Unfulfilled Seeker"
            
    else:
        print("\nYou spend so long deciding that you run out of supplies.")
        print("Game Over - even explorers need to make timely choices.")
        ending = "Starved by Indecision"
        
else:
    print("\nYou cannot decide which entrance to take.")
    print("As night falls, wild animals find you still pondering at the temple entrance.")
    print("Game Over - adventure requires action!")
    ending = "Timid Soul"
    

# Final scoring and results
print("\n" + "="*50)
print("            ADVENTURE COMPLETE!")
print("="*50)
print(f"Your ending: {ending}")
print(f"Final Score: {score} points")
print(f"Levels completed: {level-1}")

# Bonus Easter egg for high scores
if score >= 100:
    print("\n*** LEGENDARY ACHIEVEMENT: Temple Master ***")
    print("You have proven yourself worthy of the temple's greatest secrets!")
elif score >= 70:
    print("\n*** GREAT SUCCESS: Seasoned Explorer ***")
    print("The temple has yielded many of its wonders to you!")
elif score >= 40:
    print("\n*** GOOD EFFORT: Brave Adventurer ***")
    print("You've explored well and learned much from the temple!")
else:
    print("\n*** NOBLE ATTEMPT: Curious Visitor ***")
    print("The temple remains mysterious, but you survived to tell the tale!")

print("\nThank you for playing THE LOST 🛕TEMPLE ADVENTURE!")
