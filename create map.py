import folium  
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim  
import time  

# Function to get the file path from the user via command-line input  
def get_file_path():  
    file_path = input("Enter the full path to the file containing the cities: ")  
    return file_path  

# Initialize Nominatim API  
geolocator = Nominatim(user_agent="city_locator")  

# Get the file path from the user  
cities_file_path = get_file_path()  

if cities_file_path:  # Ensure a file was provided  
    # Read the list of cities from the provided text file  
    with open(cities_file_path, 'r') as file:  
        cities = [line.strip() for line in file.readlines() if line.strip()]  

    # Create a base map  
    map_center = [39.8283, -98.5795]  # Approximate center of the USA  
    mymap = folium.Map(location=map_center, zoom_start=4, tiles="CartoDB Positron")  

    marker_cluster = MarkerCluster().add_to(mymap)

    # Function to get coordinates of a city  
    def get_coordinates(city):  
        try:  
            location = geolocator.geocode(city)  
            if location:  # Check if location is found  
                return (location.latitude, location.longitude, location.address)  
            else:  
                print(f"{city} was not found.")  
                return None  
        except Exception as e:  
            print(f"Could not geocode {city}: {e}")  
            return None  

    # Loop through the cities and add them to the map  
    for city in cities:  
        print(f"Processing {city}...")  # Print progress  
        coords = get_coordinates(city)  
        if coords:  
            lat, lon, address = coords
            popup_html = f"<b>{city}</b><br>{address}"
            folium.Marker(  
                location=[lat, lon],  
                popup=popup_html,  
                icon=folium.Icon(color='blue', icon='info-sign')  
            ).add_to(marker_cluster)  
        time.sleep(1)  # Sleep to respect rate limiting  

    # Save the map to an HTML file  
    mymap.save("cities_map.html")  

    print("Map has been created and saved as 'cities_map.html'.")  
else:  
    print("No file was provided.")