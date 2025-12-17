import tkinter as tk
from tkinter import ttk
from number_entry import FloatEntry


def main():
    # Create the main window
    root = tk.Tk()
    root.title(" KAL Simple Calculator")
    root.geometry("700x700")
    
    # Create and pack the main frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Title label
    title_label = ttk.Label(main_frame, text="Kal Simple Calculator", 
                           font=("Arial", 16, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Input frame
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill=tk.X, pady=(0, 10))
    
    # First number input
    ttk.Label(input_frame, text="First Number:").grid(row=0, column=0, 
                                                      sticky=tk.W, pady=5)
    num1_entry = FloatEntry(input_frame, width=15)
    num1_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
    
    # Second number input
    ttk.Label(input_frame, text="Second Number:").grid(row=1, column=0, 
                                                       sticky=tk.W, pady=5)
    num2_entry = FloatEntry(input_frame, width=15)
    num2_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
    
    # Operation selection
    ttk.Label(input_frame, text="Operation:").grid(row=2, column=0, 
                                                   sticky=tk.W, pady=5)
    operation_var = tk.StringVar(value="+")
    operation_combo = ttk.Combobox(input_frame, textvariable=operation_var,
                                  values=["+", "-", "*", "/"], 
                                  width=12, state="readonly")
    operation_combo.grid(row=2, column=1, padx=(10, 0), pady=5)
    
    # Result display
    result_frame = ttk.Frame(main_frame)
    result_frame.pack(fill=tk.X, pady=10)
    
    ttk.Label(result_frame, text="Result:").pack(anchor=tk.W)
    result_var = tk.StringVar()
    result_label = ttk.Label(result_frame, textvariable=result_var, 
                            font=("Arial", 12, "bold"),
                            background="white", relief="sunken",
                            padding=5)
    result_label.pack(fill=tk.X, pady=(5, 0))
    
    # Status bar
    status_var = tk.StringVar()
    status_label = ttk.Label(main_frame, textvariable=status_var,
                            foreground="red", font=("Arial", 10))
    status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
    
    def calculate():
        """Perform the calculation and display the result."""
        try:
            # Clear any previous error messages
            status_var.set("")
            
            # Get the input values
            num1 = num1_entry.get()
            num2 = num2_entry.get()
            operation = operation_var.get()
            
            # Perform the calculation
            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                if num2 == 0:
                    status_var.set("Error: Cannot divide by zero!")
                    result_var.set("")
                    return
                result = num1 / num2
            
            # Display the result
            result_var.set(f"{result:.2f}")
            
        except ValueError as e:
            # Handle invalid input
            status_var.set("Error: Please enter valid numbers!")
            result_var.set("")
    
    def clear_all():
        """Clear all inputs and outputs."""
        num1_entry.clear()
        num2_entry.clear()
        operation_var.set("+")
        result_var.set("")
        status_var.set("")
    
    # Button frame
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=(10, 0))
    
    # Calculate button
    calculate_btn = ttk.Button(button_frame, text="Calculate", 
                              command=calculate)
    calculate_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    # Clear button
    clear_btn = ttk.Button(button_frame, text="Clear", 
                          command=clear_all)
    clear_btn.pack(side=tk.LEFT)
    
    # Bind Enter key to calculate
    root.bind('<Return>', lambda event: calculate())
    
    # Set focus to first entry field
    num1_entry.focus()
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()