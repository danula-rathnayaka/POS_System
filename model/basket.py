class Basket:
    def __init__(self):
        """
        Initializes a basket with empty list.
        """
        self.__basket = []

    def add_item(self, item):
        """
        Adds an item object to the basket.

        :param item: Item to add to the basket
        """
        self.__basket.append(item)

    def delete_item(self, index):
        """
        Deletes an item from the basket by index (line number).
        Returns the deleted item.

        :param index: Index of the item to delete
        """
        return self.__basket.pop(index)

    def update_item(self, index, item):
        """
        Updates sale price, discount, and quantity of an item by index.

        :param index: Index of the item to update
        :param item: Updated item to add to the basket
        """
        self.__basket[index] = item

    def get_item(self, index):
        """
        Returns the item at the given index (line number).

        :param index: Index of the item to get
        """
        return self.__basket[index]

    def get_items(self):
        """
        Returns the entire list of items in the basket.
        """
        return self.__basket

    def get_total(self):
        """
        Calculates and returns the grand total of the basket.
        """
        return sum(item.get_line_total() for item in self.__basket)

    def clear(self):
        """
        Empties the basket.
        """
        self.__basket = []

    def __str__(self):
        """
        Displays all current items in the basket with line numbers in a table format.
        """
        if not self.__basket:
            return "Basket is empty."

        # Define the header line for the table
        header_line = "+------+----------------+----------------+--------------+------------+----------+--------------+"

        # Define the header row
        header_row = "| Line | Item Code      | Internal Price | Sale Price   | Discount   | Quantity | Line Total   |"

        # Start assembling the table
        basket_table = f"{header_line}\n{header_row}\n{header_line}\n"

        # Add the row for each item in the basket
        for i, item in enumerate(self.__basket):
            basket_table += (f"| {i + 1:<4} | {item.get_item_code():<14} | "
                             f"{item.get_internal_price():<14.2f} | {item.get_sale_price():<12.2f} | "
                             f"{item.get_discount():<10.2f} | {item.get_quantity():<8} | "
                             f"{item.get_line_total():<12.2f} |\n")

        # Add the bottom border
        basket_table += f"{header_line}"

        return basket_table
