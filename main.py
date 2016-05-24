"""
CP1404 2016 SP51 Assignment 2 – Items for Hire – GUI

GUI-based items hiring program that allows to:
- load items from a file
- hire items
- return items
- add new items
- save items to a file

"""

__author__ = 'Luke Veltjens-Swan'

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from enum import Enum
from assignment1 import load_items, save_items
from itemlist import ItemList


class Mode(Enum):
    """ Supported modes """
    listing = 1
    hiring = 2
    returning = 3


class ItemButton(Button):
    """ Item button class """
    hired = BooleanProperty(False)
    item_index = NumericProperty()


class ItemsHiring(App):
    """ Main application class """

    status_text = StringProperty()

    def on_start(self):
        """ Load items from the CSV file on start """
        source_items = load_items()
        self.item_list = ItemList(source_items)
        self.create_item_buttons()
        self.set_mode(Mode.listing)

    def on_stop(self):
        """ Save items to the CSV file on exit """
        save_items(self.item_list.export_items())

    def build(self):
        """ Build Kivy app from the kv file """
        self.title = "Items Hiring"
        self.root = Builder.load_file('app.kv')
        return self.root

    def create_item_buttons(self):
        """ Create the entry buttons and add them to the GUI """
        for i, item in enumerate(self.item_list.items):
            button = ItemButton(text=item.name, hired=item.hired, item_index=i)
            button.bind(on_release=self.press_item)
            self.root.ids.itemsGrid.add_widget(button)

    def clear_selection(self):
        """ Clear any buttons that have been selected """
        for instance in self.root.ids.itemsGrid.children:
            instance.state = 'normal'

    def set_mode(self, mode):
        """ Switch between 'listing', 'hiring' and 'returning' modes """
        ids = self.root.ids
        for button in [ids.buttonList, ids.buttonHire, ids.buttonReturn]:
            button.state = 'normal'
        if mode == Mode.listing:
            self.status_text = "Choose action from the left menu, then select items on the right"
            ids.buttonList.state = 'down'
        elif mode == Mode.hiring:
            self.status_text = "Select available items to hire"
            ids.buttonHire.state = 'down'
        elif mode == Mode.returning:
            self.status_text = "Select available items to return"
            ids.buttonReturn.state = 'down'
        self.clear_selection()
        self.mode = mode

    def press_item(self, instance):
        """ Handler for pressing an item button """
        if instance.hired:
            return
        instance.state = 'normal' if instance.state == 'down' else 'down'

    def press_list(self):
        """ Handler for pressing the 'List Items' button """
        self.set_mode(Mode.listing)

    def press_hire(self):
        """ Handler for pressing the 'Hire Items' button """
        self.set_mode(Mode.hiring)

    def press_return(self):
        """ Handler for pressing the 'Return Items' button """
        self.set_mode(Mode.returning)

    def press_confirm(self):
        """ Handler for pressing the 'Conrirm' button """
        pass

    def press_add(self):
        """ Handler for pressing the 'Add New Item' button """
        pass


def main():
    app = ItemsHiring()
    app.run()


main()

