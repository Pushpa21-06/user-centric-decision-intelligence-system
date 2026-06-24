import json
import os

from datetime import datetime

HISTORY_FILE = "history/analysis_history.json"


def save_analysis_history(data):

    # Ensure history file exists
    if not os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "w") as file:
            json.dump([], file)

    # Read existing history
    with open(HISTORY_FILE, "r") as file:

        history = json.load(file)

    # Add timestamp
    data["timestamp"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Append new entry
    history.append(data)

    # Save updated history
    with open(HISTORY_FILE, "w") as file:

        json.dump(history, file, indent=4)