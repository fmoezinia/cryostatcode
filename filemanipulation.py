import urllib2
from datetime import datetime
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt 
import numpy as np
import os
import time

color=''
global errordata
errordata=[]
global operationaldata
operationaldata=[]
global inopdata
inopdata=[]

minallowed0= 1.6
maxallowed0=4.0
minallowed5=10.0
maxallowed5=18.0
minallowed9=70.0
maxallowed9=130.0
#WHAT ARE REAL RANGES??
minallowed=0
maxallowed=0.0002
gamma0=1
gamma5=0.6
gamma9=0.6
#REAL GAMMA WORKING?
gamma=4

antennaarray = ['CM01','CM02','CM03','CM04','CM05','CM06','CM07','CM08','CM09','CM10','CM11','CM12','DA41','DA42','DA43','DA44','DA45',
'DA46','DA47','DA48','DA49','DA50','DA51','DA52', 'DA53',  'DA54','DA55','DA56','DA57','DA58','DA59','DA60','DA61','DA62','DA63','DA64',
'DA65','DV01','DV02','DV03','DV04','DV05','DV06','DV07','DV08','DV09','DV10','DV11','DV12','DV13','DV14','DV15','DV16','DV17',
'DV18','DV19','DV20','DV21','DV22','DV23','DV24','DV25','PM01','PM02','PM03','PM04']
#path = '/Users/rickymoezinia/Documents/ALMA Cryostatic GUI Internship/savedfiles/'

a = ['0', '5','9']
b = ['0']

