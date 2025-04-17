from datetime import datetime


class Bill:
    def __init__(self, bill_id, items):
        self.__bill_id = str(bill_id).zfill(4)
        self.__items = items
        self.__timestamp = datetime.today().replace(microsecond=0)
        self.__total_amount = sum(item.get_line_total() for item in items)

    def get_bill_id(self):
        return self.__bill_id

    def get_items(self):
        return self.__items

    def get_timestamp(self):
        return self.__timestamp

    def get_grand_total(self):
        return self.__total_amount

    def to_dict(self):
        return {
            "bill_id": self.__bill_id,
            "timestamp": self.__timestamp,
            "grand_total": self.get_grand_total(),
            "items": [item.to_dict() for item in self.__items]
        }

    def __str__(self):
        """
        Displays the bill details and its items in a table format.
        """
        if not self.__items:
            return "No items in the bill."

        # Define the header line for the table
        header_line = "+------+----------------+----------------+--------------+------------+----------+--------------+"

        # Define the header row
        header_row = "| Line | Item Code      | Internal Price | Sale Price   | Discount   | Quantity | Line Total   |"

        # Start assembling the table
        bill_table = f"\n1Bill ID: {self.__bill_id}\nTimestamp: {self.__timestamp}\n{header_line}\n{header_row}\n{header_line}\n"

        # Add the row for each item in the bill
        for i, item in enumerate(self.__items):
            bill_table += (f"| {i + 1:<4} | {item.get_item_code():<14} | "
                           f"{item.get_internal_price():<14.2f} | {item.get_sale_price():<12.2f} | "
                           f"{item.get_discount():<10.2f} | {item.get_quantity():<8} | "
                           f"{item.get_line_total():<12.2f} |\n")

        # Add the total amount and bottom border
        bill_table += f"{header_line}\n"
        bill_table += f"\nGrand Total: {self.get_grand_total():<12.2f}\n"

        return bill_table
