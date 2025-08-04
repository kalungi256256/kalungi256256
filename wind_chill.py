def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32

def calculate_wind_chill(temp_f, wind_speed):
    """Calculate the wind chill based on temp in Fahrenheit and wind speed in mph."""
    return 35.74 + 0.6215 * temp_f - 35.75 * wind_speed**0.16 + 0.4275 * temp_f * wind_speed**0.16

# Get temperature input from the user
temp = float(input("What is the temperature? "))
scale = input("Fahrenheit or Celsius (F/C)? ").strip().upper()

# Convert to Fahrenheit if needed
if scale == "C":
    temp_f = celsius_to_fahrenheit(temp)
else:
    temp_f = temp

# Loop through wind speeds from 5 to 60 (inclusive), incrementing by 5
for wind_speed in range(5, 61, 5):
    wind_chill = calculate_wind_chill(temp_f, wind_speed)
    print(f"At temperature {temp_f:.1f}F, and wind speed {wind_speed} mph, the windchill is: {wind_chill:.2f}F")
