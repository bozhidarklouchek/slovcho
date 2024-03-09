import csv

# Define the path to your CSV file
csv_file_path = 'dictionary.csv'  # Replace with the path to your CSV file

try:
    # Open the CSV file for reading
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file) 

        # Iterate through each row in the CSV file and print them
        counter = 0
        types = set()
        for row in csv_reader:
            w_type = row['type']
            types.add(w_type)
            # derivs = len(row['derivatives'].split(','))
            # counter += derivs
            # print(row['id'] + ' ' + row['headword'] + ' ' +row['type'] + ' ' +row['definition'] + ' ' +row['derivatives'])
        print(types)

except FileNotFoundError:
    print(f"File not found: {csv_file_path}")

except Exception as e:
    print(f"An error occurred: {e}")
