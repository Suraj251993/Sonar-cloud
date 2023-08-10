import csv
from geopy.geocoders import Nominatim
import time
import geopy.exc

def reverse_geocode(latitude, longitude):
    geolocator = Nominatim(user_agent="reverse_geocoding", timeout=5)
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        return location.address if location else "N/A"
    except geopy.exc.GeocoderUnavailable as e:
        print("GeocoderUnavailable - Retrying after 5 seconds...")
        time.sleep(5)
        return reverse_geocode(latitude, longitude)
    except geopy.exc.GeocoderServiceError as e:
        print("GeocoderServiceError - Retrying after 5 seconds...")
        time.sleep(5)
        return reverse_geocode(latitude, longitude)

def reverse_geocode_bulk(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Address']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            gps_coordinates = row['GPS Coordinates']
            latitude, longitude = map(float, gps_coordinates.split(','))
            address = reverse_geocode(latitude, longitude)
            row['Address'] = address
            writer.writerow(row)

if _name_ == "_main_":
    input_file = r"C:\Users\Acer\Mw POI Dataset\Malaysia - POI  - Statics.csv"
    output_file = r"C:\Users\Acer\Mw POI Dataset\newstatic.csv"

    reverse_geocode_bulk(input_file, output_file)
    print(f"Reverse geocoding completed. Results saved to '{output_file}'.")