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
    def __init__(self, data_pin=13, clock_pin=15, time_duration=0.005):
        ''' Initializes the sender and sets up the pins
        '''
        GPIO.setwarnings(False)
        self.bit_length = "08b"
        self.adress = ""
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
        
    def send_string(self, string_to_send, adress):
        binary_list = []
        binary_list.append("11111111")
        binary_list.append(adress)
        binary_list.append("11111111")
        for character in string_to_send:
            c_binary = format(ord(character), self.bit_length)
            binary_list.append(c_binary)
        binary_list.append("11111111")
        file_length = len(binary_list)
        print "Length: " + str(file_length) + "byte"
        index = 0
        print "Progress:"
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
            sleep(self.timing_duration*2)

    def send(self, eingabe="", adress=""):
        ''' Sends a string with the send_data function (after conversion to binary)
        '''
        if eingabe == "":
            eingabe = (raw_input("Message: ") + "\n")
        if adress == "":
            adress = raw_input("To Adress: ")
        self.send_string(eingabe, adress)
        print "Finished!"

    def send_file(self, file_location, adress):
        ''' Does the same as send, except it sends a file instead of plain text
        '''
        f_target = open(file_location, "r")
        file_content = f_target.read()
        f_target.close()
        self.send_string(file_content, adress)

class Receiver(object):
    ''' The receiver for the FSG-DataProtocol
    '''
    def __init__(self, data_pin=16, clock_pin=18):
        '''Sets the board up and configures the pins
        '''
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.adress = [0,0,0,0,0,0,0,1]
        self.daten = []
        self.looked = False
        print "Setup..."
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.data_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.clock_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def receive(self):
        ''' Receives the incoming data and stores it in al list.
            To see it, use 'make_HR()'
        '''
        adress_incoming = False
        adress_came_in = False
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
            #Break if EOL is received
            print recv_thing, adress_came_in, adress_incoming
            if adress_incoming == True and adress_came_in == False:
                    is_for_adress = recv_thing[1:]
                    print "Is for adress:" + str(is_for_adress)
                    adress_came_in = True
            if recv_thing[1:] == [1,1,1,1,1,1,1,1]:
                if adress_came_in == True and adress_incoming == False:
                    break
                if adress_came_in == False and adress_incoming == False:
                    print "Now is adress coming"
                    adress_incoming = True
                else:
                    print "Adress over"
                    adress_incoming = False
            else:
                self.daten.append(recv_thing[1:])
        if is_for_adress == self.adress:
            print "This Packet was for you!"
        else:
            print "This Packet wasn't for you!"
            
        print "Your adress:" + str(self.adress)
        print "Dest. adress:" + str(is_for_adress)

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
