
class Item:
    def __init__(self, name, description, price, hired=False):
        """ initialise an Item instance """
        self.name = name
        self.description = description
        self.price = price
        self.hired = hired
