import csv

row_count=0

with open("mentalhealthBulgaria.csv", 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        row_count += 1

print(row_count)