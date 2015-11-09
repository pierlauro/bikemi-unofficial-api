#!/usr/bin/env python
import re
import requests
import json

def get_int( string ):
    return int( re.search( r'\d+', string ).group() )

web_page = requests.get( 'https://www.bikemi.com/it/mappa-stazioni.aspx' ).content
json_string = web_page.split( 'create(Artem.Google.MarkersBehavior, ', 3 )[ 1 ].split( ', null, null, $get("station-map"));' )[ 0 ]
json_data = json.loads(json_string)

stations = [ ]
for station in json_data[ 'markerOptions' ]:
    station_data = { }
    station_split = re.compile(r'<.*?>').sub( '', station[ 'info' ].replace( '<li>', '\n<li>' ) ).split( '\n' )
    station_data[ 'id' ] = get_int( station_split[0] )
    station_data[ 'title' ] = station_split[ 0 ].split( ' - ', 1 )[ 1 ]
    station_data[ 'available_bikes' ] = get_int( station_split[ 1 ] )
    station_data[ 'available_electric_bikes' ] = get_int( station_split[ 2 ] )
    station_data[ 'available_racks' ] = get_int( station_split[3] )
    station_data[ 'position' ] = station[ 'position' ][ 'lat' ], station[ 'position' ][ 'lng' ]
    stations.append( station_data )

print json.dumps( stations )
