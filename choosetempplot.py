import fileinput
import matplotlib.pyplot as plt
import os
 #'temp' + str(i) + '.php'

minallowedtempA= 1.6
maxallowedtempA=4.0
minallowedtempB=10.0
maxallowedtempB=18.0
minallowedtempC=70.0
maxallowedtempC=130.0
gammaA=0.2
gammaB=0.1
gammaC=0.06
#in case need optimal temp in legend
# optimalA=4.0
# optimalB=15.0
# optimalC=110.0


def chooseplotfunction():
    
    minallowedtemp = 0.0
    maxallowedtemp = 0.0
    gamma = 0.0
    timeplot=[]
    temp=[]
    arraystring=[]
    contents=[]
    date=[]
    t_time=[]
    #ask user for antenna (1-66), temp(s)(0-12).
    antennaanswer = raw_input("Which antenna would you like to examine? Please type antenna number (1-66)")
    tempanswer = raw_input("Which monitoring temperature(s) of antenna number %s woud you like to examine? (Temp0-Temp12)" % (antennaanswer))
    filename = antennaanswer + 'temp' + tempanswer + '.php'
#setting up correct parameters for A,B,C    
    if int(tempanswer) < 5:
        minallowedtemp = minallowedtempA
        maxallowedtemp = maxallowedtempA
        gamma = gammaA
    elif int(tempanswer) < 9:
        minallowedtemp = minallowedtempB
        maxallowedtemp = maxallowedtempB
        gamma = gammaB
    elif int(tempanswer) < 13:
        minallowedtemp = minallowedtempC
        maxallowedtemp = maxallowedtempC
        gamma = gammaC    

    with open(filename) as file:
        arraystring = file.readlines()  
    #print arraystring

    #REMOVE LINE BREAKS
    for strings in arraystring:
        contents.append(strings.replace("\n", ''))
    #print contents


    #SPLIT CONTENTS TO DATE, TIME, TEMP (deleted milliseconds and secs)

    for string in contents:
        date.append(string[0:10])
        t_time.append(string[11:16])
        temp.append(string[24:])
    #print date
    #print t_time
    #print temp
    #print type(date)
    #print type(temp)
    #print type(t_time)

    
    #ASKING USER FOR DATE/TIMEFRAME FOR PLOTS.
    # dateanswer = raw_input("From which date would you like temperature data? (Form: YYYY-MM-DD)")
    t_timeanswer1 = raw_input("From what time would you like to analyze? (Form: HH:MM) If you would like the entire day/file, please double-tap enter")
    t_timeanswer2 = raw_input("Until what time would you like to analyze? (Form: HH:MM)")
    if (t_timeanswer1 and t_timeanswer2) != '':
        index1=t_time.index(t_timeanswer1)
        index2=t_time.index(t_timeanswer2)
        t_time = t_time[index1:(index2+1)]
        temp = temp[index1:(index2+1)]
        

    #TAKES OUT QUOTATION MARKS
    dateplot =  "[%s]" % (','.join(date))
    # print dateplot

    #SPLIT TIME INTO HOURS AND MINUTES
    hour=[]
    for thetime in t_time:
        hour.append(thetime[0:2])
    #print hour
    minute=[]
    for thetime in t_time:
        minute.append(thetime[3:5])
    #print minute
    #print type(minute)

    #MINUTES TO HOUR CONVERSION (AND CONVERSION TO LIST OR ARRAY)
    minutetohour=[float(x) / 60 for x in minute]
    #print minutetohour
    hour=[float(x) / 1 for x in hour]
    #print hour

    #HOURS + MINUTES INTO TIMEPLOT 

    for minutetohour,hour in zip(minutetohour,hour):
        timeplot.append(minutetohour+hour)
    #print dateplot    
    #print timeplot
    #print temp
    #print type(dateplot)
    #print type(timeplot)
    #print type(temp)


    #PLOTTING
    plt.plot(timeplot,temp,ls=':',marker='o',ms=4, color='g', label = filename)
    #plt.ylabel('Temperature (K)')
    #plt.xlabel('Time (Hours)')
    plt.axhline(minallowedtemp, xmin=0, xmax=100,linewidth=1.2, color = 'r')
    plt.axhline(maxallowedtemp, xmin=0, xmax=100,linewidth=1.2, color = 'r')
    plt.ylim((minallowedtemp - (gamma*float(min(temp)))),(maxallowedtemp + (gamma*float(max(temp)))))
    plt.xlim(min(timeplot),max(timeplot))
    plt.ylabel('Temperature (K)')
    plt.xlabel('Time (Hours)')
    plt.title(min(date) + ' to ' + max(date))
    #legend
    leg = plt.legend(fancybox=True, loc=1)
    leg.get_frame().set_alpha(0.5)
    plt.show()

    print os.getcwd()
chooseplotfunction()



        
    