def firstinterfacefunction(antenna, temp_pressurefilename, color, minallowed, maxallowed, gamma, temp_pressure, temp_pressure2, ylabel):
    start = time.time()
    timeplot=[]
    temp=[]
    contents=[]
    #TIMES for file manipulation filename.
    now = datetime.now()
    year= str(now.year)
    if len(str(now.month)) == 1:
        month = '0'+str(now.month)
    else:
        month= str(now.month)
    if len(str(now.day)) == 1:
        day = '0'+str(now.day)
    else:
        day= str(now.day)

    
    
    
    filename = 'http://monitordata.osf.alma.cl/index.php?dir=' + year + '%2F' + month + '%2F' + year + '-' + month + '-' + day + '%2FCONTROL_' + antenna + '_FrontEnd_Cryostat%2F&download=' + temp_pressure + temp_pressurefilename +  temp_pressure2 + '.txt' 


    #OPENING FILE
    arraystring = urllib2.urlopen(filename).readlines()
    
    #NAMING TEMP0/5/9 AS TEMP STAGE I/II/III
    if temp_pressurefilename == '0':
        temp_pressurefilename = 'Stage_I'
    elif temp_pressurefilename == '5':
        temp_pressurefilename = 'Stage_II'
    elif temp_pressurefilename == '9':
        temp_pressurefilename = 'Stage_III'
    
    

    #SOME DONT HAVE READINGS AT TIMES, SO MAKE SURE, IF RESPONSE.READLINES() = [] IGNORE.
    if arraystring != []:
    
    
        #REMOVE LINE BREAKS
        for strings in arraystring:
            contents.append(strings.replace("\n", ''))
        #print contents
    
        #SPLIT CONTENTS TO DATE, TIME, TEMP (deleted milliseconds and secs)
        date=[]
        t_time=[]
        for string in contents:
            date.append(string[0:10])
            t_time.append(string[11:16])
            temp.append(string[24:])
       
        #TAKES OUT QUOTATION MARKS from date list.  
        dateplot =  " ".join(date)
        #SPLIT TIME INTO HOURS AND MINUTES
        hour=[]
        minute=[]
        for thetime in t_time:
            hour.append(thetime[0:2])
            minute.append(thetime[3:5])


        #MINUTES TO HOUR CONVERSION (AND CONVERSION TO LIST OR ARRAY)
        minutetohour=[float(x) / 60 for x in minute]
        hour=[float(x) / 1 for x in hour]
    
        #HOURS + MINUTES INTO TIMEPLOT 
        for minutetohour,hour in zip(minutetohour,hour):
            timeplot.append(minutetohour+hour)

        
        #DETECTING ERRORS
        count = 0
        tempindex=[]
        for item in temp:
            if (float(item) > maxallowed) or (float(item) < minallowed):
                count += 1
                #FINDING OUT WHEN ERRORS ARE, NOT USEFUL FOR CLEAR GRAPHS...
                tempindex.append(temp.index(item))
        # if tempindex != []:
        #     firsterror = timeplot[min(tempindex)]
        #     finalerror = timeplot[max(tempindex)]
            

        #PLOTTING ONES WITH ERRORS.(TIMEPLOT VS TEMP)    
        if count > 0:
            #print "Device Problem! Attention needed."
            #print 'You have %s errors' % count
            #print "Errors occur between %s and %s hours on %s" % (firsterror, finalerror, dateplot[0:11])
            #PLOTTING IF ERROR:
            plt.plot(timeplot,temp,linewidth = 1.5, color=color, label = temp_pressure + " " + temp_pressurefilename)
            plt.ylabel(ylabel)
            plt.xlabel('Time (Hours)')
            plt.axhline(minallowed, xmin=-1000000, xmax=1000000,linewidth=2, color = 'r')
            plt.axhline(maxallowed, xmin=-1000000, xmax=1000000,linewidth=2, color = 'r')
            plt.ylim(float(min(temp)) - (gamma*float(min(temp)))),(float(max(temp)) + (gamma*float(max(temp))))
            plt.xlim(min(timeplot),max(timeplot))
            plt.title("Error-riden        " + antenna)
            #legend
            leg = plt.legend(fancybox=True, loc=4)
            leg.get_frame().set_alpha(0.5)
            #plt.show()
            #SAVE FIGURE TO OWN DIRECTORY 
            errorfile = os.path.dirname(os.path.abspath(__file__)) + '/' + antenna + temp_pressure + temp_pressurefilename + '.png'
            plt.savefig(errorfile, format = 'png')
            #time.sleep(1)
            plt.hold(False)
            #28: STRING SLICE IS FOR RELATIVE PATH NOT ABSOLUTE (SPECIFIC TO SERVER)
            errordictionary = {'Antenna': antenna , 'Monitor Point': temp_pressure + " " + temp_pressurefilename, 'PathToImagefile': errorfile[28:]}
            errordata.append(errordictionary)
            
            
            #print 'This program took', time.time()-start, 'seconds to run.'
            #PRINT OUT HTML SCRIPT IN LONG STRING
            
        #OPERATIONAL ANTENNAS PROCESS DATA  
        else:
            plt.plot(timeplot, temp, linewidth = 1.8, color = color, label = temp_pressure + " " + temp_pressurefilename)
            plt.ylabel(ylabel)
            plt.xlabel('Time (Hours)')
            plt.axhline(minallowed, xmin=-1000000, xmax=1000000,linewidth=2, color = 'r')
            plt.axhline(maxallowed, xmin=-1000000, xmax=1000000,linewidth=2, color = 'r')
            plt.ylim(float(min(temp)) - (gamma*float(min(temp)))),(float(max(temp)) + (gamma*float(max(temp)))+5)
            plt.xlim(min(timeplot),max(timeplot))
            plt.title("Operational      " + antenna)
            #legend
            leg = plt.legend(fancybox=True, loc=4)
            leg.get_frame().set_alpha(0.5)
            #plt.show()
            operationalfile = os.path.dirname(os.path.abspath(__file__)) + '/' + antenna + temp_pressure + temp_pressurefilename + '.png'
            plt.savefig(operationalfile, format = 'png')
            #time.sleep(1)
            plt.hold(False)
            ##28: STRING SLICE IS FOR RELATIVE PATH NOT ABSOLUTE (SPECIFIC TO SERVER)
            operationaldictionary = {'Antenna': antenna , 'Monitor Point': temp_pressure + " " + temp_pressurefilename, 'PathToImagefile': operationalfile[28:]}
            operationaldata.append(operationaldictionary)
            #print "No errors for %s-%s-%s ,  on antenna %s ,  temperature reading %s" % (year, month, day, antenna, temperaturereading)
        
    #PROBLEM WITH FILE/NO MONITORDATA , ANTENNA OFF 
    #else:
        #BECAUSE THE ORIGINAL FILE IN MONITORDATA DOES NOT EXIST, IN HTML SCRIPT, MUST PASS OTHER ANTENNAS WHICH ARE NOT PRESENT IN OPERATIONALDATA OR ERRORDATA 
        # TO THE TABLE AND DISPLAY CELLS AS BLACK FILLED IN, INOPERATIVE.
        #WOULD LIKE TO PROCESS EMPTY DATA -- EMPTY DATA DICTIONARY, ANTENNA, MONITOR POINT, NO FILE, JUST BLACKENED CELL.
        
    
        
    #CALLING FIRSTINTERFACEFUNCTION
   
