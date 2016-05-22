
from item import Item

class ItemList:
    def __init__(self, source_items):
        """ initialise an ItemList instance """
        self.items = []
        for item in source_items:
            (name, description, price, hired) = item
            self.items.append(Item(name, description, price, hired))

    def export_items(self):
        """ returns a list of items prepared for saving """
        result = []
        for item in self.items:
            result.append((item.name, item.description, item.price, item.hired))
        return result
