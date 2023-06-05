import pymysql
import warnings
import pandas as pd
import datetime
import pytz
from local_settings import *
import logging

load_initial_data = False

lat_lon_dict = {
    "Hilo, Hawaii": {"lat": 19.724, "lon": -155.087},
    "Bedwell Bayfront Park": {"lat": 37.493, "lon": -122.173},
    "Urbana, Illinois": {"lat": 40.113, "lon": -88.211},
    "Lake Quannapowitt": {"lat": 42.514, "lon": -71.078},
    "Death Valley, CA": {"lat": 36.505, "lon": -117.079},
    "Mount Diablo State Park": {"lat": 37.882, "lon": -121.914},
    "Yosemite National Park": {"lat": 37.865, "lon": -119.538},
    "Fillmore, CA": {"lat": 34.399, "lon": -118.918},
    "Middletown, CA": {"lat": 38.752, "lon": -122.615},
    "Acton, CA": {"lat": 34.47, "lon": -118.197},
    "Adelanto, CA": {"lat": 34.583, "lon": -117.409},
    "Agoura, CA": {"lat": 34.143, "lon": -118.738},
    "Agoura Hills, CA": {"lat": 34.136, "lon": -118.775},
    "Alameda, CA": {"lat": 37.765, "lon": -122.242},
    "Alamo, CA": {"lat": 37.85, "lon": -122.032},
    "Albany, CA": {"lat": 37.887, "lon": -122.298},
    "Alhambra, CA": {"lat": 34.095, "lon": -118.127},
    "Aliso Viejo, CA": {"lat": 33.565, "lon": -117.727},
    "Allendale, CA": {"lat": 38.445, "lon": -121.943},
    "Altadena, CA": {"lat": 34.19, "lon": -118.131},
    "Alum Rock, CA": {"lat": 37.366, "lon": -121.827},
    "American Canyon, CA": {"lat": 38.175, "lon": -122.261},
    "Anaheim, CA": {"lat": 33.835, "lon": -117.914},
    "Antelope, CA": {"lat": 38.708, "lon": -121.33},
    "Antioch, CA": {"lat": 38.005, "lon": -121.806},
    "Apple Valley, CA": {"lat": 34.501, "lon": -117.186},
    "Arcadia, CA": {"lat": 34.14, "lon": -118.035},
    "Arnold, CA": {"lat": 38.255, "lon": -120.351},
    "Arroyo Grande, CA": {"lat": 35.119, "lon": -120.591},
    "Artesia, CA": {"lat": 33.866, "lon": -118.083},
    "Arvin, CA": {"lat": 35.209, "lon": -118.828},
    "Ashland, CA": {"lat": 37.695, "lon": -122.114},
    "Atascadero, CA": {"lat": 35.489, "lon": -120.671},
    "Atwater, CA": {"lat": 37.348, "lon": -120.609},
    "Auburn, CA": {"lat": 38.897, "lon": -121.077},
    "Avenal, CA": {"lat": 36.004, "lon": -120.129},
    "Avocado Heights, CA": {"lat": 34.036, "lon": -117.991},
    "Azusa, CA": {"lat": 34.134, "lon": -117.908},
    "Bakersfield, CA": {"lat": 35.373, "lon": -119.019},
    "Baldwin Park, CA": {"lat": 34.085, "lon": -117.961},
    "Banning, CA": {"lat": 33.926, "lon": -116.876},
    "Barstow, CA": {"lat": 34.899, "lon": -117.023},
    "Barstow Heights, CA": {"lat": 34.87, "lon": -117.056},
    "Bay Point, CA": {"lat": 38.029, "lon": -121.962},
    "Beaumont, CA": {"lat": 33.929, "lon": -116.977},
    "Bell, CA": {"lat": 33.978, "lon": -118.187},
    "Bell Gardens, CA": {"lat": 33.965, "lon": -118.151},
    "Bellflower, CA": {"lat": 33.882, "lon": -118.117},
    "Belmont, CA": {"lat": 37.52, "lon": -122.276},
    "Benicia, CA": {"lat": 38.049, "lon": -122.159},
    "Berkeley, CA": {"lat": 37.872, "lon": -122.273},
    "Beverly Hills, CA": {"lat": 34.074, "lon": -118.4},
    "Bloomington, CA": {"lat": 34.07, "lon": -117.396},
    "Blythe, CA": {"lat": 33.61, "lon": -114.596},
    "Bostonia, CA": {"lat": 32.808, "lon": -116.936},
    "Brawley, CA": {"lat": 32.979, "lon": -115.53},
    "Brea, CA": {"lat": 33.917, "lon": -117.9},
    "Brentwood, CA": {"lat": 37.927, "lon": -121.726},
    "Bridgeport, CA": {"lat": 38.256, "lon": -119.231},
    "Buena Park, CA": {"lat": 33.868, "lon": -117.998},
    "Burbank, CA": {"lat": 34.181, "lon": -118.309},
    "Burbank, CA": {"lat": 37.323, "lon": -121.932},
    "Burlingame, CA": {"lat": 37.584, "lon": -122.366},
    "Calabasas, CA": {"lat": 34.158, "lon": -118.638},
    "Calexico, CA": {"lat": 32.679, "lon": -115.499},
    "Camarillo, CA": {"lat": 34.216, "lon": -119.038},
    "Cameron Park, CA": {"lat": 38.669, "lon": -120.987},
    "Campbell, CA": {"lat": 37.287, "lon": -121.95},
    "Canyon Lake, CA": {"lat": 33.685, "lon": -117.273},
    "Carbondale, CA": {"lat": 38.409, "lon": -121.007},
    "Carlsbad, CA": {"lat": 33.158, "lon": -117.351},
    "Carmichael, CA": {"lat": 38.617, "lon": -121.328},
    "Carson, CA": {"lat": 33.831, "lon": -118.282},
    "Castaic, CA": {"lat": 34.489, "lon": -118.623},
    "Castro Valley, CA": {"lat": 37.694, "lon": -122.086},
    "Cathedral City, CA": {"lat": 33.78, "lon": -116.465},
    "Ceres, CA": {"lat": 37.595, "lon": -120.958},
    "Cerritos, CA": {"lat": 33.858, "lon": -118.065},
    "Chico, CA": {"lat": 39.728, "lon": -121.837},
    "Chino, CA": {"lat": 34.012, "lon": -117.689},
    "Chino Hills, CA": {"lat": 33.994, "lon": -117.759},
    "Chowchilla, CA": {"lat": 37.123, "lon": -120.26},
    "Chula Vista, CA": {"lat": 32.64, "lon": -117.084},
    "Citrus Heights, CA": {"lat": 38.707, "lon": -121.281},
    "Claremont, CA": {"lat": 34.097, "lon": -117.72},
    "Clayton, CA": {"lat": 37.941, "lon": -121.936},
    "Clearlake, CA": {"lat": 38.958, "lon": -122.626},
    "Clovis, CA": {"lat": 36.825, "lon": -119.703},
    "Coachella, CA": {"lat": 33.68, "lon": -116.174},
    "Collierville, CA": {"lat": 38.215, "lon": -121.269},
    "Colton, CA": {"lat": 34.074, "lon": -117.314},
    "Columbia, CA": {"lat": 38.036, "lon": -120.401},
    "Compton, CA": {"lat": 33.896, "lon": -118.22},
    "Concord, CA": {"lat": 37.978, "lon": -122.031},
    "Corcoran, CA": {"lat": 36.098, "lon": -119.56},
    "Corona, CA": {"lat": 33.875, "lon": -117.566},
    "Coronado, CA": {"lat": 32.686, "lon": -117.183},
    "Costa Mesa, CA": {"lat": 33.641, "lon": -117.919},
    "Country Club, CA": {"lat": 37.969, "lon": -121.341},
    "Covina, CA": {"lat": 34.09, "lon": -117.89},
    "Cudahy, CA": {"lat": 33.961, "lon": -118.185},
    "Culver City, CA": {"lat": 34.021, "lon": -118.396},
    "Cupertino, CA": {"lat": 37.323, "lon": -122.032},
    "Cutler, CA": {"lat": 36.523, "lon": -119.287},
    "Cypress, CA": {"lat": 33.817, "lon": -118.037},
    "Daly City, CA": {"lat": 37.706, "lon": -122.462},
    "Dana Point, CA": {"lat": 33.467, "lon": -117.698},
    "Danville, CA": {"lat": 37.822, "lon": -122.0},
    "Davis, CA": {"lat": 38.545, "lon": -121.741},
    "Deer Park, CA": {"lat": 38.682, "lon": -120.823},
    "Deer Park, CA": {"lat": 38.533, "lon": -122.47},
    "Del Rio, CA": {"lat": 37.744, "lon": -121.012},
    "Delano, CA": {"lat": 35.769, "lon": -119.247},
    "Desert Hot Springs, CA": {"lat": 33.961, "lon": -116.502},
    "Diamond Bar, CA": {"lat": 34.029, "lon": -117.81},
    "Dinuba, CA": {"lat": 36.543, "lon": -119.387},
    "Dixon, CA": {"lat": 38.445, "lon": -121.823},
    "Downey, CA": {"lat": 33.94, "lon": -118.133},
    "Duarte, CA": {"lat": 34.139, "lon": -117.977},
    "Dublin, CA": {"lat": 37.702, "lon": -121.936},
    "Durham, CA": {"lat": 39.646, "lon": -121.8},
    "East Rancho Dominguez, CA": {"lat": 33.898, "lon": -118.195},
    "East Hemet, CA": {"lat": 33.74, "lon": -116.939},
    "East Los Angeles, CA": {"lat": 34.024, "lon": -118.172},
    "East Palo Alto, CA": {"lat": 37.469, "lon": -122.141},
    "Easton, CA": {"lat": 36.65, "lon": -119.791},
    "El Cajon, CA": {"lat": 32.795, "lon": -116.963},
    "El Centro, CA": {"lat": 32.792, "lon": -115.563},
    "El Cerrito, CA": {"lat": 37.916, "lon": -122.312},
    "El Dorado Hills, CA": {"lat": 38.686, "lon": -121.082},
    "El Monte, CA": {"lat": 34.069, "lon": -118.028},
    "El Segundo, CA": {"lat": 33.919, "lon": -118.416},
    "Elk Grove, CA": {"lat": 38.409, "lon": -121.372},
    "Encinitas, CA": {"lat": 33.037, "lon": -117.292},
    "Escondido, CA": {"lat": 33.119, "lon": -117.086},
    "Fair Oaks, CA": {"lat": 38.645, "lon": -121.272},
    "Fairfield, CA": {"lat": 38.249, "lon": -122.04},
    "Fallbrook, CA": {"lat": 33.376, "lon": -117.251},
    "Florin, CA": {"lat": 38.496, "lon": -121.409},
    "Folsom, CA": {"lat": 38.678, "lon": -121.176},
    "Fontana, CA": {"lat": 34.092, "lon": -117.435},
    "Foothill Farms, CA": {"lat": 38.679, "lon": -121.351},
    "Fort Bragg, CA": {"lat": 39.446, "lon": -123.805},
    "Foster City, CA": {"lat": 37.559, "lon": -122.271},
    "Fountain Valley, CA": {"lat": 33.709, "lon": -117.954},
    "Fremont, CA": {"lat": 37.548, "lon": -121.989},
    "Fresno, CA": {"lat": 36.748, "lon": -119.772},
    "Fullerton, CA": {"lat": 33.87, "lon": -117.925},
    "Galt, CA": {"lat": 38.255, "lon": -121.3},
    "Garden Grove, CA": {"lat": 33.774, "lon": -117.941},
    "Gardena, CA": {"lat": 33.888, "lon": -118.309},
    "Georgetown, CA": {"lat": 38.907, "lon": -120.839},
    "Gilroy, CA": {"lat": 37.006, "lon": -121.568},
    "Glen Avon, CA": {"lat": 34.012, "lon": -117.485},
    "Glendale, CA": {"lat": 34.143, "lon": -118.255},
    "Glendora, CA": {"lat": 34.136, "lon": -117.865},
    "Goleta, CA": {"lat": 34.436, "lon": -119.828},
    "Goshen, CA": {"lat": 36.351, "lon": -119.42},
    "Granite Bay, CA": {"lat": 38.763, "lon": -121.164},
    "Green Valley, CA": {"lat": 34.622, "lon": -118.414},
    "Green Valley, CA": {"lat": 38.253, "lon": -122.162},
    "Greenfield, CA": {"lat": 35.269, "lon": -119.003},
    "Greenfield, CA": {"lat": 36.321, "lon": -121.244},
    "Hacienda Heights, CA": {"lat": 33.993, "lon": -117.969},
    "Hanford, CA": {"lat": 36.327, "lon": -119.646},
    "Hawthorne, CA": {"lat": 33.916, "lon": -118.353},
    "Hayward, CA": {"lat": 37.669, "lon": -122.081},
    "Hemet, CA": {"lat": 33.748, "lon": -116.972},
    "Hercules, CA": {"lat": 38.017, "lon": -122.289},
    "Hermosa Beach, CA": {"lat": 33.862, "lon": -118.4},
    "Hesperia, CA": {"lat": 34.426, "lon": -117.301},
    "Highland, CA": {"lat": 34.128, "lon": -117.209},
    "Hollister, CA": {"lat": 36.852, "lon": -121.402},
    "Hollywood, CA": {"lat": 34.098, "lon": -118.327},
    "Huntington Beach, CA": {"lat": 33.66, "lon": -117.999},
    "Huntington Park, CA": {"lat": 33.982, "lon": -118.225},
    "Imperial Beach, CA": {"lat": 32.584, "lon": -117.113},
    "Indio, CA": {"lat": 33.721, "lon": -116.216},
    "Inglewood, CA": {"lat": 33.962, "lon": -118.353},
    "Irvine, CA": {"lat": 33.669, "lon": -117.823},
    "Jackson, CA": {"lat": 38.349, "lon": -120.774},
    "Jamestown, CA": {"lat": 37.953, "lon": -120.423},
    "Lafayette, CA": {"lat": 37.886, "lon": -122.118},
    "Lake Forest, CA": {"lat": 33.647, "lon": -117.689},
    "Lakeside, CA": {"lat": 32.857, "lon": -116.922},
    "Lakewood, CA": {"lat": 33.854, "lon": -118.134},
    "Lancaster, CA": {"lat": 34.698, "lon": -118.137},
    "Largo, CA": {"lat": 39.022, "lon": -123.13},
    "Lincoln, CA": {"lat": 38.892, "lon": -121.293},
    "Linden, CA": {"lat": 38.021, "lon": -121.084},
    "Livingston, CA": {"lat": 37.387, "lon": -120.724},
    "Lodi, CA": {"lat": 38.13, "lon": -121.272},
    "Loma Linda, CA": {"lat": 34.048, "lon": -117.261},
    "Lomita, CA": {"lat": 33.792, "lon": -118.315},
    "Lompoc, CA": {"lat": 34.639, "lon": -120.458},
    "Long Beach, CA": {"lat": 33.767, "lon": -118.189},
    "Los Altos, CA": {"lat": 37.385, "lon": -122.114},
    "Los Angeles, CA": {"lat": 34.052, "lon": -118.244},
    "Los Banos, CA": {"lat": 37.058, "lon": -120.85},
    "Los Gatos, CA": {"lat": 37.227, "lon": -121.975},
    "Lynwood, CA": {"lat": 33.93, "lon": -118.211},
    "Madera, CA": {"lat": 36.961, "lon": -120.061},
    "Manhattan Beach, CA": {"lat": 33.885, "lon": -118.411},
    "Manteca, CA": {"lat": 37.797, "lon": -121.216},
    "Maricopa, CA": {"lat": 35.059, "lon": -119.401},
    "Marina, CA": {"lat": 36.684, "lon": -121.802},
    "Martinez, CA": {"lat": 38.019, "lon": -122.134},
    "Marysville, CA": {"lat": 39.146, "lon": -121.591},
    "Maywood, CA": {"lat": 33.987, "lon": -118.185},
    "Mead Valley, CA": {"lat": 33.833, "lon": -117.296},
    "Menifee, CA": {"lat": 33.728, "lon": -117.146},
    "Menlo Park, CA": {"lat": 37.454, "lon": -122.182},
    "Merced, CA": {"lat": 37.302, "lon": -120.483},
    "Middleton, CA": {"lat": 38.207, "lon": -122.263},
    "Millbrae, CA": {"lat": 37.599, "lon": -122.387},
    "Milpitas, CA": {"lat": 37.428, "lon": -121.907},
    "Mission Viejo, CA": {"lat": 33.6, "lon": -117.672},
    "Modesto, CA": {"lat": 37.639, "lon": -120.997},
    "Monrovia, CA": {"lat": 34.148, "lon": -117.999},
    "Montclair, CA": {"lat": 34.078, "lon": -117.69},
    "Montebello, CA": {"lat": 34.009, "lon": -118.105},
    "Monterey, CA": {"lat": 36.6, "lon": -121.895},
    "Monterey Park, CA": {"lat": 34.063, "lon": -118.123},
    "Moorpark, CA": {"lat": 34.286, "lon": -118.882},
    "Moraga, CA": {"lat": 37.835, "lon": -122.13},
    "Moreno Valley, CA": {"lat": 33.938, "lon": -117.231},
    "Morgan Hill, CA": {"lat": 37.131, "lon": -121.654},
    "Mountain View, CA": {"lat": 38.009, "lon": -122.117},
    "Mountain View, CA": {"lat": 37.386, "lon": -122.084},
    "Murrieta, CA": {"lat": 33.554, "lon": -117.214},
    "Napa, CA": {"lat": 38.297, "lon": -122.286},
    "National City, CA": {"lat": 32.678, "lon": -117.099},
    "Newark, CA": {"lat": 37.53, "lon": -122.04},
    "Newport Beach, CA": {"lat": 33.619, "lon": -117.929},
    "Nipomo, CA": {"lat": 35.043, "lon": -120.476},
    "Norco, CA": {"lat": 33.931, "lon": -117.549},
    "North Glendale, CA": {"lat": 34.161, "lon": -118.265},
    "North Highlands, CA": {"lat": 38.686, "lon": -121.372},
    "Norwalk, CA": {"lat": 33.902, "lon": -118.082},
    "Novato, CA": {"lat": 38.107, "lon": -122.57},
    "Oak Hill, CA": {"lat": 34.065, "lon": -118.785},
    "Oak Park, CA": {"lat": 34.179, "lon": -118.763},
    "Oakdale, CA": {"lat": 37.767, "lon": -120.847},
    "Oakland, CA": {"lat": 37.804, "lon": -122.271},
    "Oakley, CA": {"lat": 37.997, "lon": -121.712},
    "Oceanside, CA": {"lat": 33.196, "lon": -117.379},
    "Oildale, CA": {"lat": 35.42, "lon": -119.02},
    "Ontario, CA": {"lat": 34.063, "lon": -117.651},
    "Orange, CA": {"lat": 33.788, "lon": -117.853},
    "Orangevale, CA": {"lat": 38.679, "lon": -121.226},
    "Orcutt, CA": {"lat": 34.865, "lon": -120.436},
    "Orinda, CA": {"lat": 37.877, "lon": -122.18},
    "Oroville, CA": {"lat": 39.514, "lon": -121.556},
    "Oxnard, CA": {"lat": 34.197, "lon": -119.177},
    "Oxnard Shores, CA": {"lat": 34.191, "lon": -119.242},
    "Pacifica, CA": {"lat": 37.614, "lon": -122.487},
    "Pacific Grove, CA": {"lat": 36.618, "lon": -121.917},
    "Palm Desert, CA": {"lat": 33.722, "lon": -116.374},
    "Palm Springs, CA": {"lat": 33.83, "lon": -116.545},
    "Palmdale, CA": {"lat": 34.579, "lon": -118.116},
    "Palo Alto, CA": {"lat": 37.442, "lon": -122.143},
    "Paradise, CA": {"lat": 39.76, "lon": -121.622},
    "Paramount, CA": {"lat": 33.889, "lon": -118.16},
    "Pasadena, CA": {"lat": 34.148, "lon": -118.145},
    "Paso Robles, CA": {"lat": 35.627, "lon": -120.691},
    "Patterson, CA": {"lat": 37.472, "lon": -121.13},
    "Perris, CA": {"lat": 33.783, "lon": -117.229},
    "Petaluma, CA": {"lat": 38.232, "lon": -122.637},
    "Pico Rivera, CA": {"lat": 33.983, "lon": -118.097},
    "Pinole, CA": {"lat": 38.004, "lon": -122.299},
    "Pittsburg, CA": {"lat": 38.028, "lon": -121.885},
    "Placentia, CA": {"lat": 33.872, "lon": -117.87},
    "Pleasant Hill, CA": {"lat": 37.948, "lon": -122.061},
    "Pleasanton, CA": {"lat": 37.662, "lon": -121.875},
    "Plymouth, CA": {"lat": 38.482, "lon": -120.845},
    "Pomona, CA": {"lat": 34.055, "lon": -117.752},
    "Port Hueneme, CA": {"lat": 34.148, "lon": -119.195},
    "Porterville, CA": {"lat": 36.065, "lon": -119.017},
    "Poway, CA": {"lat": 32.963, "lon": -117.036},
    "Prunedale, CA": {"lat": 36.776, "lon": -121.67},
    "Quincy, CA": {"lat": 39.937, "lon": -120.947},
    "Ramona, CA": {"lat": 33.042, "lon": -116.868},
    "Rancho Cordova, CA": {"lat": 38.589, "lon": -121.303},
    "Rancho Cucamonga, CA": {"lat": 34.106, "lon": -117.593},
    "Rancho Mirage, CA": {"lat": 33.74, "lon": -116.413},
    "Rancho Palos Verdes, CA": {"lat": 33.744, "lon": -118.387},
    "Rancho San Diego, CA": {"lat": 32.747, "lon": -116.935},
    "Rancho Santa Margarita, CA": {"lat": 33.641, "lon": -117.603},
    "Redlands, CA": {"lat": 34.056, "lon": -117.183},
    "Redondo Beach, CA": {"lat": 33.849, "lon": -118.388},
    "Redwood City, CA": {"lat": 37.485, "lon": -122.236},
    "Reedley, CA": {"lat": 36.596, "lon": -119.45},
    "Rialto, CA": {"lat": 34.106, "lon": -117.37},
    "Richmond, CA": {"lat": 37.936, "lon": -122.348},
    "Ridgecrest, CA": {"lat": 35.622, "lon": -117.671},
    "Rio Linda, CA": {"lat": 38.691, "lon": -121.449},
    "Riverbank, CA": {"lat": 37.736, "lon": -120.935},
    "Riverdale, CA": {"lat": 36.431, "lon": -119.86},
    "Riverside, CA": {"lat": 33.953, "lon": -117.396},
    "Rocklin, CA": {"lat": 38.791, "lon": -121.236},
    "Rohnert Park, CA": {"lat": 38.34, "lon": -122.701},
    "Rosamond, CA": {"lat": 34.864, "lon": -118.163},
    "Rosedale, CA": {"lat": 35.384, "lon": -119.145},
    "Rosemead, CA": {"lat": 34.081, "lon": -118.073},
    "Rosemont, CA": {"lat": 38.552, "lon": -121.365},
    "Roseville, CA": {"lat": 38.752, "lon": -121.288},
    "Rowland Heights, CA": {"lat": 33.976, "lon": -117.905},
    "Rubidoux, CA": {"lat": 33.996, "lon": -117.406},
    "Sacramento, CA": {"lat": 38.582, "lon": -121.494},
    "Salinas, CA": {"lat": 36.678, "lon": -121.656},
    "San Bernardino, CA": {"lat": 34.108, "lon": -117.29},
    "San Bruno, CA": {"lat": 37.63, "lon": -122.411},
    "San Carlos, CA": {"lat": 37.507, "lon": -122.261},
    "San Clemente, CA": {"lat": 33.427, "lon": -117.612},
    "San Diego, CA": {"lat": 32.715, "lon": -117.157},
    "San Dimas, CA": {"lat": 34.107, "lon": -117.807},
    "San Fernando, CA": {"lat": 34.282, "lon": -118.439},
    "San Francisco, CA": {"lat": 37.775, "lon": -122.419},
    "San Gabriel, CA": {"lat": 34.096, "lon": -118.106},
    "San Jacinto, CA": {"lat": 33.784, "lon": -116.959},
    "San Jose, CA": {"lat": 37.339, "lon": -121.895},
    "San Juan Capistrano, CA": {"lat": 33.502, "lon": -117.663},
    "San Leandro, CA": {"lat": 37.725, "lon": -122.156},
    "San Lorenzo, CA": {"lat": 37.681, "lon": -122.124},
    "San Luis Obispo, CA": {"lat": 35.283, "lon": -120.66},
    "San Marcos, CA": {"lat": 33.143, "lon": -117.166},
    "San Mateo, CA": {"lat": 37.563, "lon": -122.326},
    "San Pablo, CA": {"lat": 37.962, "lon": -122.346},
    "San Pedro, CA": {"lat": 33.736, "lon": -118.292},
    "San Rafael, CA": {"lat": 37.974, "lon": -122.531},
    "San Ramon, CA": {"lat": 37.78, "lon": -121.978},
    "Sanger, CA": {"lat": 36.708, "lon": -119.556},
    "Santa Ana, CA": {"lat": 33.746, "lon": -117.868},
    "Santa Barbara, CA": {"lat": 34.421, "lon": -119.698},
    "Santa Clara, CA": {"lat": 37.354, "lon": -121.955},
    "Santa Clarita, CA": {"lat": 34.392, "lon": -118.543},
    "Santa Cruz, CA": {"lat": 36.974, "lon": -122.031},
    "Santa Fe Springs, CA": {"lat": 33.947, "lon": -118.085},
    "Santa Maria, CA": {"lat": 34.953, "lon": -120.436},
    "Santa Monica, CA": {"lat": 34.019, "lon": -118.491},
    "Santa Paula, CA": {"lat": 34.354, "lon": -119.059},
    "Santa Rosa, CA": {"lat": 38.44, "lon": -122.714},
    "Santee, CA": {"lat": 32.838, "lon": -116.974},
    "Saratoga, CA": {"lat": 37.264, "lon": -122.023},
    "Seal Beach, CA": {"lat": 33.741, "lon": -118.105},
    "Seaside, CA": {"lat": 36.611, "lon": -121.852},
    "Selma, CA": {"lat": 36.571, "lon": -119.612},
    "Shafter, CA": {"lat": 35.501, "lon": -119.272},
    "Sherman Oaks, CA": {"lat": 34.151, "lon": -118.449},
    "Simi Valley, CA": {"lat": 34.269, "lon": -118.781},
    "Soledad, CA": {"lat": 36.425, "lon": -121.326},
    "South El Monte, CA": {"lat": 34.052, "lon": -118.047},
    "South Gate, CA": {"lat": 33.955, "lon": -118.212},
    "South Lake Tahoe, CA": {"lat": 38.933, "lon": -119.984},
    "South Pasadena, CA": {"lat": 34.116, "lon": -118.15},
    "South San Francisco, CA": {"lat": 37.655, "lon": -122.408},
    "South San Jose Hills, CA": {"lat": 34.013, "lon": -117.905},
    "South Whittier, CA": {"lat": 33.961, "lon": -118.042},
    "South Yuba City, CA": {"lat": 39.117, "lon": -121.639},
    "Spring Valley, CA": {"lat": 32.745, "lon": -116.999},
    "Stanton, CA": {"lat": 33.803, "lon": -117.993},
    "Stockton, CA": {"lat": 37.958, "lon": -121.291},
    "Suisun, CA": {"lat": 38.238, "lon": -122.04},
    "Sun City, CA": {"lat": 33.709, "lon": -117.197},
    "Sun Valley, CA": {"lat": 34.217, "lon": -118.37},
    "Sunnyside, CA": {"lat": 36.749, "lon": -119.699},
    "Sunnyvale, CA": {"lat": 37.369, "lon": -122.036},
    "Temecula, CA": {"lat": 33.494, "lon": -117.148},
    "Temple City, CA": {"lat": 34.107, "lon": -118.058},
    "Thornton, CA": {"lat": 38.226, "lon": -121.425},
    "Thousand Oaks, CA": {"lat": 34.171, "lon": -118.838},
    "Torrance, CA": {"lat": 33.836, "lon": -118.341},
    "Tracy, CA": {"lat": 37.74, "lon": -121.425},
    "Truckee, CA": {"lat": 39.328, "lon": -120.183},
    "Tulare, CA": {"lat": 36.208, "lon": -119.347},
    "Turlock, CA": {"lat": 37.495, "lon": -120.847},
    "Tustin, CA": {"lat": 33.746, "lon": -117.826},
    "North Tustin, CA": {"lat": 33.764, "lon": -117.794},
    "Twentynine Palms, CA": {"lat": 34.136, "lon": -116.054},
    "Ukiah, CA": {"lat": 39.15, "lon": -123.208},
    "Union City, CA": {"lat": 37.596, "lon": -122.019},
    "Universal City, CA": {"lat": 34.139, "lon": -118.353},
    "Upland, CA": {"lat": 34.098, "lon": -117.648},
    "Villa Park, CA": {"lat": 33.814, "lon": -117.813},
    "Walnut Park, CA": {"lat": 33.968, "lon": -118.225},
    "Waterford, CA": {"lat": 37.641, "lon": -120.76},
    "Watsonville, CA": {"lat": 36.91, "lon": -121.757},
    "West Carson, CA": {"lat": 33.822, "lon": -118.293},
    "West Covina, CA": {"lat": 34.069, "lon": -117.939},
    "West Hollywood, CA": {"lat": 34.09, "lon": -118.362},
    "West Puente Valley, CA": {"lat": 34.052, "lon": -117.968},
    "West Sacramento, CA": {"lat": 38.58, "lon": -121.53},
    "Westminster, CA": {"lat": 33.759, "lon": -118.007},
    "Westmont, CA": {"lat": 33.941, "lon": -118.302},
    "Whittier, CA": {"lat": 33.979, "lon": -118.033},
    "Wildomar, CA": {"lat": 33.599, "lon": -117.28},
    "Willowbrook, CA": {"lat": 33.917, "lon": -118.255},
    "Wilton, CA": {"lat": 38.412, "lon": -121.272},
    "Winchester, CA": {"lat": 33.707, "lon": -117.084},
    "Windsor, CA": {"lat": 38.547, "lon": -122.816},
    "Winter Gardens, CA": {"lat": 32.831, "lon": -116.933},
    "Woodbridge, CA": {"lat": 38.154, "lon": -121.301},
    "Woodland, CA": {"lat": 38.679, "lon": -121.773},
    "Yorba Linda, CA": {"lat": 33.889, "lon": -117.813},
    "Yuba City, CA": {"lat": 39.14, "lon": -121.617},
    "Yucaipa, CA": {"lat": 34.034, "lon": -117.043},
    "Yucca Valley, CA": {"lat": 34.114, "lon": -116.432},
    "Sheridan, CA": {"lat": 38.98, "lon": -121.376},
    "Wasco, CA": {"lat": 35.594, "lon": -119.341},
    "Anderson, CA": {"lat": 40.448, "lon": -122.298},
    "Arcata, CA": {"lat": 40.867, "lon": -124.083},
    "Bayside, CA": {"lat": 40.842, "lon": -124.064},
    "Bella Vista, CA": {"lat": 40.641, "lon": -122.232},
    "Chester, CA": {"lat": 40.306, "lon": -121.232},
    "Eureka, CA": {"lat": 40.802, "lon": -124.164},
    "Ferndale, CA": {"lat": 40.576, "lon": -124.264},
    "Greenville, CA": {"lat": 40.14, "lon": -120.951},
    "Janesville, CA": {"lat": 40.297, "lon": -120.524},
    "Lewiston, CA": {"lat": 40.707, "lon": -122.808},
    "McKinleyville, CA": {"lat": 40.947, "lon": -124.101},
    "Pine Hills, CA": {"lat": 40.733, "lon": -124.152},
    "Redding, CA": {"lat": 40.587, "lon": -122.392},
    "Susanville, CA": {"lat": 40.416, "lon": -120.653},
    "Vineyard, CA": {"lat": 38.464, "lon": -121.347},
    "Arden-Arcade, CA": {"lat": 38.603, "lon": -121.379},
    "Casa de Oro-Mount Helix, CA": {"lat": 32.764, "lon": -116.969},
    "Florence-Graham, CA": {"lat": 33.968, "lon": -118.244},
    "La Crescenta-Montrose, CA": {"lat": 34.232, "lon": -118.235},
    "West Whittier-Los Nietos, CA": {"lat": 33.976, "lon": -118.069},
    "West Hills, CA": {"lat": 34.197, "lon": -118.644}
}


