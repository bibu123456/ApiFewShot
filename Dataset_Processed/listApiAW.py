import csv
import json

def create_api_mapping(csv_file_path, output_file_path, last_chars=('A', 'W')):
    # Open CSV file
    with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Skip header

        # Find the index of the 'api' column
        api_column_index = header.index("api")

        # Initialize a dictionary to store API mappings
        api_mapping = {}

        # Loop through each row in the CSV
        for row in reader:
            # Split APIs by comma and remove leading/trailing whitespaces
            apis = [api.strip() for api in row[api_column_index].split(',')]

            # Filter APIs based on last character and create mapping
            for api in apis:
                if api.endswith(last_chars):
                    modified_api = api[:-1]
                    api_mapping[api] = modified_api

        # Write the API mapping to a JSON file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(api_mapping, output_file, indent=4)

if __name__ == "__main__":
    data_file = 'VirusShare.csv'
    output_file = 'api_mapping1.json'
    create_api_mapping(data_file, output_file)
