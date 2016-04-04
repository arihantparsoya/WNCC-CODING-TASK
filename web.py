import math
import json, requests
import copy
from math import radians, cos, sin, asin, sqrt
import sys

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


raw_data = open(sys.argv[1], 'r') # opening the passwd file
f = raw_data.read()
rows = f.split('\n') # splitting the input text file by each line
data_filtered_after_spaces = [] # array which stores the input text data after replacing spaces with '+'

for row in rows:
    split_row = row.replace(" ","+") # replacing spaces with '+'
    data_filtered_after_spaces.append(split_row)

print (data_filtered_after_spaces)

distance = [] #stores the distance between the places with unwanted additional text data
final_distance = [] #array which stores the text data after removing the unwanted texts and convertng text to float
sorted_final_distance = [] # sorted array of the final_distance array
destination_coordinates = [] # array which stores the latitudes and longitues of the destination point
starting_location_coordinates = [] # array which stores the latitudes and longitudes of starting location
places_which_cannot_be_acessed_by_foot = []
for places in range(len(data_filtered_after_spaces)):
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + 'Indian+Institute+of+Technology+Bombay' + '&destination=' + data_filtered_after_spaces[places]
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    try: # to append distance if the destination can be reached by foot 
        distance.append(data['routes'][0]['legs'][0]['distance']['text'])
        destination_coordinates.append(data['routes'][0]['legs'][0]['end_location'])
        starting_location_coordinates = (data['routes'][0]['legs'][0]['start_location'])
        distance[places] = distance[places][:-3]
        distance[places] = distance[places].replace(",","")
        final_distance.append(float(distance[places]))
    except IndexError:
        places_which_cannot_be_acessed_by_foot.append(data_filtered_after_spaces[places])


sorted_final_distance = copy.deepcopy(final_distance)
sorted_final_distance.sort()
print ('Destinations in ascending order:')

for places in range(len(distance)): # replacing '+' with '  ' and printing
    data_filtered_after_spaces[final_distance.index(sorted_final_distance[places])] = data_filtered_after_spaces[final_distance.index(sorted_final_distance[places])].replace("+"," ")
    print data_filtered_after_spaces[final_distance.index(sorted_final_distance[places])]

for places in range(len(places_which_cannot_be_acessed_by_foot)): # replacing '+' with '  ' and printing the places which cannot be reached by foot
    places_which_cannot_be_acessed_by_foot[places] = places_which_cannot_be_acessed_by_foot[places].replace('+',' ')
    print places_which_cannot_be_acessed_by_foot[places]

'''
***********
the below code is to find point to point distance between two points on the globe
***********
'''
print ('')
print ('point to point distances:')
print ('')
for places in range(len(destination_coordinates)):
    lon1 = starting_location_coordinates['lng']
    lat1 = starting_location_coordinates['lat']
    lat2 = destination_coordinates[places]['lat']
    lon2 = destination_coordinates[places]['lng']
    print (data_filtered_after_spaces[places], ':' , haversine(lon1,lat1,lon2,lat2), 'km')
