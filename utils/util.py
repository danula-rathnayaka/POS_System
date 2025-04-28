import os
import csv

default_path = "../data"


def write_csv(data, headers, file_name, path=default_path):
    """Appends a single dictionary row to a CSV file. Creates file if needed.

    :param data: Dictionary of data
    :param headers: List of headers
    :param file_name: File name of the CSV file
    :param path: Path of the CSV file
    """

    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, file_name)

    # Open the file and append the new row
    with open(full_path, "w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # Write header
        writer.writerows(data)


def read_csv(file_name, path=default_path):
    """Reads a CSV file and returns a list of dictionaries.

    :param file_name: File name of the CSV file
    :param path: Path of the CSV file
    """
    full_path = os.path.join(path, file_name)
    if not os.path.exists(full_path):
        return []

    with open(full_path, "r", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)
