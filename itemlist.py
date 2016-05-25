
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

    def return_item(self, item_index):
        """ mark an item as returned """
        print("Returning {}".format(item_index))
        self.items[item_index].hired = False

    def hire_item(self, item_index):
        """ mark an item as hired """
        print("Hiring {}".format(item_index))
        self.items[item_index].hired = True

    def count(self, hired):
        """ count hired/returned items """
        total = 0
        for item in self.items:
            if item.hired == hired:
                total += 1
        return total
