"""
CP1404 2016 SP51 Assignment 2 – Items for Hire – GUI

GUI-based items hiring program that allows to:
- load items from a file
- hire items
- return items
- add new items
- save items to a file
https://github.com/lukeveltjensswan/GUI
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
    selected = BooleanProperty(False)
    item_index = NumericProperty()

    def set_selected(self, selected):
        self.selected = selected
        self.state = 'down' if self.selected else 'normal'

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

    def create_item_button(self, item, item_index):
        """ Create an item button for a certain item """
        button = ItemButton(text=item.name, hired=item.hired, item_index=item_index)
        button.bind(on_release=self.press_item)
        self.root.ids.itemsGrid.add_widget(button)

    def create_item_buttons(self):
        """ Create the item buttons and add them to the GUI """
        for i, item in enumerate(self.item_list.items):
            self.create_item_button(item, i)

    def clear_selection(self):
        """ Clear any buttons that have been selected """
        for instance in self.root.ids.itemsGrid.children:
            instance.set_selected(False)

    def update_item_buttons(self):
        """ Update colors of item buttons """
        for instance in self.root.ids.itemsGrid.children:
            item = self.item_list.items[instance.item_index]
            instance.hired = item.hired

    def set_mode(self, mode):
        """ Switch between 'listing', 'hiring' and 'returning' modes """
        ids = self.root.ids
        for button in [ids.buttonList, ids.buttonHire, ids.buttonReturn]:
            button.state = 'normal'
        if mode == Mode.listing:
            self.status_text = "Choose action from the left menu, then select items on the right"
            ids.buttonList.state = 'down'
        elif mode == Mode.hiring:
            if self.item_list.count(hired=False) > 0:
                self.status_text = "Select available items to hire"
            else:
                self.status_text = "No items available for hire"
            ids.buttonHire.state = 'down'
        elif mode == Mode.returning:
            if self.item_list.count(hired=True) > 0:
                self.status_text = "Select available items to return"
            else:
                self.status_text = "No items are currently on hire"
            ids.buttonReturn.state = 'down'
        self.clear_selection()
        self.mode = mode

    def show_details(self, item_index):
        """ Display item details in the status bar """
        item = self.item_list.items[item_index]
        status = "out" if item.hired else "in"
        self.status_text = "{}({}), ${:.2f} is {}".format(item.name, item.description, item.price, status)

    def selecting_allowed(self, hired):
        """ Check if item is selectable depending on hired status """
        if self.mode == Mode.hiring and not hired:
            return True
        elif self.mode == Mode.returning and hired:
            return True
        return False

    def show_selection_status(self):
        """ Display selected items in the status bar """
        names = []
        total_price = 0
        for i, button in enumerate(self.root.ids.itemsGrid.children):
            item = self.item_list.items[button.item_index]
            if button.selected:
                names.append(item.name)
                total_price += item.price
        if len(names) == 0:
            names = "no items"
        else:
            names = ", ".join(names)
        if self.mode == Mode.hiring:
            self.status_text = "Hiring: {} for ${:.2f}".format(names, total_price)
        else:
            self.status_text = "Returning: {}".format(names)

    def press_item(self, instance):
        """ Handler for pressing an item button """
        if self.mode == Mode.listing:
            self.show_details(instance.item_index)
            return
        if self.selecting_allowed(instance.hired):
            instance.set_selected(not instance.selected)
        self.show_selection_status()

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
        for button in self.root.ids.itemsGrid.children:
            if not button.selected:
                continue
            item = self.item_list.items[button.item_index]
            if self.mode == Mode.hiring:
                self.item_list.hire_item(button.item_index)
            elif self.mode == Mode.returning:
                self.item_list.return_item(button.item_index)
        self.update_item_buttons()
        self.set_mode(Mode.listing)

    def press_add(self):
        """ Handler for pressing the 'Add New Item' button """
        self.status_text = "Enter details for new item"
        self.root.ids.popup.open()

    def press_save(self, name, description, price):
        """ Handler for pressing the save button in the popup """
        if not name or not description or not price:
            self.status_text = "All fields must be completed"
            return
        try:
            price = float(price)
        except:
            self.status_text = "Price must be a valid number"
            return
        if price <= 0:
            self.status_text = "Price must not be negative or zero"
            return
        self.item_list.add_item(name, description, price, hired=False)
        last_index = len(self.item_list.items) - 1
        item = self.item_list.items[last_index]
        self.create_item_button(item, last_index)
        self.close_popup()

    def close_popup(self):
        """ Close the popup and clear input fields """
        self.root.ids.popup.dismiss()
        self.clear_fields()

    def clear_fields(self):
        """ Clear input fields in the popup """
        self.root.ids.itemName.text = ""
        self.root.ids.itemDescription.text = ""
        self.root.ids.itemPrice.text = ""


def main():
    app = ItemsHiring()
    app.run()


main()