location_names = [x for x in lat_lon_dict.keys()]

# connect to sql
def getSQLConn(host, user, password):
    return pymysql.connect(host=host, user=user, passwd=password, autocommit=True)


createSchema = "CREATE SCHEMA IF NOT EXISTS rain;"

createTblFactLatLon = """CREATE TABLE IF NOT EXISTS rain.tblFactLatLon
    (`dt` INT(11) NOT NULL COMMENT 'unixtimestamp of last api data update',
    `requested_dt` INT(11) NOT NULL COMMENT 'unixtimestamp of last api data request',
    `location_name` VARCHAR(255) NOT NULL COMMENT 'label given for latitude longitude coordinate (e.g. Bedwell Bayfront Park)',
    `lat` DECIMAL(7,3) SIGNED NOT NULL COMMENT 'latitude coordinate',
    `lon` DECIMAL(7,3) SIGNED NOT NULL COMMENT 'longitude coordinate',
    `rain_1h` DECIMAL(5,1) NOT NULL COMMENT 'mm rainfall in last hour',
    `rain_3h` DECIMAL(5,1) NOT NULL COMMENT 'mm rainfall in last 3 hours', 
    PRIMARY KEY (`dt`,`lat`,`lon`,`requested_dt`)) 
    ENGINE=InnoDB DEFAULT CHARSET=latin1;"""

