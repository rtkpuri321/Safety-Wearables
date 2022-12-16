from django.shortcuts import render
from geopy.geocoders import Nominatim
import geocoder
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from googleplaces import GooglePlaces, types, lang
import requests
import json

# Create your views here.


def base(request):
    return render(request, "base.html")


def index(request):
    # importing geopy library
    g = geocoder.ip('me')
    print(g.latlng)
    geolocator = Nominatim(user_agent="geoapiExercises")
    # 30.367519
    # 76.381088
    location = geolocator.reverse(str(30.367519)+","+str(76.381088))
    print(location[0])
    placelst = []

    for i in location[0]:
        if i == ',':
            break
        # print(i)
        placelst.append(i)

    print(placelst)
    place = "".join(placelst)

    df = pd.read_csv("safety\punjab-crime-statistics.csv")
    # print(df)

    df1 = df[df["Division"] == place]
    df1 = df1[df["Year"] == 2021]
    # print(df1)

    df2 = df1["District"].drop_duplicates()
    df2.drop(df2.index[0], inplace=True)

    lst_district = list(df2)
    print(lst_district)

    # dft = df1[df1["District"] == "Prem Nagar"]
    # dft = dft[dft["Crime Type"] == "All Reported"]
    # print(dft["Crime No"])

    crimeno = []

    for i in lst_district:
        dft = df1[df1["District"] == i]
        dft = dft[dft["Crime Type"] == "All Reported"]
        a = list(dft["Crime No"])
        crimeno.append(a[0])
        print(a[0])

    print("crime no.:", crimeno)

    stat = pd.DataFrame()

    stat["District"] = lst_district

    stat["Crime No"] = crimeno

    print(stat)

    plt.switch_backend('agg')

    plt.pie(crimeno, labels=lst_district,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')

    # plt.show()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    ans1 = base64.b64encode(image_png)
    ans1 = ans1.decode('utf-8')
    buffer.flush()
    buffer.close()
    # Display
    print(location)
    return render(request, 'index.html', context={"loc": location, "pie": ans1})


def policestation(request):

    g = geocoder.ip('me')

    # API_KEY = "AIzaSyCNLxPxFmG3kfrALBUkRFb_R5UdemVnqqQ"

    # google_places = GooglePlaces(API_KEY)

    # g = geocoder.ip('me')
    # print(g.latlng)
    # geolocator = Nominatim(user_agent="geoapiExercises")
    # # 30.367519
    # # 76.381088

    # query_result = google_places.nearby_search(
    #     # lat_lng ={'lat': 46.1667, 'lng': -1.15},
    #     lat_lng={'lat': #g.latlng[0] 30.367519, #g.latlng[1]'lng': 76.381088},
    #     radius=5000,

    #     types=[types.TYPE_POLICE])

    # # If any attributions related
    # # with search results print them
    # if query_result.has_attributions:
    #     print(query_result.html_attributions)

    # # Iterate over the search results
    # for place in query_result.places:
    #     print(place)
    #     # place.get_details()
    #     print(place.name)
    #     print("Latitude", place.geo_location['lat'])
    #     print("Longitude", place.geo_location['lng'])
    #     print()
    df = pd.read_csv("safety\policestation.csv")
    print(df["Police Station"][0])
    plcstation1_address = df["Police Station"][0]
    plcstation1_latitude = df["lat"][0]
    plcstation1_longitude = df["lng"][0]

    plcstation2_address = df["Police Station"][1]
    plcstation2_latitude = df["lat"][1]
    plcstation2_longitude = df["lng"][1]

    plcstation3_address = df["Police Station"][2]
    plcstation3_latitude = df["lat"][2]
    plcstation3_longitude = df["lng"][2]

    plcstation4_address = df["Police Station"][3]
    plcstation4_latitude = df["lat"][3]
    plcstation4_longitude = df["lng"][3]

    return render(request, 'policestation.html',
                  context={"place1": plcstation1_address, "lat1": plcstation1_latitude, "lng1": plcstation1_longitude,
                           "place2": plcstation2_address, "lat2": plcstation2_latitude, "lng2": plcstation2_longitude,
                           "place3": plcstation3_address, "lat3": plcstation3_latitude, "lng3": plcstation3_longitude,
                           "place4": plcstation4_address, "lat4": plcstation4_latitude, "lng4": plcstation4_longitude})
