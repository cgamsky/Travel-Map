import folium  
from geopy.geocoders import Nominatim  
import tkinter as tk  
from tkinter import filedialog  # Import filedialog to use it for file selection  
import time  

# Function to open a dialog box to select the file  
def get_file_path():  
    # Create a Tkinter root window (it won't be shown)  
    root = tk.Tk()  
    root.withdraw()  # Hide the root window  
    # Open a file dialog and return the selected file path  
    file_path = filedialog.askopenfilename(  
        title='Select a file containing the cities',  
        filetypes=[('Text Files', '*.txt')]  
    )  
    return file_path  

# Initialize Nominatim API  
geolocator = Nominatim(user_agent="city_locator")  

# Get the file path from the user  
cities_file_path = get_file_path()  

if cities_file_path:  # Ensure a file was selected  
    # Read the list of cities from the selected text file  
    with open(cities_file_path, 'r') as file:  
        cities = [line.strip() for line in file.readlines()]  

    # Create a base map  
    map_center = [39.8283, -98.5795]  # Approximate center of the USA  
    map_zoom = 4  
    mymap = folium.Map(location=map_center, zoom_start=map_zoom)  

    # Function to get coordinates of a city  
    def get_coordinates(city):  
        try:  
            location = geolocator.geocode(city)  
            if location:  # Check if location is found  
                return (location.latitude, location.longitude)  
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
            folium.Marker(  
                location=coords,  
                popup=city,  
                icon=folium.Icon(color='blue', icon='info-sign')  
            ).add_to(mymap)  
        time.sleep(1)  # Sleep to respect rate limiting  

    # Save the map to an HTML file  
    mymap.save("cities_map.html")  

    print("Map has been created and saved as 'cities_map.html'.")  
else:  
    print("No file was selected.")