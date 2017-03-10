''' 
    MIT License
    Copyright (c) 2017 Peter Stengl
    [more info: see LICENSE file]
    -----------
    FSG Pfullingen Computer Science Club 2017
    -----------

    The Module for the FSG-DataProtocol, used for
    Sender and Receiver, that's why we used classes
'''

import RPi.GPIO as GPIO
from time import sleep

class Sender(object):
    ''' The sender-class to send data with the FSG-DataProtocol
    '''
    def __init__(self, data_pin=13, clock_pin=15, time_duration=0.005):
        ''' Initializes the Sender and sets up the Pins
        '''
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
        ''' Sends a String with the send_data function (after conversion to binary)
        '''
        binary_list = []
        if eingabe == "":
            eingabe = (raw_input("Message: ") + "\n")
        for character in eingabe:
            c_binary = format(ord(character), "08b")
            binary_list.append(c_binary)
        print binary_list
        for element in binary_list:
            self.send_data("1", self.timing_duration)
            for bit in element:
                self.send_data(bit, self.timing_duration)
            GPIO.output(self.clock_pin, GPIO.LOW)
            sleep(self.timing_duration)

    def send_file(self, file_location):
        ''' Does the same as send, except it sends a file instead of plain text
        '''
        f_target = open(file_location, "r")
        file_content = f_target.read()
        file_length = len(file_content)
        f_target.close()
        print file_length
        print "Sending :[",
        for character in file_content:
            try:
                index = file_content.index(character)
                percentage = int((index / file_length) * 100)
                if percentage % 10:
                    print "#",
            except ValueError:
                print "Error in indexing send object"
            self.send_data("1", self.timing_duration)
            c_binary = format(ord(character), "08b")
            #print c_binary
            for bit in c_binary:
                self.send_data(bit, self.timing_duration)
            GPIO.output(self.clock_pin, GPIO.LOW)
            sleep(self.timing_duration)
        print "]"
        print "Finished"

class Receiver(object):
    ''' The Receiver for the FSG-DataProtocol
    '''
    def __init__(self, data_pin=16, clock_pin=18):
        '''Sets the Board up and configures the pins
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
        ''' Receives the incoming Data and stores it in al list.
            To see it, use 'make_HR()'
        '''
        while True:
            recv_thing = [0, 0]
            recv_thing = []
            while len(recv_thing) <= 8:
                if GPIO.input(self.clock_pin) and GPIO.input(self.data_pin) and not self.looked:
                    recv_thing.append(1)
                    self.looked = True
                    #print "Received a 1"
                elif GPIO.input(self.clock_pin) and GPIO.input(self.data_pin) and not self.looked:
                    recv_thing.append(0)
                    self.looked = True
                    #print "Received a 0"
                elif GPIO.input(self.clock_pin) is not True:
                    self.looked = False
                sleep(0.000000001)
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
        ''' Prints the received data to the Command Line
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
        return satz

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
    ''' Closes the Connection
    '''
    GPIO.cleanup()
