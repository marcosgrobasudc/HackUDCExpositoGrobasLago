import json
from datetime import datetime

def create_user(user_name, file="records.json"):
    try:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        if user_name not in data:
            data[user_name] = {"chat": [], "daily_records": {}}
        else:
            return f"User name {user_name} already exists"

        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error saving the interaction: {e}")


def save_chat(user, chat, file="records.json"):
    """
    Saves the user's chat interactions with detected emotions and their scores.
    """
    try:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if user not in data:
            data[user] = {"chat": [], "daily_records": {}}
        data[user]["chat"] = chat

        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error saving the interaction: {e}")


def read_chat(user, file="records.json"):
    """
    Reads and returns all interactions of the specified user from the file.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if user in data:
            return data[user]["chat"]
        else:
            return []  # Return an empty list if the user doesn't exist in the data
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if the file is not found or is empty
    except Exception as e:
        print(f"Error reading interactions: {e}")
        return []


def save_daily_record(user, record, emotions, file="records.json"):
    """
    Saves or overwrites the user's daily record with the current date and associated emotions.
    """
    try:
        # Load previous data if the file exists
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Create user structure if it doesn't exist
        if user not in data:
            data[user] = {"interactions": [], "daily_records": {}}
        
        # Overwrite the record and emotions of the day
        data[user]["daily_records"][current_date] = {
            "record": record,
            "emotions": emotions
        }
        
        # Save changes to the file
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error saving the daily record: {e}")

def read_daily_record(user, file="records.json"):
    """
    Reads and returns the user's daily record for the current date.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        if user in data and current_date in data[user]["daily_records"]:
            return data[user]["daily_records"][current_date]
        else:
            return None
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    except Exception as e:
        print(f"Error reading the daily record: {e}")
        return None

# Test code
if __name__ == "__main__":
    # Simulating interactions
    print("Saving interactions...")
    save_chat("John", "I feel amazing today", {"happy": 0.9, "excited": 0.7})
    save_chat("Anna", "I'm a bit tired", {"tired": 0.8, "stressed": 0.6})
    save_chat("John", "I'm a bit calmer now", {"calm": 0.7})
    
    # Simulating daily records with emotions
    print("Saving daily records...")
    save_daily_record("John", "I had a great day at work.", {"happy": 0.9, "satisfied": 0.8})
    save_daily_record("Anna", "The day was tiring, but productive.", {"tired": 0.7, "satisfied": 0.6})
    
    # Reading and modifying a record
    print("Reading John's record...")
    john_record = read_daily_record("John")
    if john_record:
        print("John's record:", json.dumps(john_record, ensure_ascii=False, indent=4))
    
    # Overwriting the daily record with new data
    print("Overwriting John's daily record...")
    save_daily_record("John", "It was an excellent day, I finished many projects.", {"happy": 0.95, "proud": 0.9})
    
    # # Displaying the content of the file in a readable format
    # print("Content of records.json:")
    # with open("records.json", "r", encoding="utf-8") as f:
    #     data = json.load(f)
    #     print(json.dumps(data, ensure_ascii=False, indent=4))

    # Simulating reading interactions
    print("Reading interactions for John...")
    john_interactions = read_interactions("John")
    if john_interactions:
        for interaction in john_interactions:
            print(f"{interaction['timestamp']}: {interaction['message']} - Emotions: {interaction['emotions']}")
        # print("John's interactions:", json.dumps(john_interactions, ensure_ascii=False, indent=4))
    else:
        print("No interactions found for John.")