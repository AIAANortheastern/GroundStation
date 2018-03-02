# A Python Flask Application for Processing Radio Data

Version: 0.1

This application is designed to put real time radio data
into a csv file and display that data graphically in 
real time graphically.

Currently only the post processing of the data is working!

Real time processing from radio will be released with
the next version.

<a name="RunApp"></a>
## To Run the Application:
1. If you already have python 3 configured and installed skip
to [step 4.](#Step4)
1. Check your python version by running the command

        python -V
        
1. You should see a version of 3.6.x. If you don't then
you can install the latest and greatest version of python 
[HERE ](https://www.python.org/downloads/)

1. Make sure that you have python 3 Downloaded!
If you installed python 2 or if you already have it installed
then you are either going to have to do some magic to get them both working
side by side or to uninstall python 2. 

    <a name="Step4"></a>
1. Clone or download the project using the big green button above
1. Unzip the folder
1. Open up a terminal or command prompt and navigate to 
the installed directory using the cd command
Ex: 

        cd c:/Users/username/path/to/install/GroundStation

1. Run the following command to actually run the application:

        python runserver.py
        
1. Open up your favorite browser and go to the following link:

[localhost:8080](localhost:8080)

1. Click on "Use Existing Data"
        
        
## How to use my own data?
1. In the files you downloaded there is a file called 
AvionicesData.csv, open it with your favorite csv managing appication
Excel works great.

1. Open up your data file.

1. Change the headers on each of the columns in your 
csv file to match the headers listed here, use the
existing AvionicsData.csv file as an example:

        timestamp,pressure,altitude,temperature,
        gyrox,gyroy,gyroz,magx,magy,magz,rhall,
        accx,accy,accz

    For example: If you have a header called x Acceleration data
    it should now be labeled accx above the corresponding data.

1. Rename the existing AvionicsData.csv file to something
else.

1. Rename YOUR datafile to AvionicsData.csv. 

1. Run the groundstation by following the instructions
[In Running the application.](#RunApp)

