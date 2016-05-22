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

from assignment1 import load_items, save_items
from itemlist import ItemList

def main():
    source_items = load_items()
    items = ItemList(source_items)
    save_items(items.export_items())

main()