a = ['0', '5','9']
b = ['0']


#ONLY LOOPING FIRST 5 ANTENNAS!!
for j in range(66):
#PRESSURE
    for i in b:
        firstinterfacefunction(antennaarray[j], str(i), 'k', minallowed, maxallowed, gamma, 'VACUUM_GAUGE_SENSOR', '_PRESSURE', 'Pressure (mbar)')
    #plt.show()
     
#TEMPERATURE
    for i in a:
        if i == '0':
            color = 'b'
        elif i == '5':
            color = 'k'
        elif i == '9':
            color=  'g'
        firstinterfacefunction(antennaarray[j], str(i) , color , eval('minallowed' + str(i)) , eval('maxallowed' + str(i)), eval('gamma'+str(i)), 'TEMP', '_TEMP', 'Temperature (K)')
    #plt.show()
    
#firstinterfacefunction('CM01', '5'. 'k',minallowedB,maxallowedB, gammaB, 'TEMP','_TEMP', 'Temp')     
    

#HTML RENDERING SCRIPT HERE
#print errordata
#print operationaldata[0]
#print errordata
#errordata=[]
#<td> tag can fill cell with red color for example......instead of just link...



header = """<html>
<!--(to run every x minutes using cron software)-->
<head>
<title> States Of Cryosystems</title>
<meta http-equiv="refresh" content="500" />	
</head>
<body>
<h1> Refer to Links below to view 24 Hour Plots displaying Cryosystem State <br> <br> Red = Error &nbsp;&nbsp;&nbsp;&nbsp 
 Black = Inoperative &nbsp;&nbsp;&nbsp;&nbsp   Green = Operational</h1>

<table border=1 bgcolor=#808082 style="width:90%"> 
<tr>
    <th>Antenna Number</th>
    <th>Monitoring</th> 
    <th>Image Link</th>
  </tr> """

#GETTING INOPERATIVE LIST OF ANTENNAS:
usedeantennas=[]
errorantennas=[]
operationalantennas=[]
for item in errordata:
    a = sorted(item.items())
    errorantennas.append(a[0][1])
    #print errorantennas
for item in operationaldata:
    a = sorted(item.items())
    operationalantennas.append(a[0][1])
    #print operationalantennas
    
    
#GOING TO ADD SECTION FOR CAUTION ANTENNAS /MPs
usedantennas = operationalantennas + errorantennas    

#inopantennas is list
inopantennas=[]
for item in antennaarray:
    if item not in usedantennas:
        inopantennas.append(item)
#print inopantennas
#prob with operationalantennas?
#print operationalantennas



errorrows = ''
for item in errordata:
    #a is list which contains Antenna number, Monitor Point , and Path (alphabetical order) for each dictionary in errordata list.
    a = sorted(item.items())
    newRow = '<tr> <td>' + str(a[0][1]) + '</td> <td>' +    str(a[1][1])  + '</td> <td> <a href=' + '"' + str(a[2][1]) + '"'+ 'style="color: #FF0000"> Link to 24 hour plot</a> </td> </tr>'
    errorrows +=newRow
#print errorrows
#print errordata
    


#<td> tag can fill cell with green color for example....
operationalrows =''
for item in operationaldata:
    b = sorted(item.items())
    #print b
    newRow = '<tr> <td>' + str(b[0][1]) + '</td> <td>' +    str(b[1][1])  + '</td> <td> <a href=' + '"' + str(b[2][1]) + '"'+ 'style="color: #00FF00"> Link to 24 hour plot</a> </td> </tr>'
    operationalrows += newRow



#TAKE INOPANTENNAS AND MAKE NEXT SECTION OF TABLES, JUST ANTENNAS.
inoperativerows = ''
for i in inopantennas:
    newRow = '<tr> <td>' + i + '</td> <td>' + '</td> <td>' + '</td> </tr>'
    inoperativerows += newRow








footer = """</table>
</body>
</html>"""

#(inoprows) + cautionrows coming later...
htmlContent = header + errorrows + operationalrows + inoperativerows + footer
#print htmlContent

text_file = open("index.html", "w")

text_file.write(htmlContent)

text_file.close()





