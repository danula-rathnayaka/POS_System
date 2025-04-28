import re
from datetime import datetime

from model.basket import Basket
from model.bill import Bill
from model.item import Item
from utils.util import write_csv


class POS:
    def __init__(self):
        # Initialize the POS system with an empty basket
        self.__basket = Basket()
        self.__bill_id = 1  # Used to generate unique bill IDs
        self.__bill_list = []

    def add_item_to_basket(self):
        # Get validated input for all item properties
        item_code = self.get_valid_input(
            "Item code: ",
            str,
            lambda x: re.match(r'^\w+$', x),  # \w = [A-Za-z0-9_]
            "Invalid item code: Only letters, numbers, and underscores are allowed."
        )
        internal_price = self.get_valid_input(
            "Internal price: ",
            float,
            lambda x: x >= 0,
            "Internal price cannot be negative."
        )
        discount = self.get_valid_input(
            "Discount: ",
            float,
            lambda x: 0 <= x <= 100,
            "Discount must be between 0 and 100."
        )
        sale_price = self.get_valid_input(
            "Sale price: ",
            float,
            lambda x: x >= 0,
            "Sale price cannot be negative."
        )
        quantity = self.get_valid_input(
            "Quantity: ",
            int,
            lambda x: x > 0,
            "Quantity must be a positive integer."
        )

        # Add the validated item to the basket
        self.__basket.add_item(Item(item_code, internal_price, discount, sale_price, quantity))
        print("Item added.\n")
        self.show_basket()

    def delete_item_from_basket(self):
        # Prevent deletion if basket is empty
        if len(self.__basket.get_items()) == 0:
            print("Basket is empty. No items to delete.\n")
            return

        # Get index to delete and remove item
        index = self.get_valid_input(
            "Enter line number to delete: ",
            int,
            lambda x: 1 <= x <= len(self.__basket.get_items()),
            "Invalid index. Please enter a valid line number."
        ) - 1
        removed = self.__basket.delete_item(index)
        print(f"Item removed from basket:\n{removed}" if removed else "Invalid index.")

    def update_item_in_basket(self):
        # Prevent update if basket is empty
        if len(self.__basket.get_items()) == 0:
            print("Basket is empty. No items to update.\n")
            return

        # Get index of item to update
        index = self.get_valid_input(
            "Enter line number to update: ",
            int,
            lambda x: 1 <= x <= len(self.__basket.get_items()),
            "Invalid index. Please enter a valid line number."
        ) - 1

        # Prompt user for update options
        item = self.__basket.get_item(index)
        print("\nWhat would you like to update?")
        print("1. Sale Price")
        print("2. Discount")
        print("3. Quantity")
        print("4. All of the above")

        option = self.get_valid_input(
            "Choose an option (1-4): ",
            int,
            lambda x: 1 <= x <= 4,
            "Please enter a valid option (1 to 4)."
        )

        # Apply updates based on the selected option
        if option == 1 or option == 4:
            item.set_sale_price(self.get_valid_input(
                "New sale price: ",
                float,
                lambda x: x >= 0,
                "Sale price cannot be negative."
            ))
        if option == 2 or option == 4:
            item.set_discount(self.get_valid_input(
                "New discount: ",
                float,
                lambda x: 0 <= x <= 100,
                "Discount must be between 0 and 100."
            ))
        if option == 3 or option == 4:
            item.set_quantity(self.get_valid_input(
                "New quantity: ",
                int,
                lambda x: x > 0,
                "Quantity must be a positive integer."
            ))

        print(f"Item updated.\n{item}")

    def show_basket(self):
        if len(self.__basket.get_items()) == 0:  # Check if basket is empty
            print("Basket is empty.\n")
        else:
            # Display all items in the basket if not empty
            print("\nBasket:")
            print(self.__basket)  # Basket __str__ overridden to format the output

    def generate_bill(self):
        if len(self.__basket.get_items()) != 0:
            bill = Bill(bill_id=f"{datetime.now().strftime('%y%m%d')}{self.__bill_id}",
                        items=self.__basket.get_items())  # Create a new bill
            self.__bill_list.append(bill)  # Adding the bill to the bill list
            print(bill)
            self.__bill_id += 1  # Incrementing the bill id
            self.__basket.clear()
        else:
            print("No items in the cart")

    def search_bill(self):
        # Check if there are any bills
        if len(self.__bill_list) == 0:
            print("No bills to search.")
            return

        # Ask the user to input the Bill ID to search for
        search_id = self.get_valid_input(
            "Enter the Bill ID to search: ",
            int,
            lambda x: x > 0,  # Bill ID should be positive
            "Bill ID should be positive."
        )

        # Search for the bill in the bill list
        for bill in self.__bill_list:

            # Format the input ID to match the stored format
            if bill.get_bill_id() == str(search_id).zfill(4):
                # Bill found, print its details
                print(f"Bill found: \n{bill}")
                return

        # If loop completes without returning, the bill was not found
        print(f"Bill with ID {search_id} not found.")

    def generate_tax_file(self):
        # Check if there are any bills
        if len(self.__bill_list) == 0:
            print("No bills available to generate tax file.")
            return

        # Define the output CSV file name and the column headers
        file_name = f"tax_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        headers = [
            "bill_id", "item_code", "internal_price", "discount", "sale_price", "quantity", "line_total", "checksum"
        ]

        all_rows = []

        # Process each bill in the system
        for bill in self.__bill_list:
            bill_dict = bill.to_dict()  # Convert bill to dictionary format

            # Process each item in the current bill
            for item in bill_dict["items"]:
                # Create a dictionary row for the item
                row = {
                    "bill_id": bill_dict["bill_id"],
                    "item_code": item["item_code"],
                    "internal_price": item["internal_price"],
                    "discount": item["discount"],
                    "sale_price": item["sale_price"],
                    "quantity": item["quantity"],
                    "line_total": item["line_total"]
                }

                # Generate a checksum using a string representation of all row values
                row["checksum"] = self.generate_checksum(''.join(str(value) for value in row.values()))
                all_rows.append(row)

        # Append the row with checksum to the CSV file using the util method
        write_csv(all_rows, headers, file_name)

        print(f"Tax report has been generated and saved to '{file_name}'.")

    def generate_checksum(self, data):
        upper_case = 0
        lower_case = 0
        number_and_dots = 0

        for char in data:
            if char.isupper():
                upper_case += 1
            elif char.islower():
                lower_case += 1
            elif char.isdigit() or char == '.':
                number_and_dots += 1

        return upper_case + lower_case + number_and_dots

    def run(self):
        # Main menu loop for user interaction
        while True:
            print("\n=== POS System Menu ===")
            print("\n1. Add item to basket")
            print("2. Show basket")
            print("3. Delete item")
            print("4. Update item")
            print("5. Generate bill")
            print("6. Search bill")
            print("7. Generate tax file")
            print("0. Exit")
            choice = self.get_valid_input(
                "Choose an option: ",
                int,
                lambda x: 0 <= x <= 7,
                "Invalid option. Please choose a number between 0 and 7."
            )

            # Calling the required method according to users input
            match choice:
                case 1:
                    self.add_item_to_basket()
                case 2:
                    self.show_basket()
                case 3:
                    self.delete_item_from_basket()
                case 4:
                    self.update_item_in_basket()
                case 5:
                    self.generate_bill()
                case 6:
                    self.search_bill()
                case 7:
                    self.generate_tax_file()
                case 0:
                    print("Exiting POS System.")
                    break
                case _:
                    print("Invalid option. Try again.")

    def get_valid_input(self, prompt, cast_type, validate_fn=None, error_msg="Invalid Input"):
        # Handles input conversion and validation
        while True:
            try:
                value = cast_type(input(prompt))  # Convert input to expected type
                if validate_fn and not validate_fn(value):  # Check additional validation if provided
                    print(error_msg)  # Provided error message
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter a valid value.")  # Short error message


# Entry point to start the application
if __name__ == "__main__":
    pos_system = POS()
    pos_system.run()
