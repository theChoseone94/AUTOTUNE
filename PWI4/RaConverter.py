
def RAconverter_HHtoDec(RA):
    #takes in ra as hours in HH:MM:SS
    #outputs the dec
    star_ra_hours = RA.split(':')
    
    Deci = [float(star_ra_hours[0])+(float(star_ra_hours[1])/60+(float(star_ra_hours[2])/60/60))] 

    return Deci


def RAconverter_DectoHH(RA):
    if isinstance(RA,float) != True:
        print('The input is NOT float')
        return False
    _,hours = divmod(RA*3600,86400)
    hours,minutes = (divmod(hours,3600))
    minutes, seconds = (divmod(minutes,60))
    seconds = round(seconds)
    HH = ("%i:%i:%i"%(hours,minutes,seconds))
    return HH


def DecConverter_DecitoDD(Dec):
    if (str(Dec)[:1]) == "-":
        deg = str(Dec)[1:3]
        mnt = (-Dec-float(str(Dec)[1:3]))*60
        sec = (mnt - float(str(mnt)[0:2]))*60
        sec = round(sec)
        Dec_dms = ("%s:%s:%s"%(deg,str(mnt)[0:2],sec))
        return Dec_dms
    elif (str(Dec)[:1]) != "-":
        deg = str(Dec)[0:2]
        mnt = (Dec-float(str(Dec)[0:2]))*60
        sec = (mnt - float(str(mnt)[0:2]))*60
        sec = round(sec)
        Dec_dms = ("%s:%s:%s"%(deg,str(mnt)[0:2],sec))
        return Dec_dms

