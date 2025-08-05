import zmq
import json
import os

# Load file from user
CUSTOM_FILE = "user_categories.json"
if os.path.exists(CUSTOM_FILE):
    with open(CUSTOM_FILE, "r") as f:
        user_defined_categories = json.load(f)
else:
    user_defined_categories = {}

# Default categories
default_categories = {
    "electric": "utilities",
    "hydro": "utilities",
    "starbucks": "Food & Drink",
    "pizza": "Food & Drink",
    "netflix": "Entertainment",
    "hbo": "Entertainment",
}


def add_category(keyword, category):
    user_defined_categories[keyword.lower()] = category
    with open(CUSTOM_FILE, "w") as f:
        json.dump(user_defined_categories, f, indent=2)


def get_all_keyword_categories():
    combined = default_categories.copy()
    combined.update(user_defined_categories)
    return combined


# ZeroMQ
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:6120")

print("Ingredient Categorizer Microservices is running...")

while True:
    message = socket.recv_string().strip()

    # Handles custom category addition (format add-keyword-category)
    if message.lower().startswith("add-"):
        try:
            _, keyword, category = message.split("-", 2)
            add_category(keyword, category)
            socket.send_string(f"Rule added- '{keyword}' - '{category}'")
        except ValueError:
            socket.send_string("Error: Please use format add-keyword-category")
        continue

    description = message.lower()
    category = "Uncategorized"

    for keyword, cat in get_all_keyword_categories().items():
        if keyword in description:
            category = cat
            break

    socket.send_string(category)