mysql_conn = getSQLConn(MYSQL_AUTH["host"], MYSQL_AUTH["user"], MYSQL_AUTH["password"])

with mysql_conn.cursor() as cursor:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cursor.execute(createSchema)
        cursor.execute(createTblFactLatLon)
        
 # run query
def runQuery(mysql_conn, query):
    with mysql_conn.cursor() as cursor:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cursor.execute(query)


def unixtime_to_pacific_datetime(unixtime_timestamp):
    # Create a timezone object for the Pacific timezone
    pacific_timezone = pytz.timezone("US/Pacific")
    # Convert the Unix timestamp to a datetime object in UTC timezone
    utc_datetime = datetime.datetime.utcfromtimestamp(unixtime_timestamp)

    # Convert the UTC datetime object to the Pacific timezone
    output = pacific_timezone.localize(utc_datetime).astimezone(pacific_timezone)
    return str(output)


if load_initial_data == True:
    df = pd.read_csv("initial_data.csv").fillna(0)
    requested_dt = 1683435668
    for index, row in df.iterrows():
        query = (
            "INSERT IGNORE INTO rain.tblFactLatLon(dt, requested_dt, location_name, lat, lon, rain_1h, rain_3h) VALUES (%i, %i, '%s', %.3f, %.3f, %.1f, %.1f)"
            % (
                row["dt"],
                requested_dt,
                row["city_name"],
                row["lat"],
                row["lon"],
                row["rain_1h"],
                row["rain_3h"],
            )
        )
        logging.info("query=%s" % (query))
        runQuery(mysql_conn, query)
        logging.info(
            "%s - %s - %s - %s - %s - %s - %s"
            % (
                row["dt"],
                requested_dt,
                row["city_name"],
                row["lat"],
                row["lon"],
                row["rain_1h"],
                row["rain_3h"],
            )
        )
    logging.info("finished preload")
