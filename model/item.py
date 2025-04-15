class Item:
    def __init__(self, item_code, internal_price, discount, sale_price, quantity):
        """
        Initializes an Item object with given attributes.

        :param item_code: String value representing the item code (String)
        :param internal_price: The cost price of the item (float)
        :param discount: The discount applied to the item (float)
        :param sale_price: The price at which the item is sold (float)
        :param quantity: The number of units being sold (int)
        """
        self.__item_code = item_code
        self.__internal_price = internal_price
        self.__discount = discount
        self.__sale_price = sale_price
        self.__quantity = quantity

    # ---------- Getters ----------
    def get_item_code(self):
        """Returns the item code."""
        return self.__item_code

    def get_internal_price(self):
        """Returns the internal price of the item."""
        return self.__internal_price

    def get_discount(self):
        """Returns the discount applied to the item."""
        return self.__discount

    def get_sale_price(self):
        """Returns the sale price of the item."""
        return self.__sale_price

    def get_quantity(self):
        """Returns the quantity of the item."""
        return self.__quantity

    # ---------- Setters ----------

    def set_item_code(self, item_code):
        """Sets a new item code."""
        self.__item_code = item_code

    def set_internal_price(self, internal_price):
        """Sets a new internal (cost) price."""
        self.__internal_price = internal_price

    def set_discount(self, discount):
        """Sets a new discount value."""
        self.__discount = discount

    def set_sale_price(self, sale_price):
        """Sets a new sale price."""
        self.__sale_price = sale_price

    def set_quantity(self, quantity):
        """Sets a new quantity."""
        self.__quantity = quantity

    def get_line_total(self):
        """
        Calculates and returns the line total for the item.
        Line Total = sale price × quantity
        """
        return self.__sale_price * self.__quantity

    def to_dict(self):
        """
        Converts the item details into a dictionary format.
        """
        return {
            "item_code": self.__item_code,
            "internal_price": self.__internal_price,
            "discount": self.__discount,
            "sale_price": self.__sale_price,
            "quantity": self.__quantity,
            "line_total": self.get_line_total()
        }

    def __str__(self):
        """
        Returns a user-friendly string representation of the item,
        """
        # Define the header line
        header_line = "+-----------------------+----------------+--------------+------------+----------+--------------+"

        # Define the row data with the item's details
        item_row = (f"| {self.__item_code:<21} | {self.__internal_price:<14.2f} | {self.__sale_price:<12.2f} | "
                    f"{self.__discount:<10.2f} | {self.__quantity:<8} | {self.get_line_total():<12.2f} |")

        # Return the full table with top and bottom lines
        return (f"{header_line}\n"
                f"| {'Item Code':<21} | {'Internal Price':<14} | {'Sale Price':<12} | {'Discount':<10} | "
                f"{'Quantity':<8} | {'Line Total':<12} |\n"
                f"{header_line}\n"
                f"{item_row}\n"
                f"{header_line}")
