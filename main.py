"""
CP1404 2016 SP51 Assignment 2 – Items for Hire – GUI

GUI-based items hiring program that allows to:
- load items from a file
- hire items
- return items
- add new items
- save items to a file
c
"""

__author__ = 'Luke Veltjens-Swan'

from kivy.app import App
from kivy.lang import Builder
from assignment1 import load_items, save_items
from itemlist import ItemList


class ItemsHiring(App):
    """ Main application class """

    def on_start(self):
        """ load items from the CSV file on start """
        source_items = load_items()
        self.item_list = ItemList(source_items)

    def on_stop(self):
        """ save items to the CSV file on exit """
        save_items(self.item_list.export_items())

    def build(self):
        """ build Kivy app from the kv file """
        self.title = "Items Hiring"
        self.root = Builder.load_file('app.kv')
        return self.root


def main():
    app = ItemsHiring()
    app.run()


main()
