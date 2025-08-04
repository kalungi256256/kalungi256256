count = 0
average = 0
lowest = 1000
highest = -1
highest_country= ""
lowest_country= ""
lowest_choice_year = 1000
highest_choice_year = -1
i = 0
highest_choice_country= ""
lowest_choice_country=""
highest_choice = -1
lowest_choice = 1000

choice_year = int(input("Enter the year of intrest:  "))

with open("life-expectancy.csv") as file:
    for line in file:
        i = i+1
        newline = line.strip()
        words = newline.split(",")

        if i    > 1:
            country = str(words[0])
            year = int(words[2])
            lifexp = float(words[3])
     
            if lowest > lifexp:
                lowest = lifexp
                lowest_year = year
                lowest_country = country

            if highest < lifexp:
                highest = lifexp
                highest_year = year
                highest_country = country

            if choice_year == year:
                count += 1
                average += lifexp


                if lowest_choice > lifexp:
                    lowest_choice = lifexp
                    lowest_choice_year = year
                    lowest_choice_country = country

                if highest_choice < lifexp:
                    highest_choice = lifexp
                    highest_choice_year = year
                    highest_choice_country = country
print()
print(f"The overall Max Life Expectancy is: { highest} from {highest_country} in { highest_year}")
print(f"The overall Min Life Expectancy is: {lowest} from { lowest_country} in { lowest_year}")

print()
print(f"For the year {choice_year}:")
print(f"The average life expectancy across all countries was: {average/count:.2f}")
print(f"The Max life expectancy was in {highest_choice_country} with  {highest_choice}")
print(f"The Min life expectancy was in {lowest_choice_country} with {lowest_choice}")








            
