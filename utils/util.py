import os
import json
import csv

default_path = "../data"


def read_json(file_name, path=default_path):
    full_path = os.path.join(path, file_name)
    """
    Reads and returns JSON data from a file.
    
    :param file_name: File name of the JSON file
    :param path: Path of the JSON file
    :rtype: JSON object
    """
    if not os.path.exists(full_path):
        return None
    with open(full_path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print("Error when reading JSON")
            return None


def append_json(data, file_name, path=default_path):
    """Appends a new item to a JSON list in a file. Creates file if needed.

    :param data: Data to be saved in the JSON format
    :param file_name: File name of the JSON file
    :param path: Path of the JSON file
    """

    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, file_name)

    # Initialize data list if file doesn't exist
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    raise ValueError("JSON root must be a list to append.")
            except json.JSONDecodeError:
                existing_data = []  # Start fresh if file is empty or malformed
    else:
        existing_data = []  # Start with an empty list if the file doesn't exist

    # Append the new item and save it back
    existing_data.append(data)
    with open(full_path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)


def append_csv(row, headers, file_name, path=default_path):
    """Appends a single dictionary row to a CSV file. Creates file if needed.

    :param row: Dictionary of data
    :param headers: List of headers
    :param file_name: File name of the CSV file
    :param path: Path of the CSV file
    """

    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, file_name)

    # Open the file and append the new row
    with open(full_path, "a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if not os.path.exists(full_path):
            writer.writeheader()  # Write header if the file is new
        writer.writerow(row)


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
