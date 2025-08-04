# Open the HR system file
with open("hr_system.txt") as hr_file:
    # Skip the header line
    next(hr_file)
    
    # Process each employee line
    for line in hr_file:
        # Remove leading/trailing whitespace and split into parts
        parts = line.strip().split()
        
        # Extract employee data
        name = parts[0]
        id_number = parts[1]
        job_title = parts[2]
        salary = float(parts[3])
        
        # Calculate paycheck amount (twice monthly)
        paycheck = salary / 24
        
        # Add $1000 bonus for engineers
        if job_title.lower() == "engineer":
            paycheck += 1000
        
        # Print employee information with formatted paycheck
        print(f"{name} (ID: {id_number}), {job_title} - ${paycheck:.2f}")