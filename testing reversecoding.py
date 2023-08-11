from geopy.geocoders import Nominatim

# Create a Nominatim geolocator
geolocator = Nominatim(user_agent="reverse-geocoding")

# Provide latitude and longitude values
latitude = 37.7749
longitude = -122.4194

# Perform reverse geocoding
location = geolocator.reverse((latitude, longitude), exactly_one=True)

if location:
    print("Address:", location.address)
    print("Latitude:", location.latitude)
    print("Longitude:", location.longitude)
else:
    print("No location found.")
