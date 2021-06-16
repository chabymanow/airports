# Map creator program which mark all airport on the map all around the world
# The user can choose which kind of airports should be indicated
# The program select all appropriate  airports from a CSV file
# All airports will be mark and all marks containt the current airport`s data
# The datafile downloaded from https://datahub.io
# https://datahub.io/core/airport-codes
# Created by Chaby Manow
# chabymanow@gmail.com
import folium
import pandas

# Create template for the info popup
info = '''
<h5></h5>
Name: %s</br>
Type: %s</br>
Elevation: %sft</br>
<a href="https://www.google.com/search?q=%s", target='_blank'>Check on google</a>
'''

# Create dictionary of types
typeDic = {'heliport': 'Helicopter Airport', 'balloonport': 'Balloon Airfield',
'seaplane_base': 'Seaplane Airfield', 'small_airport': 'Small Airport',
'medium_airport': 'Medium Airport', 'large_airport': 'Large Airport', 'closed': 'Closed Airport'}

datas = pandas.read_csv('airport-codes_csv.csv') #Read airpotrs data from CSV file
# Convert the coordinates to list.
coords = []
coordList = list(datas['coordinates'])
for i in range(len(coordList)):
    coords.append(coordList[i].split(','))

# Print the menu
print('What kind of airport you want on the map?')
print('Please type a number from the list!')
print('0: Helicopter airport\n1: Balloon Airfield\n2: Seaplane Airfiel\n3: Small Airport\n4: Medium Airport\n5: Large Airport\n6: Closed Airport')

# Check to the user input is correct or not
cool = False
while cool != True:
    userChoice = input()
    if userChoice.isdecimal and userChoice in ['0', '1', '2', '3', '4', '5', '6']:
        cool = True
    else:
        print('Please choose from the list above!')

userChoice = int(userChoice)
keyList = list(typeDic)

# The user input was correct, start to create the markers
print('I`m searching all '+typeDic[keyList[userChoice]]+' for you...')

#Create the basic map. The center of the map is London, because why not?
map = folium.Map(location = [51.50440, -0.08621], tiles = "Stamen Terrain", zoom_start= 7)


# Create the folium feature group
AirPorts = folium.FeatureGroup(name = 'Large Airport locations')

counter = 0 # Just a counter of the airports on the map

# Set the unique marker. 
for i in range(datas.shape[0]):
    if datas.iloc[i, 1] == keyList[userChoice]:
        iframe = folium.IFrame(html = info % (datas.iloc[i,2], typeDic[keyList[userChoice]], str(datas.iloc[i,3]), datas.iloc[i,2]), width=300, height=150)
        AirPorts.add_child(folium.Marker(location=[coords[i][1], coords[i][0]], popup=folium.Popup(iframe), icon = folium.Icon(color = 'green')))
        counter += 1

# Add the markers to the map
map.add_child(AirPorts)
# #Add Layer Controll to the map
map.add_child(folium.LayerControl())
# #Save the map with all data
map.save('AirportsMap.html')
# Print out the message about the created HTML file
print(str(counter)+' airport found. Writed all to the AirportsMap.html file!')
