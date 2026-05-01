import json

def read_json_to_list(file_path):
    # Open and read the JSON file    
    with open('api/dictionary.json', 'r') as json_file:
        data = json.load(json_file)
    
    # If the file is already a simple list of words, just return it
    if isinstance(data, list):
        return data
        
    # If it's a dictionary (object), extract the words from the values
    string_list = []
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                string_list.extend(value)
            else:
                string_list.append(str(value))
    return string_list