import json

# Data to be written to the JSON file
data = {
    "name": "DJ",
    "age": 25,
    "skills": ["Python", "Networking", "Cybersecurity"],
    "is_active": True,
    "projects": None
}

# File name to save the JSON data
file_name = "output.json"

# Writing data to the JSON file
try:
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)  # `indent=4` makes the JSON file more readable
    print(f"Data successfully written to {file_name}")
except Exception as e:
    print(f"An error occurred: {e}")
