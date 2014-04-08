#code to determine the location of an object using rotation matrices. 
import numpy as np

#we start by turning longtitude and latitude to right ascension to declination respectively

#this first part you input your long and lat coordinates in degrees to get the RA and DEC
def tocartesian(lon, lat):
    x = np.array([0.,0,0])
    x[0] = np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(lon))
    x[1] = np.cos(np.deg2rad(lat)) * np.sin(np.deg2rad(lon))
    x[2] = np.sin(np.deg2rad(lat))
    return x

#here we change from (RA, DEC) to (HA, DEC), calling this RD2HD
RD2HD = lambda LST: np.array([[np.cos(LST), np.sin(LST), 0],          [np.sin(LST), -np.cos(LST), 0], [0, 0, 1]])

#changing from (HA, DEC) to (AZ, ALT), 
HD2AA = lambda lat: np.array([[-np.sin(lat), 0, np.cos(lat)],         [0, -1, 0], [np.cos(lat), 0, np.sin(lat)]])

#from (AZ, ALT) to (l,b)
AA2lb = np.array([[-0.054876, -0.873437, -0.483835], [0.494109,       -0.444830, 0.746982], [-0.867666, -0.198076, 0.455984]])
#from now on, this code is based off of Kevin Yu's code for the tracking of sources
def untc(xp):
    return np.arctan2(xp[1], xp[0]), np.arcsin(xp[2])

def rd2aa(ra, dec, lst=None, lat=None):
    """Convert a RA, DEC, to AZ, ALT
    ra : rigth ascension of our object in radians
    dec : declination of object in radians
    lst : local sidereal time of the observer in radians
    lat : latitude of oserver in radians

    Returns az and alt in radians"""
    x = tocartesian(ra, dec)
    x = np.dot(RD2HD(lst), x)
    x = np.dot(HD2AA(lat), x)
    return untc(x)

