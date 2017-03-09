''' 
    MIT License
    Copyright (c) 2017 Peter Stengl
    [more info: see LICENSE file]
    -----------
    FSG Pfullingen Computer Science Club 2017
    -----------

    The module for the FSG-DataProtocol, used for
    sender and receiver, that's why we used classes
'''

import RPi.GPIO as GPIO
from time import sleep

class Sender(object):
    ''' The sender-class to send data with the FSG-DataProtocol
    '''
    def help(self):
		print "Aviable commands: \n \n __init__() |optional: data_pin, clock_pin, time_duration | initializing \n \n send_data(data) | optional: duration | send binary data \n \n send(data) | optional: none | sends strings \n  \n send_file(file_location) | optional: none | sends fles \n \n close_connection() | optional: none | close the connection and clear all pins \n \n \n \n"
    def __init__(self, data_pin=13, clock_pin=15, time_duration=0.005):
        ''' Initializes the sender and sets up the pins
        '''
        GPIO.setwarnings(False)
        self.clock_pin = clock_pin
        self.data_pin = data_pin
        self.timing_duration = time_duration
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)

    def send_data(self, data, duration):
        ''' Send one bit (1/0, High/Low), with duration
        '''
        GPIO.output(self.clock_pin, GPIO.HIGH)
        if data == "1":
            GPIO.output(self.data_pin, GPIO.HIGH)
        else:
            GPIO.output(self.data_pin, GPIO.LOW)
        sleep(duration)
        GPIO.output(self.clock_pin, GPIO.LOW)
        GPIO.output(self.data_pin, GPIO.LOW)
        sleep(duration)

    def send(self, eingabe=""):
        ''' Sends a string with the send_data function (after conversion to binary)
        '''
        binary_list = []
        if eingabe == "":
            eingabe = (raw_input("Message: ") + "\n")
        for character in eingabe:
            c_binary = format(ord(character), "08b")
            binary_list.append(c_binary)
        file_length = len(binary_list)
        print "Length: " + str(file_length) + "byte"
        index = 0
        for element in binary_list:
            try:
                index += 1
                percentage = int((float(index) / float(file_length)) * 100.0)
                if percentage % 10 == 0:
                    print str(percentage) + "%"
            except ValueError:
                print "Error in indexing send object"
            self.send_data("1", self.timing_duration)
            for bit in element:
                self.send_data(bit, self.timing_duration)
            GPIO.output(self.clock_pin, GPIO.LOW)
            sleep(self.timing_duration)
        print "Finished!"

    def send_file(self, file_location):
        ''' Does the same as send, except it sends a file instead of plain text
        '''
        f_target = open(file_location, "r")
        file_content = f_target.read()
        file_length = len(file_content)
        f_target.close()
        print "Lenght: " + str(file_length) + "bytes"
        index = 0
        looked = False
        print "Progress:"
        for character in file_content:
            try:
                index += 1
                percentage = int((float(index) / float(file_length)) * 100.0)
                if percentage % 10 == 0 and looked == False:
                    print str(percentage) + "%"
                    looked = True
                else:
                    looked = False
            except ValueError:
                print "Error in indexing send object"
            self.send_data("1", self.timing_duration)
            c_binary = format(ord(character), "08b")
            #print c_binary
            for bit in c_binary:
                self.send_data(bit, self.timing_duration)
            GPIO.output(self.clock_pin, GPIO.LOW)
            sleep(self.timing_duration)
        print "Finished"

class Receiver(object):
    ''' The receiver for the FSG-DataProtocol
    '''
    def help(self):
		print "Available comands: \n \n __init__() | optional: data_pin, clock_pin | initializing \n \n receive() | optional: end_with_eol (break if receive eol) | receive data \n \n make_hr() | optional: none | show received data \n \n write_to_file(target_file) | optional: none | write received data to a file \n \n \n \n"
    
    def __init__(self, data_pin=16, clock_pin=18):
        '''Sets the board up and configures the pins
        '''
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.daten = []
        self.looked = False
        print "Setup..."
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.data_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.clock_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def receive(self, end_with_eol=True):
        ''' Receives the incoming data and stores it in al list.
            To see it, use 'make_HR()'
        '''
        while True:
            recv_thing = [0, 0]
            recv_thing = []
            while len(recv_thing) <= 8:
                if GPIO.input(self.clock_pin) == True and GPIO.input(self.data_pin) == True and self.looked == False:
                    recv_thing.append(1)
                    self.looked = True
                    #print "Received a 1"
                elif GPIO.input(self.clock_pin) == True and GPIO.input(self.data_pin) == False and self.looked == False:
                    recv_thing.append(0)
                    self.looked = True
                    #print "Received a 0"
                elif GPIO.input(self.clock_pin) == False:
                    self.looked = False
                sleep(0.0001)
            self.daten.append(recv_thing[1:])
            #Break if EOL is received
            string_of_recv = str(recv_thing[1:])
            string_of_recv = string_of_recv.replace("[", '')
            string_of_recv = string_of_recv.replace("]", '')
            string_of_recv = string_of_recv.replace(",", '')
            string_of_recv = string_of_recv.replace(" ", '')
            #print string_of_recv
            recv_int = int(string_of_recv, 2)
            #print recv_int
            if recv_int == 10 and end_with_eol is True:
                break

    def make_hr(self):
        ''' Prints the received data to the command line
        '''
        satz = ""
        for recv_byte in self.daten:
            recv_string = str(recv_byte)
            recv_string = recv_string.replace("[", '')
            recv_string = recv_string.replace("]", '')
            recv_string = recv_string.replace(",", '')
            recv_string = recv_string.replace(" ", '')
            #print "String:" + str(recv_string)
            recv_int = int(recv_string, 2)
            #print "Integer:" + str(recv_int)
            buchstabe = chr(recv_int)
            #print "Character:" + str(buchstabe)
            satz += str(buchstabe)
            #print "Satz:" + str(satz)
        print satz

    def write_to_file(self, target_file):
        ''' Writes the received data to a file specified in target_file
        '''
        satz = ""
        for recv_byte in self.daten:
            recv_string = str(recv_byte)
            recv_string = recv_string.replace("[", '')
            recv_string = recv_string.replace("]", '')
            recv_string = recv_string.replace(",", '')
            recv_string = recv_string.replace(" ", '')
            #print "String:" + str(recv_string)
            recv_int = int(recv_string, 2)
            #print "Integer:" + str(recv_int)
            buchstabe = chr(recv_int)
            #print "Character:" + str(buchstabe)
            satz += str(buchstabe)
            #print "Satz:" + str(satz)
        f_target = open(target_file, "w")
        f_target.write(satz)
        f_target.close()
        return satz

def close_connection():
    ''' Closes the connection
    '''
    GPIO.cleanup()
