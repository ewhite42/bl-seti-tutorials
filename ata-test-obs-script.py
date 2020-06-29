"""
This is a simple observing script written to test
Allen Telescope Array control library, ata_control. 

Ellie White 24 June 2020

"""

from ATATools import ata_control as ac
import time

def main():

    alist = ['1a', '1c', '2h'] #define antennas list (alist)
    src = 'moon' #define target source
    #az_off = 5 #define azimuth offset for on-off scan
    #el_off = 5 #define elevation offset for on-off scan
    freq = 1400 #set center frequency in MHz
    duration = 30 #duration of tracking

    #lock out the antennas you will be using
    ac.reserve_antennas(alist) 

    #turn on the LNAs if they're not already on
    ac.try_on_lnas(alist)

    #set up with Autotune
    ac.autotune(alist)

    #display starting coordinates so 
    #you can verify antennas have moved
    start_radec = ac.getRaDec(alist)
    print("The current coordinates are: ", start_radec)

    #create ephemeris file that tells the antenna
    #where it should be pointing at each timestamp
    ac.make_and_track_ephems(src, alist)

    #set the center frequency
    ac.set_freq(freq, alist)

    #print the coordinates after the antennas have
    #been given the point and track command to ensure
    #that they moved.     
    src_radec = ac.getRaDec(alist)
    print("The source coordinates are: ", src_radec)
    
    #stay on source for the given duration
    time.sleep(duration) 

    #unlock the antennas once you're done
    ac.release_antennas(alist, True)
    

if __name__ == "__main__": 
    main()
