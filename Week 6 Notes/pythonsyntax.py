# dictionaries

pizzas = {
    "cheese": 9,
    "pep": 11,
    "veg": 10
}

for pie, price in pizzas.items():
    print("A whole {} pizza costs ${}".format(pie, price)) #.format is converting the dictinoary to a list

# objects

class Student():
    def __init__(self, name, id):
        self.name = name
        self.id = id
    def changeID(self, id):
        self.id = id
    def print(self):
        print("{} - {}".format(self.name, self.id))

jane = Student("Jane", 10)
jane.print()
jane.changeID(11)
jane.print()