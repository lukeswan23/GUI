

__author__ = 'Luke Veltjens-Swan'


MENU = "\nMenu:\n(L)ist all items\n(H)ire an item\n(R)eturn an item\n(A)dd new item to stock\n(Q)uit"
ALL = 0
ONLY_HIRED = 1
ONLY_AVAILABLE = 2


def main():
    user_name = input("Enter your name: ")
    items = load_items()
    print("Welcome {}, to my amazing program".format(user_name))
    print(MENU)
    choice = input(">>> ").upper()
    while choice != "Q": # Q - quit
        # list all items
        if choice == "L":
            print("All items on file (* indicates item is currently out):")
            list_items(items, ALL)
        # hire an item
        elif choice == "H":
            available = items_to_display(items, ONLY_AVAILABLE)
            if len(available) == 0:
                print("No items available for hire")
            else:
                print("\n".join(available))
                number = input_item_number("hire", items)
                hire_item(number, items)
        # return an item
        elif choice == "R":
            hired = items_to_display(items, ONLY_HIRED)
            if len(hired) == 0:
                print("No items are currently on hire")
            else:
                print("\n".join(hired))
                number = input_item_number("return", items)
                return_item(number, items)
        # add a new item
        elif choice == "A":
            item = input_new_item()
            items.append(item)
        else:
            print("Invalid menu choice.")
        print(MENU)
        choice = input(">>> ").upper()
    # before quit
    save_items(items)
    print("Have a nice day :)")


# read items from a CSV file
def load_items():
    in_file = open("items.csv")
    lines = in_file.readlines()
    items = []
    for line in lines:
        parts = line.strip().split(",")
        name = parts[0]
        description = parts[1]
        price = float(parts[2])
        hired = parts[3] == "out"
        item = (name, description, price, hired)
        items.append(item)
    in_file.close()
    print("{} items loaded from items.csv".format(len(items)))
    return items


# save items to a CSV file
def save_items(items):
    out_file = open("items.csv", "w")
    for item in items:
        (name, description, price, hired) = item
        if hired:
            status = "out"
        else:
            status = "in"
        out_file.write("{},{},{},{}\n".format(name, description, price, status))
    out_file.close()
    print("{} items saved to items.csv".format(len(items)))


# returns a list of HIRED, AVAILABLE or ALL items (formatted)
def items_to_display(items, kind):
    result = []
    for i, item in enumerate(items):
        (name, description, price, hired) = item
        title = "{} ({})".format(name, description)
        status = ""
        if hired:
            if kind == ONLY_AVAILABLE:
                continue
            if kind == ALL:
                status = "*"
        else:
            if kind == ONLY_HIRED:
                continue
        result.append("{} - {:45} = $ {:>6.2f} {}".format(i, title, price, status))
    return result


# string representation of HIRED, AVAILABLE or ALL items
def list_items(items, kind):
    print("\n".join(items_to_display(items, kind)))


# create a new item from user input
def input_new_item():
    name = input("Item name: ")
    while name == "":
        print("Input can not be blank")
        name = input("Item name: ")
    description = input("Description: ")
    while description == "":
        print("Input can not be blank")
        description = input("Description: ")
    price = -1
    while price < 0:
        try:
            price = float(input("Price per day: "))
            if price < 0:
                print("Invalid input; enter a valid number")
        except:
            print("Invalid input; enter a valid number")
    return (name, description, price, False)


# asks for a valid item number
def input_item_number(to, items):
    print("Enter the number of an item to {}".format(to))
    number = -1
    while number < 0 or number >= len(items):
        try:
            number = int(input(">>> "))
            if number < 0 or number >= len(items):
                print("Invalid item number")
        except:
            print("Invalid input; enter a number")
    return number


# mark an item as HIRED
def hire_item(number, items):
    (name, description, price, hired) = items[number]
    if hired:
        print("That item is not available for hire")
        return
    items[number] = (name, description, price, True)
    print("{} hired for ${:.2f}".format(name, price))


# mark an item as RETURNED
def return_item(number, items):
    (name, description, price, hired) = items[number]
    if not hired:
        print("That item is not hired")
        return
    items[number] = (name, description, price, False)
    print("{} returned".format(name))

