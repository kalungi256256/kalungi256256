#Added a chemica formular name lookup and proton counting fuction.
#and it can identify comon chemical compounds and calculate total protons in molecules.

from formula import parse_formula

def make_periodic_table():
    """
    Returns a dictionary object which contains all of the elements of the periodic table.
    For each element the dictionary key is the element's symbol.
    The value contains a list where the first item is the element's name and the second item is the atomic mass.
    """
 #simbols
    periodic_table_dict = {
        
        "Ac": ["Actinium", 227],
        "Ag": ["Silver", 107.8682],
        "Al": ["Aluminum", 26.9815386],
        "Am": ["Americium", 243],
        "Ar": ["Argon", 39.948],
        "As": ["Arsenic", 74.9216],
        "At": ["Astatine", 210],
        "Au": ["Gold", 196.966569],
        "B": ["Boron", 10.811],
        "Ba": ["Barium", 137.327],
        "Be": ["Beryllium", 9.012182],
        "Bh": ["Bohrium", 272],
        "Bi": ["Bismuth", 208.98040],
        "Bk": ["Berkelium", 247],
        "Br": ["Bromine", 79.904],
        "C": ["Carbon", 12.0107],
        "Ca": ["Calcium", 40.078],
        "Cd": ["Cadmium", 112.411],
        "Ce": ["Cerium", 140.116],
        "Cf": ["Californium", 251],
        "Cl": ["Chlorine", 35.453],
        "Cm": ["Curium", 247],
        "Cn": ["Copernicium", 285],
        "Co": ["Cobalt", 58.933195],
        "Cr": ["Chromium", 51.9961],
        "Cs": ["Cesium", 132.9054519],
        "Cu": ["Copper", 63.546],
        "Db": ["Dubnium", 268],
        "Ds": ["Darmstadtium", 281],
        "Dy": ["Dysprosium", 162.500],
        "Er": ["Erbium", 167.259],
        "Es": ["Einsteinium", 252],
        "Eu": ["Europium", 151.964],
        "F": ["Fluorine", 18.9984032],
        "Fe": ["Iron", 55.845],
        "Fl": ["Flerovium", 289],
        "Fm": ["Fermium", 257],
        "Fr": ["Francium", 223],
        "Ga": ["Gallium", 69.723],
        "Gd": ["Gadolinium", 157.25],
        "Ge": ["Germanium", 72.64],
        "H": ["Hydrogen", 1.00794],
        "He": ["Helium", 4.002602],
        "Hf": ["Hafnium", 178.49],
        "Hg": ["Mercury", 200.59],
        "Ho": ["Holmium", 164.93032],
        "Hs": ["Hassium", 277],
        "I": ["Iodine", 126.90447],
        "In": ["Indium", 114.818],
        "Ir": ["Iridium", 192.217],
        "K": ["Potassium", 39.0983],
        "Kr": ["Krypton", 83.798],
        "La": ["Lanthanum", 138.90547],
        "Li": ["Lithium", 6.941],
        "Lr": ["Lawrencium", 262],
        "Lu": ["Lutetium", 174.9668],
        "Lv": ["Livermorium", 293],
        "Mc": ["Moscovium", 290],
        "Md": ["Mendelevium", 258],
        "Mg": ["Magnesium", 24.3050],
        "Mn": ["Manganese", 54.938045],
        "Mo": ["Molybdenum", 95.96],
        "Mt": ["Meitnerium", 276],
        "N": ["Nitrogen", 14.0067],
        "Na": ["Sodium", 22.98976928],
        "Nb": ["Niobium", 92.90638],
        "Nd": ["Neodymium", 144.242],
        "Ne": ["Neon", 20.1797],
        "Nh": ["Nihonium", 286],
        "Ni": ["Nickel", 58.6934],
        "No": ["Nobelium", 259],
        "Np": ["Neptunium", 237],
        "O": ["Oxygen", 15.9994],
        "Og": ["Oganesson", 294],
        "Os": ["Osmium", 190.23],
        "P": ["Phosphorus", 30.973762],
        "Pa": ["Protactinium", 231.03588],
        "Pb": ["Lead", 207.2],
        "Pd": ["Palladium", 106.42],
        "Pm": ["Promethium", 145],
        "Po": ["Polonium", 209],
        "Pr": ["Praseodymium", 140.90765],
        "Pt": ["Platinum", 195.084],
        "Pu": ["Plutonium", 244],
        "Ra": ["Radium", 226],
        "Rb": ["Rubidium", 85.4678],
        "Re": ["Rhenium", 186.207],
        "Rf": ["Rutherfordium", 267],
        "Rg": ["Roentgenium", 280],
        "Rh": ["Rhodium", 102.90550],
        "Rn": ["Radon", 222],
        "Ru": ["Ruthenium", 101.07],
        "S": ["Sulfur", 32.065],
        "Sb": ["Antimony", 121.760],
        "Sc": ["Scandium", 44.955912],
        "Se": ["Selenium", 78.96],
        "Sg": ["Seaborgium", 271],
        "Si": ["Silicon", 28.0855],
        "Sm": ["Samarium", 150.36],
        "Sn": ["Tin", 118.710],
        "Sr": ["Strontium", 87.62],
        "Ta": ["Tantalum", 180.94788],
        "Tb": ["Terbium", 158.92535],
        "Tc": ["Technetium", 98],
        "Te": ["Tellurium", 127.60],
        "Th": ["Thorium", 232.03806],
        "Ti": ["Titanium", 47.867],
        "Tl": ["Thallium", 204.3833],
        "Tm": ["Thulium", 168.93421],
        "Ts": ["Tennessine", 294],
        "U": ["Uranium", 238.02891],
        "V": ["Vanadium", 50.9415],
        "W": ["Tungsten", 183.84],
        "Xe": ["Xenon", 131.293],
        "Y": ["Yttrium", 88.90585],
        "Yb": ["Ytterbium", 173.054],
        "Zn": ["Zinc", 65.38],
        "Zr": ["Zirconium", 91.224]
    }
    return periodic_table_dict

