import sys
import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
import geopy.distance
from dateutil import parser
from csv import writer
import os


def menu(location):
    data = pd.read_csv(location)
    Longitude = data.ISSLongitude
    Latitude = data.ISSLatitude
    Elevation = data.ISSElevation
    Magnetometer = data.MagMagnitude
    MagX = data.MagX
    MagY = data.MagY
    MagZ = data.MagZ
    DateTime = data.DateTime
    os.system("cls")
    print("--------------------------------MENU------------------------------------")
    print("1) Plot graph of raw magnetic field strength against distance travelled")
    print("2) Format longitude and latitude from degrees to decimal")
    print("3) Get distance travelled of the ISS from longitude and latitude")
    print("4) Create univariate interpolated spline of raw data and plot graph")
    print("5) Plot graph of elevation against time")
    print("6) Plot magnetic field strength against time")
    print("7) Plot magnetic field strength in 3D")
    print("8) End program")
    UserChoice = input("Enter your choice: ")
    if UserChoice == "1":
        option1(Magnetometer,location)
    elif UserChoice == "2":
        option2(Longitude, Latitude, location)
    elif UserChoice == "3":
        option3(Latitude, Longitude, location)
    elif UserChoice == "4":
        option4(Magnetometer, location)
    elif UserChoice == "5":
        option5(Elevation, DateTime, location)
    elif UserChoice == "6":
        option6(DateTime,Magnetometer, location)
    elif UserChoice == "7":
        option7(MagX,MagY,MagZ,location)
    elif UserChoice == "8":
        sys.exit()


def option1(Magnetometer,Location):
    data = pd.read_csv(location)
    DistanceTravelled = data.DistanceTravelled
    plt.plot(DistanceTravelled, Magnetometer, label="Raw Data")
    plt.xlabel("Distance Travelled / 1000 km")
    plt.ylabel("Magnetic Field Strength / T")
    plt.legend()
    plt.show()
    menu(Location)


def option2(Longitude, Latitude,Location):
    Distance = []
    for i in range(1, len(Longitude)):
        x = []
        data = []
        y = []
        x = Longitude[i].split(" ")
        y = Latitude[i].split(" ")
        z = x[2]
        z = z[:-1]
        b = y[2]
        b = b[:-1]
        DecimalLongitude = (float(x[0].replace("deg", "")) + float(x[1].replace("'", "")) / 60 + float(z) / (60 * 60))
        DecimalLatitude = (float(y[0].replace("deg", "")) + float(y[1].replace("'", "")) / 60 + float(b) / (60 * 60))
        data.append(DecimalLatitude)
        data.append(DecimalLongitude)
        with open('Longitude&Latitude.csv', 'a', buffering=1, newline='') as f:
            data_writer = writer(f)
            data_writer.writerow(data)
    menu(Location)


def option3(Latitude, Longitude,Location):
    Distance = []
    for i in range(1, len(Longitude)):
        Distance.append(Distance[i - 1] + geopy.distance.geodesic((Latitude[i - 1], Longitude[i - 1]),
                                                                  (Latitude[i], Longitude[i])).km)
    for i in range(0, len(Distance)):
        with open("DistanceTravelled", "a", buffering=1, newline=" ") as f:
            DataWriter = writer(f)
            DataWriter.writerow(Distance[i])
    menu(Location)

def option4(Magnetometer,Location):
    data = pd.read_csv(location)
    DistanceTravelled = data.DistanceTravelled
    spl = UnivariateSpline(DistanceTravelled, Magnetometer, k=5)
    xs = np.linspace(0, 182, 1000)
    plt.xlabel("Distance Travelled / 1000 km")
    plt.ylabel("Magnetic Field Strength / T")
    plt.plot(xs, spl(xs), label="Fitted Line")
    plt.legend()
    plt.show()
    menu(Location)

def option5(Elevation, DateTime,Location):
    FormattedDateTime = []
    for i in range(0, len(DateTime)):
        ParsedDateTime = parser.parse(DateTime)
        FormattedDateTime.append(ParsedDateTime)
    plt.xlabel("Time")
    plt.ylabel("Elevation / km")
    plt.plot(FormattedDateTime, Elevation)
    plt.show()
    menu(Location)


def option6(DateTime, MagneticFieldStrength,Location):
    FormattedDateTime = []
    for i in range(0, len(DateTime)):
        ParsedDateTime = parser.parse(DateTime)
        FormattedDateTime.append(ParsedDateTime)
    plt.xlabel("Time")
    plt.ylabel("Magnetic Field Strength")
    plt.plot(FormattedDateTime, MagneticFieldStrength)
    plt.show()
    menu(Location)

def option7(MagX, MagY, MagZ, Location):
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.scatter3D(MagX, MagY, MagZ)
    ax.set_xlabel("Magnetometer X")
    ax.set_ylabel("Magnetometer Y")
    ax.set_zlabel("Magnetometer Z")
    plt.show()
    menu(Location)

location = input("Enter location of csv file: ")
menu(location)
