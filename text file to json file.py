import json

def text_to_json(input_file, output_file):
    # Step 1: Read data from the text file
    with open(input_file, 'r') as file:
        text_data = file.readlines()

    # Step 2: Parse the text data
    data_list = []
    temp_data = {}
    for line in text_data:
        line = line.strip()
        if line:  # Check if the line is not empty
            key_value = line.split(": ")
            if len(key_value) == 2:  # Ensure that line has both key and value
                key, value = key_value[0].strip(), key_value[1].strip()
                temp_data[key] = value
        else:
            # If the line is empty, it means the record is complete, so add it to the list
            data_list.append(temp_data)
            temp_data = {}  # Reset temp_data for the next record

    # Step 3: Convert the data to JSON
    json_data = json.dumps(data_list, indent=4)

    # Step 4: Write the JSON data to a new file
    with open(output_file, 'w') as json_file:
        json_file.write(json_data)

# Example usage
input_file_path = 'marks.txt'
output_file_path = 'marks_converted.json'
text_to_json(input_file_path, output_file_path)