def compute_molar_mass(symbol_quantity_list, periodic_table_dict):
    """
    Compute and return the total molar mass of all the elements listed in symbol_quantity_list.
    
    Parameters:
        symbol_quantity_list: A list of lists, where each inner list contains [symbol, quantity]
        periodic_table_dict: Dictionary containing element information
    
    Returns:
        float: The total molar mass
    """
    total_mass = 0.0
    
    # Loop through each element in the symbol_quantity_list
    for element in symbol_quantity_list:

        symbol = element[0] 
        
        quantity = element[1] 

        # Look up the atomic mass in the periodic table dictionary

        atomic_mass = periodic_table_dict[symbol][1] 
        
        # Multiply atomic mass by quantity and add to total
        total_mass += atomic_mass * quantity
    
    return total_mass

def get_known_formulas():
    """
    Enhancement: Returns a dictionary of known chemical formulas and their common names.
    """
    known_formulas = {
        "H2O": "Water",
        "CO2": "Carbon Dioxide", 
        "NaCl": "Sodium Chloride (Table Salt)",
        "C6H12O6": "Glucose",
        "C2H5OH": "Ethanol",
        "NH3": "Ammonia",
        "CH4": "Methane",
        "C6H6": "Benzene",
        "H2SO4": "Sulfuric Acid",
        "HCl": "Hydrochloric Acid",
        "CaCO3": "Calcium Carbonate",
        "NaOH": "Sodium Hydroxide"
    }
    return known_formulas

def calculate_total_protons(symbol_quantity_list, periodic_table_dict):
    """
    Enhancement: Calculate the total number of protons in a molecule.
    """
    # Map of atomic numbers (number of protons) for each element
    atomic_numbers = {
        "H": 1, "He": 2, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Ne": 10,
        "Na": 11, "Mg": 12, "Al": 13, "Si": 14, "P": 15, "S": 16, "Cl": 17, "Ar": 18, "K": 19, "Ca": 20,
        "Sc": 21, "Ti": 22, "V": 23, "Cr": 24, "Mn": 25, "Fe": 26, "Co": 27, "Ni": 28, "Cu": 29, "Zn": 30,
        "Ga": 31, "Ge": 32, "As": 33, "Se": 34, "Br": 35, "Kr": 36, "Rb": 37, "Sr": 38, "Y": 39, "Zr": 40,
        "Nb": 41, "Mo": 42, "Tc": 43, "Ru": 44, "Rh": 45, "Pd": 46, "Ag": 47, "Cd": 48, "In": 49, "Sn": 50,
        "Sb": 51, "Te": 52, "I": 53, "Xe": 54, "Cs": 55, "Ba": 56, "La": 57, "Ce": 58, "Pr": 59, "Nd": 60
    }
    
    total_protons = 0
    for element in symbol_quantity_list:
        symbol = element[0]
        quantity = element[1]
        
        if symbol in atomic_numbers:
            protons_per_atom = atomic_numbers[symbol]
            total_protons += protons_per_atom * quantity
    
    return total_protons

def main():
    """
    Main function that orchestrates the chemistry calculations.
    
    As per requirements:
    - Asks the user for a chemical formula
    - Asks the user for the sample size in grams
    - Call make_periodic_table function and store returned dictionary in variable
    - Call parse_formula to get a list of elements in formula
    - Call compute_molar_mass to calculate the molar mass
    - Display the molar mass
    - Calculate Number of moles in the sample
    - Display the Number of moles
    """
    
    # Ask the user for a chemical formula
    chemical_formula = input("Enter the molecular formula of the sample: ")
    
    # Ask the user for the sample size in grams
    sample_mass = float(input("Enter the mass in grams of the sample: "))
    
    periodic_table_dict = make_periodic_table()
    
    # Call parse_formula to get a list of elements in formula (store in a variable)
    symbol_quantity_list = parse_formula(chemical_formula, periodic_table_dict)
    
    # Call compute_molar_mass to calculate the molar mass
    molar_mass = compute_molar_mass(symbol_quantity_list, periodic_table_dict)
    
    # Display the molar mass
    print(f"{molar_mass:.5f} grams/mole")
    
    # Calculate Number of moles in the sample
    number_of_moles = sample_mass / molar_mass
    
    # Display the Number of moles
    print(f"{number_of_moles:.5f} moles")
    
    #  Try to find the user entered chemical formula in a list of known formulas
    known_formulas = get_known_formulas()

    if chemical_formula in known_formulas:
        print(f"Compound name: {known_formulas[chemical_formula]}")
    
    #  Calculate the total number of protons in a molecule
    total_protons = calculate_total_protons(symbol_quantity_list, periodic_table_dict)

    print(f"Total number of protons: {total_protons}")

if __name__ == "__main__":
    main()