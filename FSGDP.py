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
    def __init__(self, data_pin=13, clock_pin=15, time_duration=0.00005):
        ''' Initializes the sender and sets up the pins
        '''
        GPIO.setwarnings(False)
        self.bit_length = "08b"
        self.adress = 23
        self.clock_pin = clock_pin
        self.data_pin = data_pin
        self.timing_duration = time_duration
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)

    def send_data(self, data, duration):
        ''' Send one bit (1/0, High/Low), with duration
        '''
        if data == True:
            GPIO.output(self.data_pin, GPIO.HIGH)
            GPIO.output(self.clock_pin, GPIO.HIGH)
        else:
            GPIO.output(self.data_pin, GPIO.LOW)
            GPIO.output(self.clock_pin, GPIO.HIGH)
        sleep(duration)
        GPIO.output(self.clock_pin, GPIO.LOW)
        GPIO.output(self.data_pin, GPIO.LOW)
        sleep(duration)
        
    def send_string(self, string_to_send, adress, progress=False):
        binary_list = []
        binary_list.append(255)
        binary_list.append(adress)
        binary_list.append(self.adress)
        binary_list.append(255)
        for char in string_to_send:
            binary_list.append(ord(char))
        binary_list.append(255)
        file_length = len(binary_list)
        print ("Length: " + str(file_length) + "byte")
        index = 0
        if progress: print ("Progress:")
        for element in binary_list:
            if progress:
                try:
                    index += 1
                    percentage = int((float(index) / float(file_length)) * 100.0)
                    if percentage % 10 == 0:
                        print (str(percentage) + "%")
                except ValueError:
                    print ("Error in indexing send object")
            self.send_data(True, self.timing_duration)
            element_string = format(element, '08b')
            for bit in element_string:
                self.send_data(bool(bit), self.timing_duration)
            GPIO.output(self.clock_pin, GPIO.LOW)
            sleep(self.timing_duration*5)

    def send(self, eingabe="", adress=""):
        ''' Sends a string with the send_data function (after conversion to binary)
        '''
        if eingabe == "":
            eingabe = (input("Message: ") + "\n")
        if adress == "":
            adress = input("To Adress: ")
        self.send_string(eingabe, int(adress))
        print ("Finished!")

    def send_file(self, file_location, adress):
        ''' Does the same as send, except it sends a file instead of plain text
        '''
        f_target = open(file_location, "r")
        file_content = f_target.read()
        f_target.close()
        self.send_string(file_content, int(adress))

class Receiver(object):
    ''' The receiver for the FSG-DataProtocol
    '''
    def __init__(self, data_pin=16, clock_pin=18):
        '''Sets the board up and configures the pins
        '''
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.adress = 3
        self.daten = []
        self.looked = False
        print ("Setup...")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.data_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.clock_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def receive(self):
        ''' Receives the incoming data and stores it in al list.
            To see it, use 'make_hr()'
        '''
        meta_incoming = False
        meta_over = False
        metadata = []
        while True:
            recv_thing = []
            while len(recv_thing) <= 8:
                if GPIO.input(self.clock_pin) == True and GPIO.input(self.data_pin) == True and self.looked == False:
                    recv_thing.append(True)
                    self.looked = True
                    #print ("Received a 1")
                elif GPIO.input(self.clock_pin) == True and GPIO.input(self.data_pin) == False and self.looked == False:
                    recv_thing.append(False)
                    self.looked = True
                    #print ("Received a 0")
                elif GPIO.input(self.clock_pin) == False:
                    self.looked = False
                #sleep(0.0001)
            #Break if EOL is received
            #print (recv_thing)
            if recv_thing[1:] == [True, True, True, True, True, True, True, True]:
                if meta_incoming == False and meta_over == False:
                    meta_incoming = True
                elif meta_incoming == True and meta_over == False:
                    meta_incoming = False
                    meta_over = True
                else:
                    break
            else:
                if meta_incoming == True:
                    metadata.append(int(''.join(['1' if x else '0' for x in recv_thing[1:]]), 2))
                else:
                    self.daten.append(int(''.join(['1' if x else '0' for x in recv_thing[1:]]), 2))
        return metadata, self.daten

    def make_hr(self, input_list=None):
        ''' Prints the received data to the command line
        '''
        satz = ""
        if input_list == None:
            input_list = self.daten
        for recv_byte in input_list:
            recv_string = str(recv_byte)
            """
            recv_string = recv_string.replace("[", '')
            recv_string = recv_string.replace("]", '')
            recv_string = recv_string.replace(",", '')
            recv_string = recv_string.replace(" ", '')
            #print ("String:" + str(recv_string))
            recv_int = int(recv_string, 2)
            #print ("Integer:" + str(recv_int))
            """
            buchstabe = chr(recv_byte)
            #print ("Character:" + str(buchstabe))
            satz += str(buchstabe)
            #print ("Satz:" + str(satz))
        print (satz)
        return satz

    def write_to_file(self, target_file):
        ''' Writes the received data to a file specified in target_file
        '''
        satz = self.make_hr()
        f_target = open(target_file, "w")
        f_target.write(satz)
        f_target.close()
        return satz

def close_connection():
    ''' Closes the connection
    '''
    GPIO.cleanup()
