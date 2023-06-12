# -------------------------------
# HHORZIONS EXPERIMENT CODE
# -------------------------------

# -------------------------------
# IMPORTS
# -------------------------------

from pathlib import Path  # Ensure we use the right paths to store our data
from csv import writer  # To allow us to store our data in a csv file
from sense_hat import SenseHat  # To allow us to take readings of the environment using the sense-hat sensors
from datetime import datetime, timedelta  # To allow us to keep our program runtime under 3 hours
import time  # Allows us to calculate the time between accelerometer readings
from orbit import ISS  # Allows us to record the position of the ISS
from logzero import logger, logfile  # Allows us to log errors if they occur and log code events
import math  # Allows us to calculate the magnitude of the magnetometer readings
from random import randint  # Allows us to generate random numbers
import os  # Allows us to monitor the total file size of the files generated

# -------------------------------
# INITIALISING VARIABLES
# -------------------------------

# Creates the variable start_time at which the program starts
start_time = datetime.now()

# Creates the variable of base_folder, which has the file location where the program is located
base_folder = Path(__file__).parent.resolve()

# Creates the variable data_file and creates a csv file which is named data.csv in the file location of base_folder
data_file = base_folder / "data.csv"

# Creates the log file under the file path of the base_folder
logfile(base_folder / "HHorizons.log")

# Adds to the log the start time
logger.info(start_time)

# Creates the sense variable with the properties of the sense hat
sense = SenseHat()

# Sets the orientation of the text displayed to be correct
sense.set_rotation(270)

# Displays on the LED Matrix the string Hello World as per computer science tradition
sense.show_message('Hello World')

# Adds to log that the time variables and base folders have been created
logger.info('Time Variables & Base Folders Created')

# Declares the variables which is being used to calculate the displacement of the AstroPi
# V1 is the instantaneous velocity of the previous dataset
# V2 is the instantaneous velocity of the A1 dataset
# A1 is the previous acceleration
# A2 is the acceleration from two datasets ago
# Dis is the displacement of the AstroPi between the datasets of A0 and A1
# time1 is the time when A1 values is taken
# time1_2 is the time when A2 values is taken
# time2 is the time when the current acceleration values is taken
# The variables have an underscore with either x,y or z which refers to which axis the variable holds the value for


V1_x = float(0)
V2_x = float(0)
A1_x = float(0)
A2_x = float(0)
Dis_x = float(0)

V1_y = float(0)
V2_y = float(0)
A1_y = float(0)
A2_y = float(0)
Dis_y = float(0)

V1_z = float(0)
V2_z = float(0)
A1_z = float(0)
A2_z = float(0)
Dis_z = float(0)

# Gets the accelerometer values, which will be stored in the A2 variables in the x,y and z axes and
# the time for which the accelerometer took the readings

acc = sense.get_accelerometer_raw()
time1_2_x = time.time()
time1_2_y = time1_2_x
time1_2_z = time1_2_x

A2_x = acc["x"]
A2_y = acc["y"]
A2_z = acc["z"]

# Gets the accelerometer values, which will be stored in the A1 variables for the x,y and z axes and
# stores the time for which the accelerometer took the readings

acc = sense.get_accelerometer_raw()
time1_x = time.time()
time1_y = time1_x
time1_z = time1_x
A1_x = acc["x"]
A1_y = acc["y"]
A1_z = acc["z"]


# -------------------------------
# MAIN FUNCTION
# -------------------------------

# This is the main function which has the sensor readings and stores them into a list which is called sense_data and
# calculates the displacement of the AstroPi using our formula. Every sensor reading is done in a try-except to
# prevent any errors from taking those readings crashing the program, and it reports that error in the log and moves
# on. After the sensor reading is added to the sense_data list it is added to the log that it has been added,
# this also applies to the creation of the list and the displacement calculation. In the function at the start,
# it adds to the log the time at which it is called at. We use global variables to allow the function to access the
# starting data which is collected at the start outside the function.

# The function below is based off the Raspberry Pi Foundation Sense HAT Data Logger guide, specifically from the section
# Getting the data from the sense hat

