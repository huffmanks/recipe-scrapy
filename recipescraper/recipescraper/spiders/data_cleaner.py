import json


def data_cleaner():
    currentDataFilename = 'recipedata.json'

    with open(currentDataFilename, 'r') as file:
        # Read the contents of the file
        json_data = file.read()

    data = json.loads(json_data)

    # Remove an item by key
    for item in data:
        del item['image_urls']
        del item['image_name']
        del item['images']

    # Convert the modified object back to JSON
    modified_json = json.dumps(data)

    updatedDataFilename = f"modified_{currentDataFilename}"
    # Save the modified JSON to a file if needed
    with open(updatedDataFilename, 'w') as file:
        file.write(modified_json)
