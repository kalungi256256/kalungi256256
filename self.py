import math
speed_per_mile = 20.90002
speed_per_minute =100.34343434

def main():
    s = speed_per_mile**2 *3 / speed_per_minute
    t = float(input("what  is the speed per mile: "))
    e = float(input("what is speed per minute: "))
    print(f"{s}+ {t} /{e}")
    return main()