def get_sense_data():
    # Declaring the global variables needed

    global V1_x
    global V2_x
    global A1_x
    global A2_x
    global Dis_x

    global V1_y
    global V2_y
    global A1_y
    global A2_y
    global Dis_y

    global V1_z
    global V2_z
    global A1_z
    global A2_z
    global Dis_z

    global time1_x
    global time1_y
    global time1_z

    global time1_2_x
    global time1_2_y
    global time1_2_z

    # Adds to the log the time at which the function was called at
    try:
        function_calltime = datetime.now()
        logger.info(function_calltime)
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

    # Creates the list named sense_data
    try:
        sense_data = []
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

    # Appends to the list the datetime
    try:
        sense_data.append(function_calltime)
        logger.info('Time Added - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

    # Appends to the list the magnetometer readings, first it takes the full readings and appends them separately to
    # list.
    # It also calculates the magnitude of the x,y,z readings using the formula the square root of x^2+y^2+z^2, it
    # appends that too to the list.

    try:
        mag = sense.get_compass_raw()
        logger.info('Mag Variable Created - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    try:
        sense_data.append(mag["x"])
        logger.info('Mag X added - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    try:
        sense_data.append(mag["y"])
        logger.info('Mag Y added - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    try:
        sense_data.append(mag["z"])
        logger.info('Mag Z added - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    try:
        sense_data.append(math.sqrt((pow(mag["y"], 2)) + (pow(mag["x"], 2)) + (pow(mag["z"], 2))))
        logger.info('Mag Magnitude Calculated And Added - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

    # Appends accelerometer readings, first it takes the full readings and appends them separately to list under
    # their axes. It takes the time of the accelerometer readings which will be used in the calculation of the
    # displacement.

    try:
        acc = sense.get_accelerometer_raw()
        time2_x = time.time()
        time2_y = time2_x
        time2_z = time2_x
        logger.info('Acc Variable Created - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    try:
        sense_data.append(acc["x"])
        logger.info('Acc X Added - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    try:
        sense_data.append(acc["y"])
        logger.info('Acc Y added - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    try:
        sense_data.append(acc["z"])
        logger.info('Azz Z added - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

    # We now use our displacement formula to calculate initially the previous velocity of the AstroPi. Then using the
    # calculated velocity and other data it will calculate the displacement of the AstroPi for that dataset. We do
    # this for all three axes to allow us to use the data collected to map the journey of the AstroPi in 3D and 2D
    # space against the magnetometer readings. We also add to the logg that the displacement is calculated when the
    # displacement is calculated. We cycle the readings so A2 has the value of A1 and A1 has the value of the current
    # acceleration, this happens for all the other variables as well

    try:
        V1_x = 0.5 * (A1_x + A2_x) * (time1_x - time1_2_x) + V2_x
        Dis_x = 0.25 * (acc["x"] + A1_x) * (time2_x - time1_x) + V1_x * (time2_x - time1_x)
        sense_data.append(Dis_x)
        A2_x = A1_x
        A1_x = acc["x"]
        V2_x = V1_x
        time1_2_x = time1_x
        time1_x = time2_x
        logger.info('Displacement X calculated - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

    try:
        V1_y = 0.5 * (A1_y + A2_y) * (time1_y - time1_2_y) + V2_y
        Dis_y = 0.25 * (acc["y"] + A1_y) * (time2_y - time1_y) + V1_y * (time2_y - time1_y)
        sense_data.append(Dis_y)
        A2_y = A1_y
        A1_y = acc["y"]
        V2_y = V1_y
        time1_2_y = time1_y
        time1_y = time2_y
        logger.info('Displacement Y calculated - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

    try:
        V1_z = 0.5 * (A1_z + A2_z) * (time1_z - time1_2_z) + V2_z
        Dis_z = 0.25 * (acc["z"] + A1_z) * (time2_z - time1_z) + V1_z * (time2_z - time1_z)
        sense_data.append(Dis_z)
        A2_z = A1_z
        A1_z = acc["z"]
        V2_z = V1_z
        time1_2_z = time1_z
        time1_z = time2_z
        logger.info('Displacement Z calculated - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

    # Appends to the list the longitude, latitude and elevation of the ISS
    # This is done by storing the ISS location in a variable called location
    # Then it extracts the longitude, latitude and elevation and appends it to the list
    # We take the ISS position data to check our calculated displacements from, but if our calculated displacement
    # is wrong we can use this data to plot our graph and calculate the function of that graph.

    try:
        location = ISS.coordinates()
        logger.info('Location Variable Created - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    try:
        sense_data.append(location.latitude)
        logger.info('Latitude added - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    try:
        sense_data.append(location.longitude)
        logger.info('Longitude added - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    try:
        sense_data.append(location.elevation.km)
        logger.info('Elevation added - Function')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    return sense_data


# -------------------------------
# WRITING THE HEADER
# -------------------------------

# Adds to the csv file named data.csv the header for the data collected, it does that by using a with open statement
# which closes it when the code inside it finishes We also use the try except method to prevent any errors from
# crashing the program Also, we add to the log that it has created the data writer variable and that the header has
# been added.

# The code below is based off the Raspberry Pi Foundation Sense HAT Data Logger guide, specifically from the section
# Adding a header to the CSV file.


with open('data.csv', 'w', buffering=1, newline='') as f:
    try:
        data_writer = writer(f)
        logger.info('Data writer variable created')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    try:
        data_writer.writerow(['DateTime', 'Mag X', 'Mag Y', ' Mag Z', 'Mag Magnitude', 'Acc X', 'Acc Y', 'Acc Z',
                              'Displacement X', 'Displacement Y', 'Displacement Z', 'ISS Latitude', 'ISS Longitude'
                                 , 'ISS Elevation'])
        logger.info('Header Added')
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

# -------------------------------
# MAIN WHILE LOOP
# -------------------------------

# In here we use a while loop which has the condition to run while the variable now_time, which is updated in the
# loop to have the time currently, is lower than the variable called start_time, which stores the value of the start
# time, plus 178.5 minutes to allow the program to finish within 3 hours. Inside we use a with-open statement which can
# only append to the .csv file and cannot overwrite the data in the .csv file. We also use the try-except method to
# prevent any errors from crashing the code. We also use the log to report any errors that have occurred, we also use
# it to report that the second data writer has been created and that the data has been added to the .csv file. We
# also display 'sparkles' on the LED matrix on the sense hat as an indication of the program running and also add to
# the log file that it has sparkled. We use the os.stat function to find out the file size in bytes of the specified
# file through the file size,we do that for the csv,log and program file and calculate their total file size and if
# it is equal to or greater than 2.99999 GB it exits the while loop, in testing the files created and the program
# itself, will not take more than 0.21 GB of space on the Astro Pi, but we want to be safe and make sure that it will
# not exceed the 3 GB file space limit on the Astro Pi.

# The code where it receives the data from the function and writes it to the csv file, also the while loop is based
# off the Raspberry Pi Foundation Sense HAT Data Logger guide, specifically from the section Writing the data to a file.

# The code where the sense hat sparkles it is based off the Raspberry Pi Foundation Sense HAT Random Sparkles guide.

now_time = datetime.now()
while now_time < start_time + timedelta(minutes=178.5):
    try:
        TotalFileSize = os.stat(base_folder / "data.csv").st_size
        TotalFileSize = TotalFileSize + os.stat(base_folder / "HHorizons.log").st_size
        TotalFileSize = TotalFileSize + os.stat(base_folder / "main.py").st_size
        if TotalFileSize >= 2999990000:
            break
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')
    with open('data.csv', 'a', buffering=1, newline='') as f:
        try:
            x = randint(0, 7)
            y = randint(0, 7)
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            sense.set_pixel(x, y, r, g, b)
            logger.info('Sparkled')
        except Exception as e:
            logger.error(f'{e.__class__.__name__}: {e})')
        try:
            data_writer = writer(f)
            logger.info('Data Writer 2 Created')
        except Exception as e:
            logger.error(f'{e.__class__.__name__}: {e})')
        try:
            data = get_sense_data()
            logger.info('Data Variable created and got the data')
            data_writer.writerow(data)
            logger.info('Data added')
            now_time = datetime.now()
        except Exception as e:
            logger.error(f'{e.__class__.__name__}: {e})')

# -------------------------------
# Finishing the program
# -------------------------------

# Displays on the LED Matrix the string Finished
sense.show_message('Finished')

# Stores the current time in the variable FinishTime
FinishTime = datetime.now()

# Adds to the log file the value of the variable FinishTime and the string FinishTime
logger.info('Finish Time')
logger.info(FinishTime)

# Clears the sense hat LED Matrix
sense.clear()

# End of Program
