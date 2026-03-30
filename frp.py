class Button:
    def __init__(self, text, align):
        self.text = text
        self.align = align

    def show(self):
        print(f"Button: {self.text}, Alignment: {self.align}")


# creating two objects from the same class
btn1 = Button("Submit", "left")
btn2 = Button("Cancel", "right")

btn1.show()
btn2.show()
