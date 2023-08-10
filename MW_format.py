import csv
import re

# Sample data (list of dictionaries)
data = [
    {
        'MW POI ID': 'ABC123456789XYZA',
        'Location Name': 'Sample Location 1',
        'Parent_Category': 'Category 1',
        'Child_Category': 'Subcategory 1',
        'Grand_Child_Category': 'Sub-subcategory 1',
        'Latitude': 40.7128,
        'Longitude': -74.0060,
        'Street Address': '123 Main Street',
        'Country': 'United States',
        'Region/state': 'New York',
        'District': 'Manhattan',
        'City': 'New York City',
        'Postcode': '10001',
        'Open Hours (Day, HH:MM:SS)': 'Monday 09:00:00',
        'Category/place Tags': 'Tag1, Tag2',
        'Website': 'https://www.example.com',
        'TimeZone': 'UTC',
        'Peak Hours': '12:00:00',
        'Relative Wealth index': 5,
        'Verified': 1,
        'NAICS/Business Code': 12345,
        'Last Refreshed': '2023-07-24',
        'Source': 'Example Source',
        'ID At Source': 'ABC123'
    },
    # Add more data here...
]

# Define the field names and their corresponding data format
field_formats = {
    'MW POI ID': r'^[A-Za-z0-9]{16}$',
    'Location Name': r'^[A-Za-z0-9 ]{1,256}$',
    'Parent_Category': r'^[A-Za-z0-9 ]{1,256}$',
    'Child_Category': r'^[A-Za-z0-9 ]{1,256}$',
    'Grand_Child_Category': r'^[A-Za-z0-9 ]{1,256}$',
    'Latitude': r'^-?\d{1,3}\.\d{6}$',
    'Longitude': r'^-?\d{1,3}\.\d{6}$',
    'Street Address': r'^[A-Za-z0-9 ]{1,512}$',
    'Country': r'^[A-Za-z0-9 ]{1,256}$',
    'Region/state': r'^[A-Za-z0-9 ]{1,256}$',
    'District': r'^[A-Za-z0-9 ]{1,256}$',
    'City': r'^[A-Za-z0-9 ]{1,256}$',
    'Postcode': r'^[A-Za-z0-9 ]{1,256}$',
    'Open Hours (Day, HH:MM:SS)': r'^[A-Za-z]{3} \d{2}:\d{2}:\d{2}$',
    'Category/place Tags': r'^[A-Za-z0-9, ]+$',
    'Website': r'^https?://[^\s]+$',
    'TimeZone': r'^[A-Za-z0-9 ]{1,256}$',
    'Peak Hours': r'^\d{2}:\d{2}:\d{2}$',
    'Relative Wealth index': r'^\d+$',
    'Verified': r'^[01]$',
    'NAICS/Business Code': r'^\d+$',
    'Last Refreshed': r'^\d{4}-\d{2}-\d{2}$',
    'Source': r'^[A-Za-z0-9 ]{1,256}$',
    'ID At Source': r'^[A-Za-z0-9 ]{1,256}$'
}

# Define the CSV file name
csv_file = 'poi_data.csv'

# Function to validate data format
def is_valid_format(field, value):
    pattern = field_formats.get(field)
    if pattern:
        return bool(re.match(pattern, str(value)))
    return True

# Write data to CSV file
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())

    # Write the header row
    writer.writeheader()

    # Write the data rows
    for row in data:
        if all(is_valid_format(field, row[field]) for field in row):
            writer.writerow(row)
        else:
            print(f"Invalid data format in row: {row}")

print(f'Data has been written to {csv_file}.')
