import csv
with open('contacts.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    print("CSV Columns:")
    for i, col in enumerate(headers):
        print(f"{i}: {col}")


