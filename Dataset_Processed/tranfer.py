import csv
import json

def csv_to_json(csv_file, json_file):
    # Open CSV file and read data
    with open(csv_file, 'r', encoding='utf-8-sig') as csv_input:
        csv_reader = csv.DictReader(csv_input)
        
        # Convert CSV data to a list of dictionaries
        data = list(csv_reader)
    
    # Write JSON data to the output file
    with open(json_file, 'w') as json_output:
        json_output.write(json.dumps(data, indent=2))

# Specify the input and output file names
csv_file_name = 'VirusShare.csv'
json_file_name = 'VirusShare.json'

# Convert CSV to JSON
csv_to_json(csv_file_name, json_file_name)
