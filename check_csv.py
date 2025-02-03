import csv

# Open and read CSV file
with open("mobiles.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    # Print the detected column headers
    print("CSV Headers Detected:", reader.fieldnames)
