import numpy as np
import json
import sys
import requests
from math import sin, cos, sqrt, atan2, radians
import configparser

########################  Constants  ################################
R_EARTH = 6373.0 # approximate radius of earth in km
LAT_IDX = 'lat'
LON_IDX = 'lng'

#####################  Configuration  ##############################
config = configparser.ConfigParser()
config.read('keys.ini')

google_api_keys = [config['google']['key_1']]



#####################################################################
#           Function to obtain distance between two points          #
# @param point_a (tuple)                                            #
# @param point_b (tuple)                                            #
#####################################################################
def get_distance(point_a, point_b):
    lon1 = radians(point_a[LON_IDX])
    lon2 = radians(point_b[LON_IDX])
    lat1 = radians(point_a[LAT_IDX])
    lat2 = radians(point_b[LAT_IDX])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R_EARTH * c



#####################################################################
#           Function to sort by distance                            #
# @param result_json (json result from  google maps)                #
# @param point_a (tuple)                                            #
#####################################################################
def sort_by_distance(result_json, point_a):
    result_list = []
    for item in result_json['results']:
        point_b =  item['geometry']['location']
        distance_to_a =  get_distance(point_a, point_b)
        item_dict = {}
        item_dict['item'] = item
        item_dict['distance_to_a'] = distance_to_a
        result_list.append(item_dict)
    new_list = sorted (result_list, key = lambda k: k['distance_to_a'])
    return [(item['item']['geometry']['location'], item['item']['name'] )for item in new_list]



#####################################################################
#           Function to search bansefi branches by lat and lon      #
# @param lon (float)                                                #
# @param lat (float)                                                #
# @param atm (bolean)                                               #
# @param radius (number)                                            #
#####################################################################
def get_bansefi_branch_by_loc(lon, lat,atm ,radius=20000):
    point_a =  {LAT_IDX: lat, LON_IDX: lon}
    if atm :
        base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=%d&keyword=bansefi&type=atm&key=%s'
    else:
        base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=%d&keyword=bansefi&type=bank&key=%s'
    full_url = base_url%(str(point_a[LAT_IDX]),str(point_a[LON_IDX]),radius, google_api_keys[0])
    r = requests.get(full_url)
    result_json = r.json()
    result_list = sort_by_distance(result_json, point_a)
    return result_list

#####################################################################
#            Main function to search by locality                    #
# @param lon (float)                                                #
# @param lat (float)                                                #
# @param atm (bolean)                                               #
# @param radius (number)                                            #
#####################################################################
def get_bansefi (lon, lat,atm = False ,radius = 20000):
    result = get_bansefi_branch_by_loc( lon, lat, atm, radius)
    for i in result:
        print i








