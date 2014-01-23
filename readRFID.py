import sys
import os
import time
import serial
import csv
import optparse
import RPi.GPIO as GPIO

def RFIDread():
    ser = serial.Serial("/dev/ttyAMA0")
    print "waiting for a card"
    id = ser.read(13)
    print "The ID is :"
    print id
    ser.close()
    return id[1:]

def validateUser(id='',room=''):
    datetimenow=time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())
    logfile=open('userlog.txt','a')
    with open('userlist.csv','rb') as file:
        reader = csv.reader(file)
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if id in row['id']:
		invalidcard = False
                if 'yes' in row[room]:
                #    print 'yes'
                    logfile.write(datetimenow+'User:'+str(row['name'])+' Entered' + room+'\n')
                    logfile.close()
		    os.system('cp userlog.txt /boot')
                    return 1
                else:
                #    print 'No'
                    logfile.write(datetimenow+'User:'+str(row['name'])+' Access Denied to '+ room+'\n')
                    logfile.close()
                    return 0
	    else:
                logfile.write(datetimenow+'ID:'+id+ 'Un-registered \n')
	        logfile.close()
	        return 0
       
                

def main():
    os.system('rm -f userlog.txt')
    os.system('rm -f /boot/userlog.txt')
    os.system('cp /boot/userlist.csv .')
    os.system('echo none > /sys/class/leds/led0/trigger')
    parser = optparse.OptionParser()
    parser.add_option('-r', '--room',help='check access to this room',
                      dest='roomname', default='room1', action='store')
    parser.add_option('-f', '--forever', help='run forever',
                      dest='runf', default=False, action='store_true')
    (opts, args) = parser.parse_args()
    pin = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16,GPIO.OUT)
    GPIO.output(16,GPIO.HIGH)
    if(opts.runf == False):
        room = opts.roomname
        ID=RFIDread()
        key=validateUser(str(ID),str(room))
    else:
        while(True):
            roomcount = 0
            ID=RFIDread()
            if validateUser(str(ID),'room1'):
                roomcount = roomcount + 1
                print "access granted to room1"
		GPIO.output(16,GPIO.LOW)
                time.sleep(3)
		GPIO.output(16,GPIO.HIGH)
            if validateUser(str(ID),'room2'):
                roomcount = roomcount +1
                print "access granted to room2"
                time.sleep(3)
            if validateUser(str(ID),'room3'):
                roomcount = roomcount +1
                print "access granted to room3"
                time.sleep(3)
            if roomcount == 3:
                print "Sorry! No access"

    if room == 'room1':
        pin = 0
    elif room == 'room2':
        pin = 1
    elif room == 'room3':
        pin = 2

    if key:
        print "!! Access Granted !!"
        pfio.digital_write(pin,1)
        time.sleep(3)
        pfio.digital_write(pin,0)
    else:
        print "Sorry! No access"

if __name__ == "__main__":
    main()
    
 
