# this program exceeds requirements by:
# 1. using constants for earth's gravity, water density, and viscosity
# 2. including a function that converts kilopascals to pounds per square inch (psi)
# 3. intended to be used with a test function that verifies the kpa-to-psi conversion

# constants for physical properties of water and gravity
earth_acceleration_of_gravity = 9.80665      
water_density = 998.2                        
water_dynamic_viscosity = 0.0010016          

# calculates the effective height of the water column
def water_column_height(tower_height, tank_height):
    return tower_height + (3 * tank_height / 4)

# calculates pressure gain from the height of the water column
def pressure_gain_from_water_height(height):
    return water_density * earth_acceleration_of_gravity * height / 1000

# calculates pressure loss due to pipe friction
def pressure_loss_from_pipe(pipe_diameter, pipe_length, friction_factor, fluid_velocity):
    return -friction_factor * pipe_length * water_density * fluid_velocity**2 / (2000 * pipe_diameter)

# calculates pressure loss due to pipe fittings (e.g., elbows)
def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    return -0.04 * water_density * fluid_velocity**2 * quantity_fittings / 2000

# calculates reynolds number to determine flow type
def reynolds_number(hydraulic_diameter, fluid_velocity):
    return water_density * hydraulic_diameter * fluid_velocity / water_dynamic_viscosity

# calculates pressure loss from a pipe diameter reduction
def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    if reynolds_number == 0:
        return 0.0  
    k = 0.1 + (50 / reynolds_number) * (((larger_diameter / smaller_diameter) ** 4) - 1)
    return -k * water_density * fluid_velocity ** 2 / 2000

# converts pressure from kilopascals to pounds per square inch
def kpa_to_psi(kpa):
    return kpa * 0.145038

# main program function
def main():
    
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    pipe_length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    fittings = int(input("Number of 90° angles in supply pipe: "))
    pipe_length2 = float(input("Length of pipe from supply to house (meters): "))

    # system parameters (assumed values)
    pipe_diameter1 = 0.28687     
    pipe_diameter2 = 0.048692    
    fluid_velocity = 1.75        
    friction_factor = 0.013     

    # compute water pressure step-by-step
    h = water_column_height(tower_height, tank_height)
    pressure1 = pressure_gain_from_water_height(h)

    loss1 = pressure_loss_from_pipe(pipe_diameter1, pipe_length1, friction_factor, fluid_velocity)
    loss2 = pressure_loss_from_fittings(fluid_velocity, fittings)
    re = reynolds_number(pipe_diameter1, fluid_velocity)
    loss3 = pressure_loss_from_pipe_reduction(pipe_diameter1, fluid_velocity, re, pipe_diameter2)
    loss4 = pressure_loss_from_pipe(pipe_diameter2, pipe_length2, friction_factor, fluid_velocity)

    # total pressure at the house
    pressure_at_house = pressure1 + loss1 + loss2 + loss3 + loss4

    # display the result in kpa and psi
    print(f"Pressure at house: {pressure_at_house:.1f} kilopascals")
    print(f"Pressure at house: {kpa_to_psi(pressure_at_house):.1f} psi")

# run the program
if __name__ == "__main__":
    main()
