import csv
from geopy.geocoders import Nominatim

def reverse_geocode(latitude, longitude):
    geolocator = Nominatim(user_agent="reverse_geocoding")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    return location.address if location else "N/A"

def reverse_geocode_bulk(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames  ['Address']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            latitude = row['Latitude']
            longitude = row['Longitude']
            address = reverse_geocode(latitude, longitude)
            row['Address'] = address
            writer.writerow(row)

if __name__ == "__main__":
    input_file = "F:\D.p testing.csv"
    output_file = "output_addresses.csv"

    reverse_geocode_bulk(input_file, output_file)
    print(f"Reverse geocoding completed. Results saved to '{output_file}'.")
